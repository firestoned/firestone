"""
Generate OpenAPI Spec >= 3.1
"""
import copy
import http.client
import logging

import jinja2

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


def get_mthod_op(path: str, method: str, schema: dict, desc: str = None):
    """Get the specified method seciton for the paths."""
    if not desc:
        desc = f"{method} operation for {path}"
    op = {
        "description": desc,
        "operationId": get_opid(path, method),
        "responses": {
            http.client.OK.value: {
                "description": http.client.OK.name,
                "content": {
                    "application/json": {
                        "schema": schema["items"] if "items" in schema else schema,
                    },
                },
            },
        },
    }

    if method == "head":
        del op["responses"]
    if method == "post":
        op["requestBody"] = {
            "description": f"The request body for {path}",
            "required": True,
            "content": {
                "application/json": {
                    "schema": schema["items"] if "items" in schema else schema,
                },
            },
        }
    if "query_params" not in schema:
        return op

    op["paramaters"] = []
    for param in copy.deepcopy(schema["query_params"]):
        _LOGGER.debug(f"param: {param}")
        methods = param.get("methods", [])
        _LOGGER.debug(f"methods: {methods}")
        if methods:
            del param["methods"]
        if methods and method not in methods:
            continue
        op["paramaters"].append(
            {
                "name": param["name"],
                "in": "query",
                "required": param.get("required", False),
                "schema": param.get("schema", "string"),
            }
        )
    # cleanup if no parameters due to methods set
    if not op["paramaters"]:
        del op["paramaters"]

    return op


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
            base_url, method, schema, rsrc_descs.get(method)
        )
        paths[base_url][method]["tags"] = [rsrc_name]
        _LOGGER.debug(f"paths[base_url][{method}]: {paths[base_url][method]}")

    # 2. Add paths for each attribtue
    if schema["type"] == "array" and not "key" in schema:
        raise MissingAttribute("A 'key' is missing in schema {yaml.dump(schema)}")

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
            instance_baseurl, method, schema, rsrc_inst_descs.get(method)
        )
        paths[instance_baseurl][method]["tags"] = [rsrc_name]
        _LOGGER.debug(
            f"paths[instance_baseurl][{method}]: {paths[instance_baseurl][method]}"
        )

    # 3. Add attribute path for instance of this resource
    for prop in schema["items"]["properties"]:
        path = "/".join([instance_baseurl, prop])
        _LOGGER.debug(f"path: {path}")
        inst_op = copy.deepcopy(paths[instance_baseurl][method])
        prop_schema = schema["items"]["properties"][prop]

        paths[path] = {}
        for method in RSRC_ATTR_HTTP_METHODS:
            if rsrc_methods and method not in rsrc_methods:
                _LOGGER.info(
                    f"Skipping the definition of {method} in resource instance attribute generation, "
                    "as it is not in the defined methods requested"
                )
                continue
            inst_attr_op = get_mthod_op(
                path, method, prop_schema
            )
            _LOGGER.debug(f"inst_attr_op: {inst_attr_op}")

            paths[path][method] = inst_attr_op
            paths[path][method]["tags"] = [rsrc_name]
            _LOGGER.debug(
                f"paths[path][{method}]: {paths[path][method]}"
            )

            # TODO test and add recursivness
            if "items" in prop_schema:
                get_paths(rsrc_name, prop_schema, path, paths)

    return paths


def generate(rsrc_data: list, title: str, desc: str, summary: str):
    """Generate an OpenAPI spec based ont he resource data sent and other meta data."""
    all_paths = {}
    for rd in rsrc_data:
        rsrc_name = rd["name"]
        base_url = "/"
        if rd["versionInPath"]:
            base_url += f"v{rd['version']}/"
        base_url += rsrc_name
        _LOGGER.debug(f"base_url: {base_url}")

        paths = get_paths(rsrc_name, rd["schema"], base_url, {})
        _LOGGER.debug(f"paths: {paths}")
        all_paths.update(paths)

    tmpl = _base.JINJA_ENV.get_template("openapi.jinja2")
    return tmpl.render(
        title=title,
        summary=summary,
        description=desc,
        components=[],
        paths=paths,
    )
