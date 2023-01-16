"""
Utility to manage resource json schema files.

Used for reading a schema file, validate against firestone schema and convert to
dict.
"""
import io
import json
import logging

import jsonref
import jsonschema
import pkg_resources
import yaml


_LOGGER = logging.getLogger(__name__)


def _jsonloader(uri, **kwargs):
    if uri.startswith("file://"):
        uri = uri[8:]

    with io.open(uri, "r", encoding="utf-8") as fh:
        if uri.endswith(".json"):
            _LOGGER.debug(f"Loading resource file {uri} using jsonref")
            return jsonref.load(fh)

        _LOGGER.debug(f"Loading resource file {uri} using yaml")
        rsrc_data = yaml.safe_load(fh)

        dumpj = json.dumps(rsrc_data)
        return jsonref.loads(dumpj, loader=_jsonloader, base_uri=f"file:{uri}", **kwargs)


def get_resource_schema(filename: str) -> dict:
    """Get a resource schema file in JSON or YAML format.

    First try YAML, then JSON

    :param str filename: the file name, full path, to read JSON schema from
    :return: return a dictionary of the json schema, usable for validation
    :rtype: dict
    """
    with io.open(filename, "r", encoding="utf-8") as fh:
        if filename.endswith(".json"):
            _LOGGER.debug(f"Loading resource file {filename} using jsonref")
            return jsonref.load(fh)

        _LOGGER.debug(f"Loading resource file {filename} using yaml")
        rsrc_data = yaml.safe_load(fh)
        dumpj = json.dumps(rsrc_data)
        return jsonref.loads(
            dumpj, loader=_jsonloader, base_uri=f"file:{filename}", lazy_load=False
        )


def validate(data: dict) -> bool:
    """Validate user given resource schema, data, agianst our schema.

    :param dict data: the data as a dict from user resource
    :return: return True if validate, else throw exception
    :rtype: bool
    """
    schema_file = pkg_resources.resource_stream("firestone.schema", "resource.yaml")

    schema = get_resource_schema(schema_file.name)

    jsonschema.validate(instance=data, schema=schema)
