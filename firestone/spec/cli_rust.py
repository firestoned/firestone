# pylint: disable=duplicate-code
"""
Generate Rust Clap based CLI from one or more resource schemas.
"""

import io
import logging
import os

import jinja2

from firestone.spec import _base as spec_base
from firestone.spec import openapi as spec_openapi

# Map OpenAPI types to Rust types
PARAM_TYPE_TO_RUST_TYPE = {
    "string": "String",
    "integer": "i64",
    "boolean": "bool",
}

_LOGGER = logging.getLogger(__name__)


def _get_op_name(method: str, top_level: bool) -> str:
    """Get operation name from HTTP method."""
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


def _to_snake_case(name: str) -> str:
    """Convert a name to snake_case."""
    snake = name.replace("-", "_").replace(" ", "_")
    # Escape Rust keywords
    rust_keywords = {
        "type",
        "match",
        "self",
        "Self",
        "super",
        "trait",
        "impl",
        "fn",
        "const",
        "static",
        "let",
        "mut",
        "ref",
        "move",
        "as",
        "use",
        "pub",
        "mod",
        "crate",
        "extern",
        "where",
        "unsafe",
        "async",
        "await",
    }
    if snake in rust_keywords:
        return f"r#{snake}"
    return snake


def _to_pascal_case(name: str) -> str:
    """Convert a name to PascalCase."""
    parts = name.replace("-", "_").replace(" ", "_").split("_")
    return "".join(part.capitalize() for part in parts)


def _enum_value_to_variant(enum_value: str) -> str:
    """Convert an enum value to a Rust enum variant name.

    Examples:
        "work" -> "Work"
        "admin-roles" -> "AdminRoles"
        "read-write" -> "ReadWrite"
    """
    return _to_pascal_case(enum_value)


