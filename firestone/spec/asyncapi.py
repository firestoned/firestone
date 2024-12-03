"""
Generate AsyncAPI 2.5 Spec
"""

# TODO: fix dupe code
# pylint: disable=duplicate-code

import enum
import copy
import logging

from firestone.spec import _base as spec_base

_LOGGER = logging.getLogger(__name__)


class OperationType(enum.Enum):
    """The operation type for a channel."""

    SUBSCRIBE = "subscribe"
    PUBLISH = "publish"


class SupportedBindingType(enum.Enum):
    """The supported binding type for an operation."""

    HTTP = "http"
    WS = "ws"


def get_payload(
    schema: dict,
    comp_name: str = None,
    attr_name: bool = None,
    is_list: bool = None,
):
    """Set schema for a given operation type."""
    # Default to using the schema directly in the file
    payload = schema["items"] if "items" in schema else schema

    # if a component name is provided, use that to reference it
    ref = None
    if comp_name:
        ref = f"#/components/schemas/{comp_name}"
    if attr_name:
        ref = f"#/components/schemas/{comp_name}/properties/{attr_name}"

    if is_list:
        items = {"$ref": ref} if ref else payload
        return {
            "type": "array",
            "items": items,
        }
    if ref:
        return {"$ref": ref}

    return payload


def get_message(
    rsrc_name: str,
    schema: dict,
    content_type: str,
    comp_name: str = None,
    attr_name: bool = None,
    is_list: bool = None,
):
    """Get a message for the operation.

    :param str rsrc_name: the resource name
    :param dict schema: the schema for this resource name
    :param str content_type: the content type for the messages
    """
    message = {"name": rsrc_name, "contentType": content_type}
    payload = get_payload(
        schema,
        comp_name=comp_name,
        attr_name=attr_name,
        is_list=is_list,
    )
    _LOGGER.debug(f"payload: {payload}")
    message["payload"] = payload

    return message


def get_binding(
    meta: dict,
    schema: dict,
    method: str,
):
    """Get a binding for the operation.

    :param dict meta: the meta data in the resource
    :param dict schema: the schema for this resource name
    :param str method: the method being used in this binging
    """
    query_params = schema.get("query_params", [])
    default_query_params = meta.get("default_query_params")
    query_params.extend(default_query_params)

    query = {}
    if "query_params" in schema:
        query = {"type": "object", "required": [], "properties": {}}
        for param in query_params:
            _LOGGER.debug(f"param: {param}")
            methods = param.get("methods", [])
            _LOGGER.debug(f"methods: {methods}")
            if methods:
                del param["methods"]
            if methods and method not in methods:
                continue

            param_name = param["name"]
            required = param.get("required", False)
            if required and param_name not in query["required"]:
                query["required"].append(param_name)

            query["properties"][param_name] = {
                "description": param["description"],
            }
            query["properties"][param_name].update(param.get("schema", {"type": "string"}))

    return {
        "method": method,
        "query": query,
    }


