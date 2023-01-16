"""
Generate OpenAPI 3.0 Spec
"""
# TODO: fix dupe code
# pylint: disable=duplicate-code

import copy
import http.client
import logging

import yaml

from firestone.spec import _base as spec_base

# This is a list of all HTTP methods supported on high-level resource base
RSRC_HTTP_METHODS = ["delete", "get", "head", "patch", "post"]

# This is a list of all HTTP methods supported on an instance of a resource
RSRC_INST_HTTP_METHODS = ["delete", "get", "head", "patch", "put"]

# This is a list of all HTTP methods supported on attributes of an instance of a resource
RSRC_ATTR_HTTP_METHODS = ["delete", "get", "head", "put"]

_LOGGER = logging.getLogger(__name__)

# TODO add support for JSON Patch: https://www.jvt.me/posts/2022/05/29/openapi-json-patch/


def get_responses(
    method: str,
    schema: dict,
    content_type: str,
    comp_name: str = None,
    attr_name: bool = None,
    is_list: bool = None,
):
    """Set schema for a given operation type."""
    if method == "head":
        return {"default": {"description": "Default HEAD response"}}

    resp_code_enum = http.client.OK
    if method == "post":
        resp_code_enum = http.client.CREATED

    responses = {
        resp_code_enum.value: {
            "description": f"Response for {resp_code_enum.name}",
            "content": {
                content_type: {
                    "schema": {},
                },
            },
        },
    }
    # Default to using the schema directly in the file
    schema_value = schema["items"] if "items" in schema and schema["type"] != "array" else schema

    # if a component name is provided, use that to reference it
    if comp_name:
        schema_value = f"#/components/schemas/{comp_name}"
    if attr_name:
        # schema_value = f"#/components/schemas/{comp_name}/properties/{attr_name}"
        schema_value = (
            schema["items"] if "items" in schema and schema["type"] != "array" else schema
        )
        responses[resp_code_enum.value]["content"][content_type]["schema"] = schema_value
        return responses

    responses[resp_code_enum.value]["content"][content_type]["schema"]["$ref"] = schema_value
    if is_list:
        responses[resp_code_enum.value]["content"][content_type]["schema"] = {
            "type": "array",
            "items": {"$ref": schema_value},
        }

    return responses


def get_method_op(
    path: str,
    method: str,
    schema: dict,
    desc: str = None,
    comp_name: str = None,
    attr_name: str = None,
    is_list: bool = None,
):
    """Get the specified method seciton for the paths."""
    if not desc:
        desc = f"{method} operation for {path}"
    content_type = spec_base.DEFAULT_CONTENT_TYPE
    opr = {
        "description": desc,
        "operationId": spec_base.get_opid(path, method),
    }

    # Now set the schema for responses
    _LOGGER.debug(f"method: {method}")
    _LOGGER.debug(f"schema: {schema}")
    _LOGGER.debug(f"is_list: {is_list}")
    opr["responses"] = get_responses(
        method,
        schema,
        content_type,
        comp_name=comp_name,
        attr_name=attr_name,
        is_list=is_list,
    )

    if method == "post":
        request_schema = (
            copy.deepcopy(schema["items"]) if "items" in schema else copy.deepcopy(schema)
        )
        if (
            http.client.CREATED in opr["responses"]
            and "$ref" in opr["responses"][http.client.CREATED]["content"][content_type]["schema"]
        ):
            request_schema = opr["responses"][http.client.CREATED]["content"][content_type][
                "schema"
            ]

        if "descriptions" in request_schema:
            del request_schema["descriptions"]

        opr["requestBody"] = {
            "description": f"The request body for {path}",
            "required": True,
            "content": {
                spec_base.DEFAULT_CONTENT_TYPE: {
                    "schema": request_schema,
                },
            },
        }

    return opr


def get_params(
    baseurl: str,
    method: str,
    schema: dict,
    keys: list = None,
    param_schema: dict = None,
):
    """Get the parameters for this method."""
    parameters = []

    # Handle query params
    if "query_params" in schema:
        for param in copy.deepcopy(schema["query_params"]):
            _LOGGER.debug(f"param: {param}")
            methods = param.get("methods", [])
            _LOGGER.debug(f"methods: {methods}")
            if methods:
                del param["methods"]
            if methods and method not in methods:
                continue
            parameters.append(
                {
                    "name": param["name"],
                    "in": "query",
                    "required": param.get("required", False),
                    "schema": param.get("schema", {"type": "string"}),
                }
            )

    # Handle path params
    _LOGGER.debug(f"keys: {keys}")
    if keys:
        for key in keys:
            key_name = key["name"]
            if key_name not in baseurl:
                continue
            parameters.append(
                {
                    "name": key_name,
                    "in": "path",
                    "required": True,
                    "schema": param_schema or {"type": "string"},
                }
            )

    return parameters