# pylint: disable=too-many-locals,too-many-branches,too-many-statements,too-many-nested-blocks
def _enrich_attr_for_body(
    attr: dict,
    rsrc_name: str,  # pylint: disable=unused-argument
    comp_name: str,
    op_name: str,
    key_names: list = None,  # pylint: disable=unused-argument
):
    """Enrich an attribute with metadata for request body generation.

    Adds:
    - body_conversion: Rust code to convert CLI arg to body field value
    - is_path_param_in_body: Whether this is a path param that also appears in body
    - enum_model_type: Model enum type name
    - enum_variant_mappings: Mappings from CLI enum to model enum
    - needs_none_in_update: Whether to set to None in update body
    """
    if not key_names:
        key_names = []

    attr_name = attr["name"]
    rust_name = attr["rust_name"]
    rust_type = attr["type"]
    is_enum = attr.get("is_enum", False)
    is_enum_array = attr.get("is_enum_array", False)
    is_argument = attr.get("argument", False)
    is_required = attr.get("required", False)

    # Check if this is a path parameter that also appears in the body
    is_path_param_in_body = is_argument and attr_name in key_names

    # Determine body conversion code
    body_conversion = None
    needs_none_in_update = False

    if is_path_param_in_body:
        # Path parameters that appear in body should be set to None in update operations
        needs_none_in_update = True
        body_conversion = "None"
    elif is_enum_array:
        # Array of enums - needs conversion from Vec<String> to Vec<EnumType>
        enum_variants = attr.get("enum_variants", [])
        # The model enum type for arrays - OpenAPI generator uses the property name in PascalCase
        # For example, "categories" becomes "Categories" not "CategoriesItem"
        enum_item_type = f"crate::models::{op_name}_{comp_name}::{_to_pascal_case(attr_name)}"
        attr["enum_item_type"] = enum_item_type

        # Generate variant mappings for the array items
        variant_mappings = []
        for variant in enum_variants:
            variant_name = variant["name"]
            variant_value = variant["value"]
            model_variant = _enum_value_to_variant(variant_value)
            variant_mappings.append(
                {
                    "cli_variant": variant_name,
                    "model_variant": model_variant,
                }
            )
        attr["enum_variant_mappings"] = variant_mappings
        body_conversion = "ENUM_ARRAY_MATCH"  # Special marker for template
    elif is_enum:
        # Enum conversion - generate match statement
        enum_variants = attr.get("enum_variants", [])
        enum_model_type = f"crate::models::{op_name}_{comp_name}::{_to_pascal_case(attr_name)}"
        attr["enum_model_type"] = enum_model_type

        # Generate variant mappings
        variant_mappings = []
        for variant in enum_variants:
            variant_name = variant["name"]
            variant_value = variant["value"]
            # Convert enum value to PascalCase for model enum (e.g., "admin-ro" -> "AdminRo")
            model_variant = _enum_value_to_variant(variant_value)
            variant_mappings.append(
                {
                    "cli_variant": variant_name,
                    "model_variant": model_variant,
                }
            )
        attr["enum_variant_mappings"] = variant_mappings
        body_conversion = "ENUM_MATCH"  # Special marker for template
    elif rust_type == "String":
        # Check if this is an object reference (like person with $ref)
        # First check original_schema (before jsonref resolution) for $ref
        original_schema = attr.get("original_schema", {})
        param_schema = attr.get("schema", {})

        # Check for $ref in original schema (before resolution)
        schema_ref = None
        if isinstance(original_schema, dict):
            schema_ref = original_schema.get("$ref")
        elif hasattr(original_schema, "get"):
            schema_ref = original_schema.get("$ref")

        # Also check param_schema for $ref (in case original_schema wasn't set)
        has_get = hasattr(param_schema, "get")
        if not schema_ref and has_get and isinstance(param_schema, dict):
            schema_ref = param_schema.get("$ref")

        is_object_ref = bool(schema_ref)

        if not is_object_ref and has_get:
            # Check if schema has a 'key' field (indicates it's a resource schema, i.e., a reference)
            if "key" in param_schema:
                is_object_ref = True
            else:
                # Check if resolved schema is an object type without properties (indicates object reference)
                param_type = param_schema.get("type")
                has_properties = "properties" in param_schema
                # If it's an object type but has no properties, it's likely a reference
                if param_type == "object" and not has_properties:
                    is_object_ref = True
                elif param_type == "array":
                    items = param_schema.get("items", {})
                    if hasattr(items, "get"):
                        # Check if items has a 'key' field (indicates it's a resource schema)
                        if "key" in items:
                            is_object_ref = True
                        else:
                            items_type = items.get("type")
                            items_has_properties = "properties" in items
                            # If items is object type without properties, it's a reference
                            if items_type == "object" and not items_has_properties:
                                is_object_ref = True

        if is_object_ref:
            # Object reference - needs JSON parsing
            # Extract model name from $ref if present (e.g., "person.yaml#/schema" -> "person")
            if schema_ref:
                # Extract name from ref (e.g., "person.yaml#/schema" -> "person")
                # Handle both "person.yaml#/schema" and "#/components/schemas/person" formats
                if "#" in schema_ref:
                    ref_part = schema_ref.split("#")[0]
                else:
                    ref_part = schema_ref
                # Extract filename or last component
                ref_parts = ref_part.split("/")
                ref_name = ref_parts[-1].replace(".yaml", "").replace(".json", "")
            else:
                ref_name = attr_name
            model_type = f"crate::models::{_to_pascal_case(ref_name)}"
            body_conversion = f"args.{rust_name}.as_ref().and_then(|s| serde_json::from_str::<{model_type}>(s).ok()).map(|p| Box::new(p))"
        elif param_schema.get("expose") is False or attr_name in key_names:
            # Fields with expose: false or key fields need Option<Option<Value>>
            # This handles fields like address_key, uuid that use serde_with::rust::double_option
            # However, if the field is required, it's a String not Option<String>
            if is_required:
                # Required key field: convert directly without .as_ref()
                # It's Option<Value> in the model
                body_conversion = f"Some(serde_json::Value::String(args.{rust_name}.clone()))"
            else:
                # Optional key field: use .as_ref().map()
                body_conversion = (
                    f"args.{rust_name}.as_ref().map(|s| Some(serde_json::Value::String(s.clone())))"
                )
        else:
            # Regular string
            body_conversion = f"args.{rust_name}.clone()"
    elif rust_type == "i64":
        # Integer conversion - check if model expects i32
        # Required fields don't need .map(), optional fields do
        if is_required:
            body_conversion = f"args.{rust_name} as i32"
        else:
            body_conversion = f"args.{rust_name}.map(|v| v as i32)"
    elif rust_type == "bool":
        # Boolean - pass directly
        body_conversion = f"args.{rust_name}"
    elif rust_type == "Vec<String>":
        # Vector - clone
        body_conversion = f"args.{rust_name}.clone()"
    else:
        # Default - clone
        body_conversion = f"args.{rust_name}.clone()"

    # Ensure body_conversion is always set
    if not body_conversion:
        body_conversion = f"args.{rust_name}.clone()"

    attr["body_conversion"] = body_conversion
    attr["is_path_param_in_body"] = is_path_param_in_body
    attr["needs_none_in_update"] = needs_none_in_update

    # Debug logging
    if attr_name == "person":
        _LOGGER.debug(f"Person attr schema: {attr.get('schema')}")
        _LOGGER.debug(f"Person body_conversion: {body_conversion}")

    return attr


