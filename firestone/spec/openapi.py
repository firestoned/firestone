"""
Generate OpenAPI 3.0 Spec
"""

# TODO: fix dupe code
# pylint: disable=duplicate-code

import copy
import http.client
import logging

from firestone.spec import _base as spec_base

DEFAULT_VERSION = "3.0.0"

# This is a list of all HTTP methods supported on high-level resource base
RSRC_HTTP_METHODS = ["delete", "get", "head", "patch", "post"]

# This is a list of all HTTP methods supported on an instance of a resource
RSRC_INST_HTTP_METHODS = ["delete", "get", "head", "patch", "put"]

# This is a list of all HTTP methods supported on attributes of an instance of a resource
RSRC_ATTR_HTTP_METHODS = ["delete", "get", "head", "put"]

_LOGGER = logging.getLogger(__name__)

# TODO add support for JSON Patch: https://www.jvt.me/posts/2022/05/29/openapi-json-patch/


def _dedup_params(params: list):
    seen = set()
    new_list = []
    for param in params:
        name = param["name"]
        if name not in seen:
            seen.add(name)
            new_list.append(param)

    return new_list


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


def _get_comp_name(rsrc_name: str, method: str):
    comp_name = rsrc_name if not rsrc_name.endswith("s") else rsrc_name[:-1]
    if method == "post":
        comp_name = f"Create{comp_name.capitalize()}"
    if method == "put":
        comp_name = f"Update{comp_name.capitalize()}"

    return comp_name


def get_method_op(
    path: str,
    method: str,
    schema: dict,
    desc: str = None,
    comp_name: str = None,
    attr_name: str = None,
    is_list: bool = None,
):
    """Get the specified method section for the paths."""
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
    _LOGGER.debug(f"comp_name: {comp_name}")
    _LOGGER.debug(f"attr_name: {attr_name}")
    _LOGGER.debug(f"is_list: {is_list}")
    opr["responses"] = get_responses(
        method,
        schema,
        content_type,
        comp_name=comp_name,
        attr_name=attr_name,
        is_list=is_list,
    )

    request_schema = None
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
    elif method == "put":
        _LOGGER.debug(f"Getting {method} operation")
        request_schema = copy.deepcopy(schema)
        _LOGGER.debug(f"request_schema: {request_schema}")
        if comp_name and not attr_name:
            request_schema = {"$ref": f"#/components/schemas/{comp_name}"}
    _LOGGER.debug(f"request_schema: {request_schema}")

    if request_schema:
        if "descriptions" in request_schema:
            del request_schema["descriptions"]
        if "key" in request_schema:
            del request_schema["key"]
        if "methods" in request_schema:
            del request_schema["methods"]
        if "query_params" in request_schema:
            del request_schema["query_params"]

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
            new_params = {
                "name": param["name"],
                "in": "query",
                "required": param.get("required", False),
                "schema": param.get("schema", {"type": "string"}),
                "description": param.get("description"),
            }
            if param.get("default") is not None:
                new_params["default"] = param.get("default")

            parameters.append(new_params)

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


# pylint: disable=too-many-arguments
def add_resource_methods(
    rsrc_name: str,
    schema: dict,
    baseurl: str,
    paths: dict,
    methods: list = None,
    descs: dict = None,
    keys: list = None,
    default_query_params: dict = None,
    orig_rsrc_name: str = None,
    security: dict = None,
):
    """Add resource level methods to the paths.

    :param str rsrc_name: the resource name
    :param dict schema: the schema for this resource name
    :param str baseurl: the baseurl to use for paths
    :param dict paths: the paths
    :param list keys: the keys for the instance of this resource
    :param dict default_query_params: the paths
    """
    if not descs:
        descs = {}

    paths[baseurl] = {}

    for method in RSRC_HTTP_METHODS:
        if methods and method not in methods:
            _LOGGER.info(
                f"Skipping the definition of {method} in resource generation, "
                "as it is not defined in methods.resource requested"
            )
            continue

        comp_name = _get_comp_name(rsrc_name, method)
        _LOGGER.debug(f"comp_name: {comp_name}")

        paths[baseurl][method] = get_method_op(
            baseurl,
            method,
            schema,
            desc=descs.get(method),
            comp_name=comp_name,
            is_list=(method == "get"),
        )
        paths[baseurl][method]["tags"] = [orig_rsrc_name or rsrc_name]

        # Add security if required
        if security and method in security.get("resource", []):
            security_scheme = list(security["scheme"].keys())[0]
            paths[baseurl][method]["security"] = [{security_scheme: []}]

        # Add parameters
        params = get_params(baseurl, method, schema, keys=keys)
        if default_query_params:
            params.extend(default_query_params)
            params = _dedup_params(params)
        _LOGGER.debug(f"params: {params}")
        paths[baseurl][method]["parameters"] = params

    return paths


