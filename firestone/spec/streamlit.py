# pylint: disable=duplicate-code
"""
Generate python streamlit WebUI from one or more resource schemas.
"""

import io
import json
import logging
import os

import jinja2

from firestone_lib import utils

from firestone.spec import _base as spec_base
from firestone.spec import openapi as spec_openapi

PARAM_TYPE_TO_ATTR_TYPE = {
    "string": "TextColumn",
    "integer": "NumberColumn",
    "boolean": "CheckboxColumn",
    "object": "JsonColumn",
    "array": "ListColumn",
    "enum": "SelectboxColumn",
}

_LOGGER = logging.getLogger(__name__)


def _get_op_name(method: str, top_level: bool) -> str:
    if method == "get" and top_level:
        return "list"
    if method == "get":
        return "get"
    if method == "post":
        return "create"
    if method in ["put", "patch"]:
        return "update"
    if method == "delete":
        return method

    return None


def params_to_attrs(params: list, required: list = None, key_names: list = None):
    """Convert the params from OpenAPI spec to Click attributes."""
    if not required:
        required = []
    if not key_names:
        key_names = []
    _LOGGER.debug(f"params: {params}")
    _LOGGER.debug(f"key_names: {key_names}")

    attrs = []
    for param in params:
        _LOGGER.debug(f"param: {param}")
        param_schema = param.get("schema", param)
        _LOGGER.debug(f"param_schema: {param_schema}")
        # Determine if this is an embeded object using `$ref`
        if "key" in param_schema and param_schema["type"] == "array":
            param_schema = param_schema["items"]
        param_type = param_schema.get("type", "string")
        _LOGGER.info(
            f"{param['name']} is of type: {param_type}, looking up type in PARAM_TYPE_TO_ATTR_TYPE"
        )
        col_type = PARAM_TYPE_TO_ATTR_TYPE.get(param_type, PARAM_TYPE_TO_ATTR_TYPE["string"])
        _LOGGER.debug(f"param_type: {param_type}")

        # this means that this param/attribute is another object
        attr_data = None
        if "enum" in param_schema:
            _LOGGER.info(f"{param['name']} is of type '{param_type}', creating click.Choice()")
            attr_data = json.dumps(param_schema["enum"])
            col_type = PARAM_TYPE_TO_ATTR_TYPE["enum"]

        param_name = param["name"]
        is_required = param_name in required
        _LOGGER.debug(f"param_name: {param_name}")
        _LOGGER.debug(f"key_names: {key_names}")

        attrs.append(
            {
                "name": param_name,
                "pretty_name": utils.split_capitalize(param_name),
                "description": param.get("description"),
                "type": col_type,
                "data": attr_data,
                "required": param.get("required", is_required),
                # TODO: support different formatting
                # "format": formatted_str,
            }
        )
    return attrs


def get_resource_attrs(
    schema: dict, params: dict = None, check_required: bool = None, key_names: list = None
):
    """Get resource attributes."""
    _LOGGER.debug(f"key_names: {key_names}")
    props = schema.get("items", {}).get("properties", {})
    tmp_attrs = [{"name": attr, **(props[attr])} for attr in props]
    if params:
        tmp_attrs.extend(params)
    _LOGGER.debug(f"tmp_attrs: {tmp_attrs}")

    required = schema["items"].get("required", []) if check_required else []
    _LOGGER.debug(f"required: {required}")

    attrs = params_to_attrs(tmp_attrs, required, key_names=key_names)
    _LOGGER.debug(f"attrs: {attrs}")

    return attrs


def get_instance_ops(
    rsrc_name: str,
    schema: dict,
    baseurl: str,
    methods: list = None,
    descs: list = None,
    keys: list = None,
):
    """Add the instance methods to the paths.

    :param str rsrc_name: the resource name
    :param dict schema: the schema for this resource name
    :param str baseurl: the baseurl to use for paths
    :param list methods: optional set of methods to create for
    :param list keys: the keys for the instance of this resource
    :param dict paths: the paths
    """
    _LOGGER.debug(f"keys: {keys}")
    ops = []
    top_level = False
    for method in spec_openapi.RSRC_INST_HTTP_METHODS:
        if methods and method not in methods:
            _LOGGER.info(
                f"Skipping the definition of {method} in resource instance generation, "
                "as it is not in the defined methods requested"
            )
            continue

        op_name = _get_op_name(method, top_level)
        if not op_name:
            continue
        _LOGGER.info(f"Getting streamlit attributes for {op_name}")

        op = {}
        op["name"] = op_name
        op["id"] = spec_base.get_opid(baseurl, method)
        op["description"] = descs.get(method, f"{op_name.capitalize()} operation for {rsrc_name}")

        params = spec_openapi.get_params(baseurl, method, schema, keys=keys)
        _LOGGER.debug(f"params: {params}")

        key_names = [key["name"] for key in keys]
        _LOGGER.debug(f"key_names: {key_names}")
        attrs = params_to_attrs(params, key_names=key_names)

        if op_name == "update":
            attrs = get_resource_attrs(schema, params=params, key_names=key_names)

        _LOGGER.debug(f"attrs: {attrs}")

        op["attrs"] = attrs

        ops.append(op)

    return ops