# pylint: disable=too-many-locals
def params_to_attrs(params: list, required: list = None, key_names: list = None):
    """Convert the params from OpenAPI spec to Clap attributes."""
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
        param_type = param_schema.get("type", "string")
        rust_type = "String"
        enum_variants = None

        # this means that this param/attribute is another object
        if param_type in ["object", "array"]:
            _LOGGER.info(f"{param['name']} is of type '{param_type}', processing special CLI type.")
            rust_type = "String"  # JSON string for objects/arrays
            items_schema = param_schema.get("items", {})
            items_type = items_schema.get("type", "string")
            _LOGGER.debug(f"rust_type: {rust_type}")
            _LOGGER.debug(f"items_type: {items_type}")

            # Check if array items are enums
            if param_type == "array" and "enum" in items_schema:
                _LOGGER.info(
                    f"{param['name']} is an array of enums, setting to Vec<String> for CLI"
                )
                rust_type = "Vec<String>"
                # Store enum info for body conversion
                enum_variants = []
                for enum_val in items_schema["enum"]:
                    variant = enum_val.upper().replace("-", "_").replace(" ", "_")
                    enum_variants.append(
                        {
                            "name": variant,
                            "value": enum_val,
                        }
                    )
            elif param_type == "array" and items_type != "object":
                _LOGGER.info(
                    f"{param['name']} has items of type '{items_type}', setting to Vec<String>"
                )
                rust_type = "Vec<String>"
        elif "enum" in param_schema:
            _LOGGER.info(f"{param['name']} is of type '{param_type}', creating enum")
            rust_type = f"{_to_pascal_case(param['name'])}Enum"
            # Pre-process enum values to Rust enum variant names
            enum_variants = []
            for enum_val in param_schema["enum"]:
                variant = enum_val.upper().replace("-", "_").replace(" ", "_")
                enum_variants.append(
                    {
                        "name": variant,
                        "value": enum_val,
                    }
                )
        else:
            _LOGGER.info(
                f"{param['name']} is of type: {param_type}, looking up type in PARAM_TYPE_TO_RUST_TYPE"
            )
            rust_type = PARAM_TYPE_TO_RUST_TYPE.get(param_type, "String")

        param_name = param["name"]
        required_val = param_name in required
        _LOGGER.debug(f"param_name: {param_name}")
        _LOGGER.debug(f"key_names: {key_names}")

        # Convert to snake_case for Rust
        rust_name = _to_snake_case(param_name)

        # Check if this is an array of enums
        is_enum_array = param_type == "array" and "enum" in param_schema.get("items", {})

        # Get parameter location (query, path, body)
        param_in = param.get("in", "body")  # Default to body if not specified

        attr = {
            "argument": param_name in key_names,
            "name": param_name,  # Keep original for API calls
            "rust_name": rust_name,  # Snake case for Rust
            "description": param.get("description", ""),
            "type": rust_type,
            "required": param.get("required", required_val),
            "is_enum": "enum" in param_schema,
            "is_enum_array": is_enum_array,
            "schema": param_schema,  # Preserve schema for enrichment
            "in": param_in,  # Parameter location (query, path, body)
        }
        if "enum" in param_schema:
            attr["enum_values"] = param_schema["enum"]
            attr["enum_variants"] = enum_variants
        if is_enum_array:
            # For enum arrays, store the enum info from items
            attr["enum_values"] = param_schema.get("items", {}).get("enum", [])
            attr["enum_variants"] = enum_variants
        if param.get("default") is not None:
            attr["default"] = param.get("default")

        attrs.append(attr)

    return attrs