def get_channel(
    meta: dict,
    baseurl: str,
    schema: dict,
    descs: dict,
    keys: list = None,
    rsrc_name: str = None,
    attr_name: str = None,
    is_list: bool = None,
):
    """Get a channel for the given info.

    :param dict meta: the meta data in the resource
    :param str baseurl: the baseurl to use for channels
    :param dict schema: the schema for this resource name
    :param dict descs: the descriptions
    :param list keys: the keys dict for the instance of this resource
    :param bool is_list: this schema is for a list
    """

    # Sane default
    if is_list is None:
        is_list = False

    # TODO: send what operation types, as a list
    if not rsrc_name:
        rsrc_name = meta["name"]

    channel = {
        "description": f"Channel for {baseurl}",
        "parameters": {},
    }
    _LOGGER.debug(f"keys: {keys}")
    if keys:
        for key in keys:
            key_name = key["name"]
            _LOGGER.debug(f"key_name: {key_name}: {baseurl}")
            if key_name not in baseurl:
                continue
            channel["parameters"][key_name] = {
                "description": key["description"],
                "schema": key.get("schema") or {"type": "string"},
            }
    _LOGGER.debug(f"channel: {channel}")

    # 1. Add subscribers, i.e. get
    method = "get"
    message = get_message(
        rsrc_name,
        schema,
        spec_base.DEFAULT_CONTENT_TYPE,
        comp_name=rsrc_name,
        attr_name=attr_name,
        is_list=is_list,
    )

    binding = get_binding(meta, schema, method)
    _LOGGER.debug(f"binding: {binding}")
    channel[OperationType.SUBSCRIBE.value] = {
        "operationId": spec_base.get_opid(baseurl, OperationType.SUBSCRIBE.value),
        "description": descs.get(method, f"Subscribe from {baseurl}"),
        "message": message,
        "bindings": {
            SupportedBindingType.WS.value: binding,
        },
        "tags": [{"name": rsrc_name}],
    }

    # 2. Add publishers, i.e. post
    method = "post"
    message = get_message(
        rsrc_name,
        schema,
        spec_base.DEFAULT_CONTENT_TYPE,
        comp_name=rsrc_name,
        attr_name=attr_name,
    )
    binding = get_binding(meta, schema, method)
    _LOGGER.debug(f"binding: {binding}")

    channel[OperationType.PUBLISH.value] = {
        "operationId": spec_base.get_opid(baseurl, OperationType.PUBLISH.value),
        "description": descs.get(method, f"Publish to {baseurl}"),
        "message": message,
        "bindings": {
            SupportedBindingType.WS.value: binding,
        },
        "tags": [{"name": rsrc_name}],
    }

    return channel


def add_resource_level(
    meta: dict,
    baseurl: str,
    schema: dict,
    channels: dict,
    keys: list = None,
    rsrc_name: str = None,
):
    """Add resource level channels.

    :param dict meta: the meta data in the resource
    :param str baseurl: the baseurl to use for channels
    :param dict schema: the schema for this resource name
    :param dict channels: the channels
    :param list keys: the keys list for the instance of this resource
    :param str rsrc_name: override the resource name, defaults to meta data
    """
    _LOGGER.debug(f"keys: {keys}")

    # TODO: move to using "subscribe" in meta
    method = "get"
    rsrc_methods = schema.get("methods", [])

    if rsrc_methods and method not in rsrc_methods:
        return channels

    rsrc_descs = schema.get("descriptions", {})

    channels[baseurl] = get_channel(
        meta, baseurl, schema, rsrc_descs, keys=keys, rsrc_name=rsrc_name, is_list=True
    )

    return channels


def add_instance_level(
    meta: dict,
    baseurl: str,
    schema: dict,
    channels: dict,
    keys: list = None,
    rsrc_name: str = None,
):
    """Add instance level channels.

    :param dict meta: the meta data in the resource
    :param str baseurl: the baseurl to use for channels
    :param dict schema: the schema for this resource name
    :param dict channels: the channels
    :param list keys: the keys list for the instance of this resource
    :param str rsrc_name: override the resource name, defaults to meta data
    """
    _LOGGER.debug(f"keys: {keys}")

    # TODO: move to using "subscribe" in meta
    method = "get"
    rsrc_methods = schema.get("methods", [])

    if rsrc_methods and method not in rsrc_methods:
        return channels

    _LOGGER.debug(f"schema: {schema}")
    rsrc_inst_descs = schema["items"].get("descriptions", {})

    channels[baseurl] = get_channel(
        meta, baseurl, schema, rsrc_inst_descs, keys=keys, rsrc_name=rsrc_name
    )

    return channels


