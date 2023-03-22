"""
Generate python Click based CLI from one or more resource schemas.
"""
import logging

from firestone.spec import _base as spec_base
from firestone.spec import openapi as spec_openapi

PARAM_TYPE_TO_ATTR_TYPE = {
    "string": "str",
    "integer": "int",
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


def params_to_attrs(params: list, required: list = None, keys: list = None):
    """Convert the params from OpenAPI spec to Click attributes."""
    if not required:
        required = []
    if not keys:
        keys = []
    _LOGGER.debug(f"params: {params}")
    _LOGGER.debug(f"keys: {keys}")

    attrs = []
    for param in params:
        _LOGGER.debug(f"param: {param}")
        param_schema = param.get("schema", param)
        param_type = param_schema.get("type", "string")
        cli_type = "str"

        # this means that this param/attribute is another object
        if param_type in ["object", "array"]:
            _LOGGER.info(f"{param['name']} is of type '{param_type}', processing special CLI type.")
            cli_type = "cli.FromJSON()"
            items_type = param_schema.get("items", {}).get("type", "string")
            _LOGGER.debug(f"cli_type: {cli_type}")
            _LOGGER.debug(f"items_type: {items_type}")
            if param_type == "array" and items_type != "object":
                _LOGGER.info(
                    f"{param['name']} has items of type '{items_type}', setting click option to cli.StrList"
                )
                cli_type = "cli.StrList"
        elif "enum" in param_schema:
            _LOGGER.info(f"{param['name']} is of type '{param_type}', creating click.Choice()")
            enums = '","'.join(param_schema["enum"])
            cli_type = f'click.Choice(["{enums}"])'
        else:
            _LOGGER.info(
                f"{param['name']} is of type: {param_type}, looking up type in PARAM_TYPE_TO_ATTR_TYPE"
            )
            cli_type = PARAM_TYPE_TO_ATTR_TYPE.get(param_type)

        param_name = param["name"]
        required_val = param_name in required
        attrs.append(
            {
                "argument": param_name in keys,
                "name": param_name,
                "description": param.get("description"),
                "type": cli_type,
                "required": param.get("required", required_val),
            }
        )
    return attrs


def get_resource_attrs(schema: dict, check_required: bool = None):
    """Get resource attributes."""
    props = schema.get("items", {}).get("properties", {})
    tmp_attrs = [{"name": attr, **(props[attr])} for attr in props]
    _LOGGER.debug(f"tmp_attrs: {tmp_attrs}")

    required = schema["items"].get("required", []) if check_required else []
    _LOGGER.debug(f"required: {required}")

    attrs = params_to_attrs(tmp_attrs, required)
    _LOGGER.debug(f"attrs: {attrs}")

    return attrs


def get_resource_ops(
    rsrc_name: str,
    schema: dict,
    baseurl: str,
    methods: list = None,
    descs: list = None,
    keys: list = None,
    default_query_params: dict = None,
):
    """Add resource level methods to the ops.

    :param str rsrc_name: the resource name
    :param dict schema: the schema for this resource name
    :param str baseurl: the baseurl to use for ops
    :param list methods: optional set of methods to create for
    :param list keys: the keys for the instance of this resource
    :param dict default_query_params: the ops
    """
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
        params = spec_openapi.get_params(baseurl, method, schema, keys=keys)
        if default_query_params:
            params.extend(default_query_params)
        _LOGGER.debug(f"params: {params}")

        attrs = params_to_attrs(params)

        if op_name == "create":
            check_required = True
            attrs = get_resource_attrs(schema, check_required)

        _LOGGER.debug(f"attrs: {attrs}")

        op["attrs"] = attrs

        ops.append(op)

    return ops


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

        op = {}
        op["name"] = op_name
        op["id"] = spec_base.get_opid(baseurl, method)
        op["description"] = descs.get(method, f"{op_name.capitalize()} operation for {rsrc_name}")

        params = spec_openapi.get_params(baseurl, method, schema, keys=keys)
        attrs = params_to_attrs(params, keys=[key["name"] for key in keys])

        if op_name == "update":
            attrs = get_resource_attrs(schema)

        _LOGGER.debug(f"attrs: {attrs}")

        op["attrs"] = attrs

        ops.append(op)

    return ops


def get_ops(
    rsrc: dict,
    baseurl: str,
    ops: dict = None,
    keys: list = None,
    default_query_params: dict = None,
):
    """Get the operations for this resource."""
    rsrc_name = rsrc["name"]
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

    # 1. Add operations to high-level baseurl
    ops["resource"] = get_resource_ops(
        rsrc_name,
        schema,
        baseurl,
        methods=methods.get("resource", {}),
        descs=descs.get("resource", {}),
        keys=keys,
        default_query_params=default_query_params,
    )

    instance_baseurl = "/".join([baseurl, f"{{{key['name']}}}"])
    _LOGGER.debug(f"instance_baseurl: {instance_baseurl}")

    # 2. Add paths for each attribute
    ops["instance"] = get_instance_ops(
        rsrc_name,
        schema,
        instance_baseurl,
        methods=methods.get("instance", {}),
        descs=descs.get("instance", {}),
        keys=keys,
    )

    return ops


# pylint: disable=too-many-locals
def generate(
    pkg: str, client_pkg: str, rsrc_data: list, title: str, desc: str, summary: str, version: str
):
    """Generate a Click based CLI script based on the resource data sent and other meta data."""
    rsrcs = []
    for rsrc in rsrc_data:
        rsrc_name = rsrc["name"]
        baseurl = "/"
        if "version_in_path" in rsrc and rsrc["version_in_path"]:
            baseurl += f"v{rsrc['version']}/"
        baseurl += rsrc_name
        _LOGGER.debug(f"baseurl: {baseurl}")

        default_query_params = rsrc.get("default_query_params", [])
        _LOGGER.debug(f"default_query_params: {default_query_params}")

        ops = get_ops(
            rsrc,
            baseurl,
            ops={},
            keys=[],
            default_query_params=default_query_params,
        )
        _LOGGER.debug(f"ops: {ops}")
        rsrcs.append(
            {
                "name": rsrc_name,
                "operations": ops,
            }
        )

    tmpl = spec_base.JINJA_ENV.get_template("main.py.jinja2")
    return tmpl.render(
        title=title,
        summary=summary,
        description=desc,
        version=version,
        pkg=pkg,
        client_pkg=client_pkg,
        rsrcs=rsrcs,
    )