def get_resource_attrs(
    schema: dict, params: dict = None, check_required: bool = None, key_names: list = None
):
    """Get resource attributes."""
    _LOGGER.debug(f"key_names: {key_names}")
    props = schema.get("items", {}).get("properties", {})
    # Preserve original schema info for each property
    tmp_attrs = []
    for attr_name in props:
        prop_data = props[attr_name]
        attr_data = {"name": attr_name}
        # Copy all properties
        attr_data.update(prop_data)
        # Preserve original schema structure before resolution
        # Check if schema has $ref (before jsonref resolution)
        if "schema" in prop_data:
            schema_val = prop_data["schema"]
            # Preserve the original schema dict (may contain $ref)
            if isinstance(schema_val, dict):
                attr_data["original_schema"] = schema_val
            elif hasattr(schema_val, "__dict__"):
                # Try to get dict representation
                attr_data["original_schema"] = (
                    dict(schema_val)
                    if hasattr(schema_val, "__iter__") and not isinstance(schema_val, str)
                    else {}
                )
            # Also keep resolved schema for type detection
            attr_data["schema"] = schema_val
        elif "$ref" in prop_data:
            # $ref at top level
            attr_data["original_schema"] = {"$ref": prop_data["$ref"]}
            attr_data["schema"] = prop_data
        elif prop_data.get("type"):
            # Type info at top level
            attr_data["original_schema"] = prop_data
            attr_data["schema"] = prop_data
        tmp_attrs.append(attr_data)

    if params:
        tmp_attrs.extend(params)
    _LOGGER.debug(f"tmp_attrs: {tmp_attrs}")

    required = schema["items"].get("required", []) if check_required else []
    _LOGGER.debug(f"required: {required}")

    attrs = params_to_attrs(tmp_attrs, required, key_names=key_names)
    _LOGGER.debug(f"attrs: {attrs}")

    return attrs


# pylint: disable=too-many-locals
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
        _LOGGER.info(f"Getting CLI attributes for {op_name}")

        op = {}
        op["name"] = op_name
        op["id"] = spec_base.get_opid(baseurl, method)
        op["description"] = descs.get(method, f"{op_name.capitalize()} operation for {rsrc_name}")
        op["is_delete"] = method == "delete"

        params = spec_openapi.get_params(baseurl, method, schema, keys=keys)
        _LOGGER.debug(f"params: {params}")

        key_names = [key["name"] for key in keys]
        _LOGGER.debug(f"key_names: {key_names}")
        attrs = params_to_attrs(params, key_names=key_names)

        if op_name == "update":
            attrs = get_resource_attrs(schema, params=params, key_names=key_names)

        # Deduplicate attributes by name
        seen_names = {}
        deduplicated_attrs = []
        for attr in attrs:
            attr_name = attr["name"]
            if attr_name not in seen_names:
                seen_names[attr_name] = True
                deduplicated_attrs.append(attr)
            elif not attr.get("argument"):
                # If duplicate and not an argument, prefer the non-argument one
                # Replace the existing one
                for i, existing_attr in enumerate(deduplicated_attrs):
                    if existing_attr["name"] == attr_name:
                        deduplicated_attrs[i] = attr
                        break

        _LOGGER.debug(f"attrs: {deduplicated_attrs}")

        op["attrs"] = deduplicated_attrs

        ops.append(op)

    return ops


