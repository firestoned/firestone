"""
Generate OpenAPI 3.0 Spec
"""
import copy
import http.client
import logging

from firestone.spec import _base

# This is a list of all HTTP methods supported on high-level resource base
RSRC_HTTP_METHODS = ["delete", "get", "head", "patch", "post"]

# This is a list of all HTTP methods supported on an instance of a resource
RSRC_INST_HTTP_METHODS = ["delete", "get", "head", "patch", "put"]

# This is a list of all HTTP methods supported on attributes of an instance of a resource
RSRC_ATTR_HTTP_METHODS = ["delete", "get", "head", "put"]

_LOGGER = logging.getLogger(__name__)


class SchemaMissingAttribute(Exception):
    """Schema is missing an attribute."""


def get_opid(path: str, method: str):
    """Get a unique operationId given the patha nd method."""
    opid = path[1:].replace("/", "_")
    opid = opid.replace("{", "")
    opid = opid.replace("}", "")
    return f"{opid}_{method}"


def get_responses(
    method: str,
    schema: dict,
    content_type: str,
    comp_name: str = None,
    is_list: bool = None,
):
    """Set schema for a given oepration type."""
    if method == "head":
        return None

    resp_code_enum = http.client.OK
    if method == "post":
        resp_code_enum = http.client.CREATED

    responses = {
        resp_code_enum.value: {
            "description": resp_code_enum.name,
            "content": {
                content_type: {
                    "schema": {},
                },
            },
        },
    }
    # Default to using the schema directly in the file
    schema_value = schema["items"] if "items" in schema else schema

    # if a component name is provided, use that to reference it
    if comp_name:
        schema_value = f"#/components/schemas/{comp_name}"

    responses[resp_code_enum.value]["content"][content_type]["schema"]["$ref"] = schema_value
    if is_list:
        responses[resp_code_enum.value]["content"][content_type]["schema"] = {
            "type": "array",
            "items": {"$ref": schema_value},
        }

    return responses


def get_mthod_op(
    path: str,
    method: str,
    schema: dict,
    desc: str = None,
    comp_name: str = None,
    is_list: bool = None,
):
    """Get the specified method seciton for the paths."""
    if not desc:
        desc = f"{method} operation for {path}"
    content_type = "application/json"
    opr = {
        "description": desc,
        "operationId": get_opid(path, method),
    }

    # Now set the schema for responses
    _LOGGER.debug(f"method: {method}")
    opr["responses"] = get_responses(
        method,
        schema,
        content_type,
        comp_name=comp_name,
        is_list=is_list,
    )

    if method == "post":
        opr["requestBody"] = {
            "description": f"The request body for {path}",
            "required": True,
            "content": {
                "application/json": {
                    "schema": schema["items"] if "items" in schema else schema,
                },
            },
        }
    if "query_params" not in schema:
        return opr

    opr["paramaters"] = []
    for param in copy.deepcopy(schema["query_params"]):
        _LOGGER.debug(f"param: {param}")
        methods = param.get("methods", [])
        _LOGGER.debug(f"methods: {methods}")
        if methods:
            del param["methods"]
        if methods and method not in methods:
            continue
        opr["paramaters"].append(
            {
                "name": param["name"],
                "in": "query",
                "required": param.get("required", False),
                "schema": param.get("schema", "string"),
            }
        )
    # cleanup if no parameters due to methods set
    if not opr["paramaters"]:
        del opr["paramaters"]

    return opr


def get_paths(rsrc_name: str, schema: dict, base_url: str, paths: dict):
    """Get tshe paths for resource."""
    # 1. Add methods to high-level baseurl
    paths[base_url] = {}
    rsrc_methods = schema.get("methods", [])
    rsrc_descs = schema.get("descriptions", {})
    for method in RSRC_HTTP_METHODS:
        if rsrc_methods and method not in rsrc_methods:
            _LOGGER.info(
                f"Skipping the definition of {method} in resource generation, "
                "as it is not in the defined methods requested"
            )
            continue
        paths[base_url][method] = get_mthod_op(
            base_url,
            method,
            schema,
            desc=rsrc_descs.get(method),
            comp_name=rsrc_name,
            is_list=(method == "get"),
        )
        paths[base_url][method]["tags"] = [rsrc_name]
        _LOGGER.debug(f"paths[base_url][{method}]: {paths[base_url][method]}")

    # 2. Add paths for each attribtue
    if schema["type"] == "array" and not "key" in schema:
        raise SchemaMissingAttribute("A 'key' is missing in schema {yaml.dump(schema)}")

    key = schema["key"]["name"]
    instance_baseurl = "/".join([base_url, f"{{{key}}}"])
    _LOGGER.debug(f"instance_baseurl: {instance_baseurl}")
    rsrc_inst_descs = schema["items"].get("descriptions", {})

    paths[instance_baseurl] = {}
    for method in RSRC_INST_HTTP_METHODS:
        if rsrc_methods and method not in rsrc_methods:
            _LOGGER.info(
                f"Skipping the definition of {method} in resource instance generation, "
                "as it is not in the defined methods requested"
            )
            continue
        paths[instance_baseurl][method] = get_mthod_op(
            instance_baseurl, method, schema,
            desc=rsrc_inst_descs.get(method),
            comp_name=rsrc_name,
        )
        paths[instance_baseurl][method]["tags"] = [rsrc_name]
        _LOGGER.debug(f"paths[instance_baseurl][{method}]: {paths[instance_baseurl][method]}")

    # 3. Add attribute path for instance of this resource
    for prop in schema["items"]["properties"]:
        path = "/".join([instance_baseurl, prop])
        _LOGGER.debug(f"path: {path}")
        # inst_op = copy.deepcopy(paths[instance_baseurl][method])
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
            inst_attr_op = get_mthod_op(path, method, prop_schema)
            _LOGGER.debug(f"inst_attr_op: {inst_attr_op}")

            paths[path][method] = inst_attr_op
            paths[path][method]["tags"] = [rsrc_name]
            _LOGGER.debug(f"paths[path][{method}]: {paths[path][method]}")

            # TODO test and add recursivness
            if "items" in prop_schema:
                get_paths(rsrc_name, prop_schema, path, paths)

    return paths


def generate(rsrc_data: list, title: str, desc: str, summary: str):
    """Generate an OpenAPI spec based ont he resource data sent and other meta data."""
    components = {"schemas": {}}
    all_paths = {}
    for rsrc in rsrc_data:
        rsrc_name = rsrc["name"]
        base_url = "/"
        if rsrc["versionInPath"]:
            base_url += f"v{rsrc['version']}/"
        base_url += rsrc_name
        _LOGGER.debug(f"base_url: {base_url}")

        # Extract and set high-level resource component schema
        rschema = rsrc["schema"]
        comp_schema = copy.deepcopy(rschema["items"])
        if "descriptions" in comp_schema:
            del comp_schema["descriptions"]
        components["schemas"][rsrc_name] = comp_schema

        paths = get_paths(rsrc_name, rschema, base_url, {})
        _LOGGER.debug(f"paths: {paths}")
        all_paths.update(paths)

    tmpl = _base.JINJA_ENV.get_template("openapi.jinja2")
    return tmpl.render(
        title=title,
        summary=summary,
        description=desc,
        components=components,
        paths=all_paths,
    )