def add_instance_methods(
    rsrc_name: str,
    schema: dict,
    baseurl: str,
    paths: dict,
    methods: list = None,
    descs: dict = None,
    keys: list = None,
    orig_rsrc_name: str = None,
    security: dict = None,
):
    """Add the instance methods to the paths.

    :param str rsrc_name: the resource name
    :param dict schema: the schema for this resource name
    :param str baseurl: the baseurl to use for paths
    :param list keys: the keys for the instance of this resource
    :param dict paths: the paths
    """
    if not descs:
        descs = {}

    paths[baseurl] = {}
    for method in RSRC_INST_HTTP_METHODS:
        _LOGGER.debug(f"baseurl: {baseurl}")
        if methods and method not in methods:
            _LOGGER.info(
                f"Skipping the definition of {method} in resource instance generation, "
                "as it is not defined in methods.instance requested"
            )
            continue

        comp_name = _get_comp_name(rsrc_name, method)
        _LOGGER.debug(f"comp_name: {comp_name}")

        paths[baseurl][method] = get_method_op(
            baseurl,
            method,
            schema,
            desc=descs.get(method),
            comp_name=comp_name,
        )

        # Add security if required
        if security and method in security.get("instance", []):
            security_scheme = list(security["scheme"].keys())[0]
            paths[baseurl][method]["security"] = [{security_scheme: []}]

        # Add parameters
        params = get_params(baseurl, method, schema, keys=keys)
        _LOGGER.debug(f"params: {params}")
        paths[baseurl][method]["parameters"] = params

        # Add tags
        paths[baseurl][method]["tags"] = [orig_rsrc_name or rsrc_name]
        _LOGGER.debug(f"paths[baseurl][{method}]: {paths[baseurl][method]}")


# pylint: disable=too-many-locals
def add_instance_attr_methods(
    rsrc_name: str,
    schema: dict,
    baseurl: str,
    paths: dict,
    methods: dict = None,
    keys: list = None,
    default_query_params: dict = None,
    components: dict = None,
    orig_rsrc_name: str = None,
    security: dict = None,
):
    """Add the instance attr methods to the paths.

    :param str rsrc_name: the resource name
    :param dict schema: the schema for this resource name
    :param str baseurl: the baseurl to use for paths
    :param list keys: the keys for the instance of this resource
    :param dict paths: the paths
    :param dict default_query_params: the paths
    """
    inst_methods = methods.get("instance_attrs", [])
    for prop in schema["items"]["properties"]:
        path = "/".join([baseurl, prop])
        _LOGGER.debug(f"path: {path}")
        prop_schema = schema["items"]["properties"][prop]

        if "expose" in prop_schema and not prop_schema["expose"]:
            continue

        paths[path] = {}
        for method in RSRC_ATTR_HTTP_METHODS:
            if inst_methods and method not in inst_methods:
                _LOGGER.info(
                    f"Skipping the definition of {method} in resource instance attribute generation, "
                    "as it is not in the defined methods requested"
                )
                continue

            comp_name = rsrc_name if not rsrc_name.endswith("s") else rsrc_name[:-1]
            inst_attr_op = get_method_op(
                path, method, prop_schema, comp_name=comp_name, attr_name=prop
            )

            # Add security if required
            if security and method in security.get("instance_attrs", []):
                security_scheme = list(security["scheme"].keys())[0]
                inst_attr_op["security"] = [{security_scheme: []}]

            _LOGGER.debug(f"inst_attr_op: {inst_attr_op}")

            paths[path][method] = inst_attr_op

            # Add parameters
            params = get_params(baseurl, method, schema, keys=keys)
            _LOGGER.debug(f"params: {params}")
            paths[path][method]["parameters"] = params

            # Add tags
            paths[path][method]["tags"] = [orig_rsrc_name or rsrc_name]
            _LOGGER.debug(f"paths[{path}][{method}]: {paths[path][method]}")

            # Recursively get paths for this property
            _LOGGER.debug(f"prop: {prop}")
            if "schema" in prop_schema:
                if "descriptions" in prop_schema["schema"]:
                    del prop_schema["schema"]["descriptions"]
                if "descriptions" in prop_schema["schema"]["items"]:
                    del prop_schema["schema"]["items"]["descriptions"]

                components = add_rsrc_components(
                    components, prop, methods, prop_schema["schema"], security
                )
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
                    orig_rsrc_name=orig_rsrc_name,
                    security=security,
                )