# pylint: disable=too-many-locals
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
        op["is_delete"] = method == "delete"

        # Add params and attributes
        params = spec_openapi.get_params(baseurl, method, schema, keys=keys)
        if default_query_params:
            params.extend(default_query_params)
        _LOGGER.debug(f"params: {params}")

        attrs = params_to_attrs(params)

        if op_name == "create":
            check_required = True
            attrs = get_resource_attrs(schema, check_required=check_required)

        # Deduplicate attributes by name
        seen_names = {}
        deduplicated_attrs = []
        for attr in attrs:
            attr_name = attr["name"]
            if attr_name not in seen_names:
                seen_names[attr_name] = True
                deduplicated_attrs.append(attr)
            elif not attr.get("argument"):
                # If duplicate and not an argument, prefer the non-argument one
                for i, existing_attr in enumerate(deduplicated_attrs):
                    if existing_attr["name"] == attr_name:
                        deduplicated_attrs[i] = attr
                        break

        _LOGGER.debug(f"attrs: {deduplicated_attrs}")

        op["attrs"] = deduplicated_attrs

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
    rsrc_name = rsrc["kind"]
    schema = rsrc["schema"]
    methods = rsrc.get("methods", {})
    descs = rsrc.get("descriptions", {})

    if not ops:
        ops = {}

    if schema["type"] == "array" and "key" not in schema:
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
        default_query_params=default_query_params,
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
    pkg: str,
    client_pkg: str,
    rsrc_data: list,
    title: str,
    desc: str,
    summary: str,
    version: str,
    as_modules: bool = False,
    template: str = None,
):
    """Generate a Clap based CLI script based on the resource data sent and other meta data."""
    rsrcs = []
    for rsrc in rsrc_data:
        rsrc_name = rsrc["kind"]
        baseurl = "/"
        if rsrc.get("versionInPath", False):
            baseurl += f"v{rsrc['apiVersion']}/"
        baseurl += rsrc_name
        _LOGGER.debug(f"baseurl: {baseurl}")

        default_query_params = rsrc.get("default_query_params", [])
        _LOGGER.debug(f"default_query_params: {default_query_params}")

        # Extract keys before calling get_ops
        schema = rsrc["schema"]
        keys = []
        if "key" in schema:
            key = schema["key"]
            keys.append(key)

        ops = get_ops(
            rsrc,
            baseurl,
            ops={},
            keys=keys,
            default_query_params=default_query_params,
        )
        _LOGGER.debug(f"ops: {ops}")

        # Add PascalCase names for Rust
        rsrc_pascal = _to_pascal_case(rsrc_name)
        rsrc_upper = rsrc_name.upper().replace("-", "_").replace(" ", "_")

        # Calculate component name (singular form)
        comp_name = rsrc_name if not rsrc_name.endswith("s") else rsrc_name[:-1]
        comp_name_pascal = _to_pascal_case(comp_name)

        # Process operations to add PascalCase names and enrich attributes
        processed_ops = {}
        key_names = [key["name"] for key in keys] if keys else []
        for op_type in ["resource", "instance"]:
            processed_ops[op_type] = []
            for op in ops.get(op_type, []):
                op_pascal = _to_pascal_case(op["name"])
                # Enrich attributes with body conversion metadata
                enriched_attrs = []
                for attr in op.get("attrs", []):
                    # Make a deep copy to avoid modifying the original
                    attr_copy = dict(attr)
                    if "schema" in attr:
                        attr_copy["schema"] = (
                            dict(attr["schema"])
                            if isinstance(attr["schema"], dict)
                            else attr["schema"]
                        )
                    enriched_attr = _enrich_attr_for_body(
                        attr_copy,
                        rsrc_name,
                        comp_name,
                        op["name"],
                        key_names=key_names,
                    )
                    enriched_attrs.append(enriched_attr)

                # Build query params list in the order they appear in attrs
                # This preserves the order from the OpenAPI spec
                query_params = []
                for attr in enriched_attrs:
                    if attr.get("in") == "query":
                        query_params.append(attr)

                processed_op = {
                    **op,
                    "pascal_name": op_pascal,
                    "attrs": enriched_attrs,
                    "query_params": query_params,  # Explicit list of all query params for API calls
                }
                processed_ops[op_type].append(processed_op)

        rsrcs.append(
            {
                "name": rsrc_name,
                "pascal_name": rsrc_pascal,
                "upper_name": rsrc_upper,
                "comp_name": comp_name,
                "comp_name_pascal": comp_name_pascal,
                "operations": processed_ops,
            }
        )

    _LOGGER.info(f"rsrcs: {rsrcs}")

    tmpl = None
    if template and os.path.exists(template):
        _LOGGER.info(f"Using custom template from {template}")
        tmpl_str = ""
        with io.open(template, "r", encoding="utf-8") as fh:
            tmpl_str = "".join(fh.readlines())

        tmpl = jinja2.Environment(
            loader=jinja2.BaseLoader,
            extensions=["jinja2.ext.loopcontrols"],
        ).from_string(tmpl_str)

    # Convert Python-style client_pkg to Rust-style (dots to underscores)
    rust_client_pkg = client_pkg.replace(".", "_")

    if not as_modules:
        if not tmpl:
            tmpl = spec_base.JINJA_ENV.get_template("main.rs.jinja2")
        return tmpl.render(
            title=title,
            summary=summary,
            description=desc,
            version=version,
            pkg=pkg,
            client_pkg=rust_client_pkg,
            rsrcs=rsrcs,
        )

    # Convert Python-style client_pkg to Rust-style (dots to underscores)
    rust_client_pkg = client_pkg.replace(".", "_")

    rendered_rsrcs = {}
    for rsrc in rsrcs:
        if not tmpl:
            tmpl = spec_base.JINJA_ENV.get_template("cli_module.rs.jinja2")
        rendered = tmpl.render(
            title=title,
            summary=summary,
            description=desc,
            version=version,
            pkg=pkg,
            client_pkg=rust_client_pkg,
            rsrc=rsrc,
        )
        rendered_rsrcs[rsrc["name"]] = rendered

    return rendered_rsrcs