def add_resource_methods(
    rsrc_name: str,
    schema: dict,
    baseurl: str,
    paths: dict,
    keys: list = None,
    default_query_params: dict = None,
):
    """Add resource level methods to the paths.

    :param str rsrc_name: the resource name
    :param dict schema: the schema for this resource name
    :param str baseurl: the baseurl to use for paths
    :param dict paths: the paths
    :param list keys: the keys for the instance of this resource
    :param dict default_query_params: the paths
    """
    paths[baseurl] = {}
    rsrc_methods = schema.get("methods", [])
    rsrc_descs = {}
    if "descriptions" in schema:
        rsrc_descs = copy.deepcopy(schema.get("descriptions", {}))
        del schema["descriptions"]

    for method in RSRC_HTTP_METHODS:
        if rsrc_methods and method not in rsrc_methods:
            _LOGGER.info(
                f"Skipping the definition of {method} in resource generation, "
                "as it is not in the defined methods requested"
            )
            continue
        paths[baseurl][method] = get_method_op(
            baseurl,
            method,
            schema,
            desc=rsrc_descs.get(method),
            comp_name=rsrc_name,
            is_list=(method == "get"),
        )
        paths[baseurl][method]["tags"] = [rsrc_name]

        # Add parameters
        params = get_params(baseurl, method, schema, keys=keys)
        if default_query_params:
            params.extend(default_query_params)
        _LOGGER.debug(f"params: {params}")
        paths[baseurl][method]["parameters"] = params

    return paths


def add_instance_methods(
    rsrc_name: str,
    schema: dict,
    baseurl: str,
    paths: dict,
    keys: list = None,
):
    """Add the instance methods to the paths.

    :param str rsrc_name: the resource name
    :param dict schema: the schema for this resource name
    :param str baseurl: the baseurl to use for paths
    :param list keys: the keys for the instance of this resource
    :param dict paths: the paths
    """
    rsrc_methods = schema.get("methods", [])
    rsrc_inst_descs = {}
    if "descriptions" in schema:
        rsrc_inst_descs = copy.deepcopy(schema.get("descriptions", {}))
        del schema["descriptions"]

    paths[baseurl] = {}
    for method in RSRC_INST_HTTP_METHODS:
        if rsrc_methods and method not in rsrc_methods:
            _LOGGER.info(
                f"Skipping the definition of {method} in resource instance generation, "
                "as it is not in the defined methods requested"
            )
            continue
        paths[baseurl][method] = get_method_op(
            baseurl,
            method,
            schema,
            desc=rsrc_inst_descs.get(method),
            comp_name=rsrc_name,
        )

        # Add parameters
        params = get_params(baseurl, method, schema, keys=keys)
        _LOGGER.debug(f"params: {params}")
        paths[baseurl][method]["parameters"] = params

        # Add tags
        if "tags" in paths[baseurl][method]:
            paths[baseurl][method]["tags"].append(rsrc_name)
        else:
            paths[baseurl][method]["tags"] = [rsrc_name]
        _LOGGER.debug(f"paths[baseurl][{method}]: {paths[baseurl][method]}")