def get_paths(
    rsrc_name: str,
    rsrc: dict,
    baseurl: str,
    paths: dict = None,
    keys: list = None,
    default_query_params: dict = None,
    components: dict = None,
    orig_rsrc_name: str = None,
    security: dict = None,
):
    """Get the paths for resource."""
    # Extract and set high-level resource component schema
    _LOGGER.debug(f"rsrc: {rsrc}")
    schema = rsrc["schema"] if "schema" in rsrc else rsrc
    methods = rsrc.get("methods", {})
    descs = rsrc.get("descriptions", {})

    if not paths:
        paths = {}

    if schema["type"] == "array" and schema["items"]["type"] == "object" and not "key" in schema:
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
        methods=methods.get("resource", {}),
        descs=descs.get("resource", {}),
        keys=keys,
        default_query_params=default_query_params,
        orig_rsrc_name=orig_rsrc_name,
        security=security,
    )
    _LOGGER.debug(f"paths[{baseurl}]: {paths[baseurl]}")

    instance_baseurl = "/".join([baseurl, f"{{{key['name']}}}"])
    _LOGGER.debug(f"instance_baseurl: {instance_baseurl}")

    # 2. Add paths for each attribute
    if methods.get("instance"):
        add_instance_methods(
            rsrc_name,
            schema,
            instance_baseurl,
            paths,
            methods=methods.get("instance", {}),
            descs=descs.get("instance", {}),
            keys=keys,
            orig_rsrc_name=orig_rsrc_name,
            security=security,
        )

    # 3. Add attribute path for instance of this resource
    if methods.get("instance_attrs"):
        add_instance_attr_methods(
            rsrc_name,
            schema,
            instance_baseurl,
            paths,
            methods=methods,
            keys=keys,
            default_query_params=default_query_params,
            components=components,
            orig_rsrc_name=orig_rsrc_name,
            security=security,
        )

    return paths


def add_rsrc_components(
    components: dict, rsrc_name: str, methods: dict, schema: dict, security: dict
):
    """Get the components for this resource."""
    comp_name = rsrc_name if not rsrc_name.endswith("s") else rsrc_name[:-1]

    # Reosurce level component, without required
    comp_schema = copy.deepcopy(schema["items"])
    if "descriptions" in comp_schema:
        del comp_schema["descriptions"]

    components["schemas"][comp_name] = comp_schema

    required = schema["items"].get("required", [])
    if required:
        del components["schemas"][comp_name]["required"]

    rscr_methods = methods.get("resource", [])
    rscr_inst_methods = methods.get("instance", [])
    _LOGGER.debug(f"rscr_methods: {rscr_methods}")
    _LOGGER.debug(f"rscr_inst_methods: {rscr_inst_methods}")

    if security and "scheme" in security:
        components["securitySchemes"] = security.get("scheme", {})

    # Create resource model
    if "post" in rscr_methods or "post" in rscr_inst_methods:
        create_key = f"Create{comp_name.capitalize()}"
        _LOGGER.info(f"Adding {create_key} to components")
        components["schemas"][create_key] = {
            "allOf": [
                {"$ref": f"#/components/schemas/{comp_name}"},
                {"type": "object"},
            ]
        }

        if required:
            components["schemas"][create_key]["allOf"][1]["required"] = required

    # Update resource model
    if "put" in rscr_methods or "put" in rscr_inst_methods:
        update_key = f"Update{comp_name.capitalize()}"
        _LOGGER.info(f"Adding {update_key} to components")
        components["schemas"][update_key] = {
            "allOf": [
                {"$ref": f"#/components/schemas/{comp_name}"},
                {"type": "object"},
            ]
        }

    return components


# pylint: disable=too-many-locals
def generate(
    rsrc_data: list,
    title: str,
    desc: str,
    summary: str,
    version: str,
    prefix: str = None,
    openapi_version: str = None,
):
    """Generate an OpenAPI spec based on the resource data sent and other meta data."""
    components = {"schemas": {}}
    all_paths = {}
    for rsrc in rsrc_data:
        rsrc_name = rsrc["kind"]
        baseurl = "/"
        if rsrc.get("versionInPath", False):
            baseurl += f"v{rsrc['apiVersion']}/"
        baseurl += rsrc_name
        _LOGGER.debug(f"baseurl: {baseurl}")

        # Extract authc or security from the header
        security = rsrc.get("security", {})

        # Extract and set high-level resource component schema
        methods = rsrc.get("methods", {})
        components = add_rsrc_components(components, rsrc_name, methods, rsrc["schema"], security)
        _LOGGER.debug(f"components: {components['schemas']}")
        if (
            security
            and "resource" not in security
            and "instance" not in security
            and "instance_attrs" not in security
        ):
            security_scheme = list(security["scheme"].keys())[0]
            rsrc["security"] = [{security_scheme: []}]

        default_query_params = rsrc.get("default_query_params", [])
        _LOGGER.debug(f"default_query_params: {default_query_params}")

        paths = get_paths(
            rsrc["kind"],
            rsrc,
            baseurl,
            paths={},
            keys=[],
            default_query_params=default_query_params,
            components=components,
            orig_rsrc_name=rsrc_name,
            security=security,
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
        openapi_version=openapi_version,
    )