def add_instance_attrs_level(
    meta: dict,
    baseurl: str,
    schema: dict,
    channels: dict,
    keys: list = None,
    components: dict = None,
    rsrc_name: str = None,
):
    """Add the instance attr level channels.

    :param dict meta: the meta data in the resource
    :param str baseurl: the baseurl to use for channels
    :param dict schema: the schema for this resource name
    :param dict channels: the channels
    :param dict keys: the keys dict for the instance of this resource
    :param str rsrc_name: override the resource name, defaults to meta data
    """
    _LOGGER.debug(f"keys: {keys}")

    method = "get"
    rsrc_methods = schema.get("methods", [])
    rsrc_inst_descs = schema["items"].get("descriptions", {})

    for prop in schema["items"]["properties"]:
        path = "/".join([baseurl, prop])
        _LOGGER.debug(f"path: {path}")
        prop_schema = schema["items"]["properties"][prop]

        if "expose" in prop_schema and not prop_schema["expose"]:
            continue

        if rsrc_methods and method not in rsrc_methods:
            _LOGGER.info(
                f"Skipping the definition of {method} in resource instance attribute generation, "
                "as it is not in the defined methods requested"
            )
            continue

        # Recursively get channels for this property
        if "schema" in prop_schema:
            components["schemas"][prop] = prop_schema["schema"]["items"]
            _LOGGER.debug(f"components: {components}")
            get_channels(
                meta,
                path,
                prop_schema["schema"],
                keys=keys,
                rsrc_name=prop,
                channels=channels,
                components=components,
            )
        else:
            channels[path] = get_channel(
                meta,
                path,
                prop_schema,
                rsrc_inst_descs,
                keys=keys,
                rsrc_name=rsrc_name,
                attr_name=prop,
            )


def get_channels(
    meta: dict,
    baseurl: str,
    schema: dict,
    keys: list = None,
    rsrc_name: str = None,
    channels: dict = None,
    components: dict = None,
):
    """Get the channels, based on the resource definition."""
    if not channels:
        channels = {}
    _LOGGER.debug(f"keys: {keys}")

    asyncapi = meta.get("asyncapi", {})

    key = schema["key"]
    keys.append(key)

    # 1. Add resource level channels
    if asyncapi.get("channels", {}).get("resources"):
        add_resource_level(
            meta,
            baseurl,
            schema,
            channels,
            keys=keys,
            rsrc_name=rsrc_name,
        )

    if not asyncapi.get("channels", {}).get("instances") and not asyncapi.get("channels", {}).get(
        "instance_attrs"
    ):
        return channels

    if schema["type"] == "array" and not "key" in schema:
        raise spec_base.SchemaMissingAttribute(
            "You set asyncapi.channels.instances: true, but a 'key' is missing in schema {yaml.dump(schema)}"
        )

    instance_baseurl = "/".join([baseurl, f"{{{key['name']}}}"])
    _LOGGER.debug(f"instance_baseurl: {instance_baseurl}")

    # 2. Add instance level channels
    if asyncapi.get("channels", {}).get("instances"):

        add_instance_level(
            meta,
            instance_baseurl,
            schema,
            channels,
            keys=keys,
            rsrc_name=rsrc_name,
        )

    # 3. Add instance attribute level channels
    if asyncapi.get("channels", {}).get("instance_attrs"):
        add_instance_attrs_level(
            meta,
            instance_baseurl,
            schema,
            channels,
            keys=keys,
            components=components,
            rsrc_name=rsrc_name,
        )

    return channels


# pylint: disable=too-many-locals
def generate(rsrc_data: list, title: str, desc: str, summary: str, version: str):
    """Generate an AsyncAPI spec based on the resource data sent and other meta data."""
    components = {"schemas": {}}
    all_channels = {}
    servers = {}
    for rsrc in rsrc_data:
        rsrc_name = rsrc["kind"]
        baseurl = "/"
        if rsrc.get("versionInPath", False):
            baseurl += f"v{rsrc['apiVersion']}/"
        baseurl += rsrc_name
        _LOGGER.debug(f"baseurl: {baseurl}")

        # Extract and set high-level resource component schema
        rschema = rsrc["schema"]
        comp_schema = copy.deepcopy(rschema["items"])
        if "descriptions" in comp_schema:
            del comp_schema["descriptions"]
        components["schemas"][rsrc_name] = comp_schema

        meta = copy.deepcopy(rsrc)
        # TODO: remove
        if "schema" in meta:
            del meta["schema"]

        channels = get_channels(
            meta,
            baseurl,
            rschema,
            keys=[],
            channels={},
            components=components,
        )
        rsrc_servers = meta.get("asyncapi", {}).get("servers", {})
        servers.update(rsrc_servers)
        _LOGGER.debug(f"channels: {channels}")
        all_channels.update(channels)

    tmpl = spec_base.JINJA_ENV.get_template("asyncapi.jinja2")
    return tmpl.render(
        title=title,
        summary=summary,
        description=desc,
        version=version,
        servers=servers,
        components=components,
        channels=all_channels,
    )