def add_instance_attr_methods(
    rsrc_name: str,
    schema: dict,
    baseurl: str,
    paths: dict,
    keys: list = None,
    default_query_params: dict = None,
    components: dict = None,
):
    """Add the instance attr methods to the paths.

    :param str rsrc_name: the resource name
    :param dict schema: the schema for this resource name
    :param str baseurl: the baseurl to use for paths
    :param list keys: the keys for the instance of this resource
    :param dict paths: the paths
    :param dict default_query_params: the paths
    """
    rsrc_methods = schema.get("methods", [])
    for prop in schema["items"]["properties"]:
        path = "/".join([baseurl, prop])
        _LOGGER.debug(f"path: {path}")
        prop_schema = schema["items"]["properties"][prop]

        if "expose" in prop_schema and not prop_schema["expose"]:
            continue

        paths[path] = {}
        for method in RSRC_ATTR_HTTP_METHODS:
            if rsrc_methods and method not in rsrc_methods:
                _LOGGER.info(
                    f"Skipping the definition of {method} in resource instance attribute generation, "
                    "as it is not in the defined methods requested"
                )
                continue
            inst_attr_op = get_method_op(
                path, method, prop_schema, comp_name=rsrc_name, attr_name=prop
            )
            _LOGGER.debug(f"inst_attr_op: {inst_attr_op}")

            paths[path][method] = inst_attr_op

            # Add parameters
            params = get_params(baseurl, method, schema, keys=keys)
            _LOGGER.debug(f"params: {params}")
            paths[path][method]["parameters"] = params

            # Add tags
            if "tags" in paths[path][method]:
                paths[path][method]["tags"].append(rsrc_name)
            else:
                paths[path][method]["tags"] = [rsrc_name]
            _LOGGER.debug(f"paths[{path}][{method}]: {paths[path][method]}")

            # Recursively get paths for this property
            _LOGGER.debug(f"prop: {prop}")
            _LOGGER.debug(f"components: {yaml.dump(components['schemas'])}")
            if "schema" in prop_schema:
                if "descriptions" in prop_schema["schema"]:
                    del prop_schema["schema"]["descriptions"]
                if "descriptions" in prop_schema["schema"]["items"]:
                    del prop_schema["schema"]["items"]["descriptions"]

                components["schemas"][prop] = prop_schema["schema"]["items"]
                if (
                    rsrc_name in components["schemas"]
                    and prop in components["schemas"][rsrc_name]["properties"]
                ):
                    components["schemas"][rsrc_name]["properties"][prop] = {
                        "$ref": f"#/components/schemas/{prop}"
                    }

                get_paths(
                    prop,
                    prop_schema["schema"],
                    path,
                    paths,
                    keys=keys,
                    default_query_params=default_query_params,
                    components=components,
                )


def get_paths(
    rsrc_name: str,
    schema: dict,
    baseurl: str,
    paths: dict = None,
    keys: list = None,
    default_query_params: dict = None,
    components: dict = None,
):
    """Get the paths for resource."""
    if not paths:
        paths = {}

    if schema["type"] == "array" and not "key" in schema:
        raise spec_base.SchemaMissingAttribute("A 'key' is missing in schema {yaml.dump(schema)}")

    key = None
    if "key" in schema:
        key = schema["key"]
        has_param = next((item for item in keys if item["name"] == key["name"]), None)
        _LOGGER.debug(f"has_param: {has_param}")
        if not has_param:
            keys.append(key)

    # 1. Add methods to high-level baseurl
    add_resource_methods(
        rsrc_name,
        schema,
        baseurl,
        paths,
        keys=keys,
        default_query_params=default_query_params,
    )
    _LOGGER.debug(f"paths[{baseurl}]: {paths[baseurl]}")

    instance_baseurl = "/".join([baseurl, f"{{{key['name']}}}"])
    _LOGGER.debug(f"instance_baseurl: {instance_baseurl}")

    # 2. Add paths for each attribute
    add_instance_methods(
        rsrc_name,
        schema,
        instance_baseurl,
        paths,
        keys=keys,
    )

    # 3. Add attribute path for instance of this resource
    add_instance_attr_methods(
        rsrc_name,
        schema,
        instance_baseurl,
        paths,
        keys=keys,
        default_query_params=default_query_params,
        components=components,
    )

    return paths


# pylint: disable=too-many-locals
def generate(
    rsrc_data: list, title: str, desc: str, summary: str, version: str, prefix: str = None
):
    """Generate an OpenAPI spec based ont he resource data sent and other meta data."""
    components = {"schemas": {}}
    all_paths = {}
    for rsrc in rsrc_data:
        rsrc_name = rsrc["name"]
        baseurl = "/"
        if "version_in_path" in rsrc and rsrc["version_in_path"]:
            baseurl += f"v{rsrc['version']}/"
        baseurl += rsrc_name
        _LOGGER.debug(f"baseurl: {baseurl}")

        # Extract and set high-level resource component schema
        rschema = rsrc["schema"]
        comp_schema = copy.deepcopy(rschema["items"])
        if "descriptions" in comp_schema:
            del comp_schema["descriptions"]
        components["schemas"][rsrc_name] = comp_schema

        default_query_params = rsrc.get("default_query_params", [])
        _LOGGER.debug(f"default_query_params: {default_query_params}")

        paths = get_paths(
            rsrc_name,
            rschema,
            baseurl,
            paths={},
            keys=[],
            default_query_params=default_query_params,
            components=components,
        )
        _LOGGER.debug(f"paths: {paths}")
        all_paths.update(paths)

    servers = []
    if prefix:
        servers.append({"url": prefix})

    tmpl = spec_base.JINJA_ENV.get_template("openapi.jinja2")
    return tmpl.render(
        title=title,
        summary=summary,
        description=desc,
        version=version,
        components=components,
        paths=all_paths,
        servers=servers,
    )