def get_resource_ops(
    rsrc_name: str,
    schema: dict,
    baseurl: str,
    methods: list = None,
    descs: list = None,
    keys: list = None,
):
    """Add resource level methods to the ops.

    :param str rsrc_name: the resource name
    :param dict schema: the schema for this resource name
    :param str baseurl: the baseurl to use for ops
    :param list methods: optional set of methods to create for
    :param list keys: the keys for the instance of this resource
    """
    _LOGGER.debug(f"keys: {keys}")
    ops = []

    top_level = True
    for method in spec_openapi.RSRC_HTTP_METHODS:
        if methods and method not in methods:
            _LOGGER.info(
                f"Skipping the definition of {method} in resource generation, "
                "as it is not in the defined methods requested"
            )
            continue

        op_name = _get_op_name(method, top_level)
        if not op_name:
            continue

        op = {}
        op["name"] = op_name
        op["id"] = spec_base.get_opid(baseurl, method)
        op["description"] = descs.get(method, f"{op_name.capitalize()} operation for {rsrc_name}")

        # Add params and attributes
        params = []
        attrs = params_to_attrs(params)

        if op_name == "create":
            check_required = True
            attrs = get_resource_attrs(schema, check_required=check_required)
        _LOGGER.debug(f"attrs: {attrs}")

        op["attrs"] = attrs

        ops.append(op)

    return ops


def get_ops(
    rsrc: dict,
    baseurl: str,
    ops: dict = None,
    keys: list = None,
):
    """Get the operations for this resource."""
    rsrc_name = rsrc["kind"]
    schema = rsrc["schema"]
    methods = rsrc.get("methods", {})
    descs = rsrc.get("descriptions", {})

    if not ops:
        ops = {}

    if schema["type"] == "array" and not "key" in schema:
        raise spec_base.SchemaMissingAttribute("A 'key' is missing in schema {yaml.dump(schema)}")

    key = None
    if "key" in schema:
        key = schema["key"]
        has_param = next((item for item in keys if item["name"] == key["name"]), None)
        _LOGGER.debug(f"has_param: {has_param}")
        if not has_param:
            keys.append(key)

    _LOGGER.debug(f"keys: {keys}")

    # 1. Add operations to high-level baseurl
    ops["resource"] = get_resource_ops(
        rsrc_name,
        schema,
        baseurl,
        methods=methods.get("resource", {}),
        descs=descs.get("resource", {}),
        keys=keys,
    )

    instance_baseurl = "/".join([baseurl, f"{{{key['name']}}}"])
    _LOGGER.debug(f"instance_baseurl: {instance_baseurl}")

    # 2. Get instance operations
    ops["instance"] = get_instance_ops(
        rsrc_name,
        schema,
        instance_baseurl,
        methods=methods.get("instance", {}),
        descs=descs.get("instance", {}),
        keys=keys,
    )

    return ops


# pylint: disable=too-many-locals,too-many-arguments
def generate(
    rsrc_data: list,
    title: str,
    desc: str,
    summary: str,
    version: str,
    backend_url: str = None,
    as_modules: bool = False,
    template: str = None,
    col_mappings: dict = None,
):
    """Generate a streamlit based WebUI script based on the resource data sent and other meta data."""
    if not col_mappings:
        col_mappings = {}
    _LOGGER.debug(f"col_mappings: {col_mappings}")

    rsrcs = []
    for rsrc in rsrc_data:
        rsrc_name = rsrc["kind"]
        baseurl = "/"
        if rsrc.get("versionInPath", False):
            baseurl += f"v{rsrc['apiVersion']}/"
        baseurl += rsrc_name
        _LOGGER.debug(f"baseurl: {baseurl}")

        ops = get_ops(
            rsrc,
            baseurl,
            ops={},
            keys=[],
        )
        _LOGGER.debug(f"ops: {ops}")
        rsrcs.append(
            {
                "name": rsrc_name,
                "key": rsrc["schema"]["key"],
                "pretty_name": utils.split_capitalize(rsrc_name),
                "baseurl": baseurl,
                "operations": ops,
                "col_mapping": col_mappings.get(rsrc_name),
            }
        )

    _LOGGER.info(f"rsrcs: {rsrcs}")

    tmpl = None
    if template and os.path.exists(template):
        _LOGGER.info(f"Using custom template from {template}")
        with io.open(template, "r", encoding="utf-8") as fh:
            tmpl_str = "".join(fh.readlines())

            tmpl = jinja2.Environment(
                loader=jinja2.BaseLoader,
                extensions=["jinja2.ext.loopcontrols"],
            ).from_string(tmpl_str)

    if not as_modules:
        if not tmpl:
            tmpl = spec_base.JINJA_ENV.get_template("streamlit.py.jinja2")
        return tmpl.render(
            title=title,
            summary=summary,
            description=desc,
            version=version,
            rsrcs=rsrcs,
            backend_url=backend_url,
        )

    rendered_rsrcs = {}
    for rsrc in rsrcs:
        if not tmpl:
            tmpl = spec_base.JINJA_ENV.get_template("streamlit_page.py.jinja2")
        rendered = tmpl.render(
            title=title,
            summary=summary,
            description=desc,
            version=version,
            rsrc=rsrc,
            backend_url=backend_url,
        )
        rendered_rsrcs[rsrc["name"]] = rendered

    return rendered_rsrcs
