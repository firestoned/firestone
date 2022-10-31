"""
Utility to manage resource json schema files.

Used for reading a schema file, validate against firestone schema and convert to
dict.
"""
import io
import logging

import pkg_resources
import jsonref
import jsonschema
import yaml


_LOGGER = logging.getLogger(__name__)


def get_resource_schema(filename: str) -> dict:
    """Get a resource schema file in JSON or YAML format.

    First try YAML, then JSON

    :param str filename: the file name, full path, to read JSON schema from
    :return: return a dictionary of the json schema, usable for validation
    :rtype: dict
    """
    rsrc_data = {}
    with io.open(filename, "r", encoding="utf-8") as fh:
        if filename.endswith(".json"):
            _LOGGER.debug(f"Loading resource file {filename} using jsonref")
            rsrc_data = jsonref.load(fh)
        else:
            _LOGGER.debug(f"Loading resource file {filename} using yaml")
            rsrc_data = yaml.safe_load(fh)

    return rsrc_data


def validate(data: dict) -> bool:
    """Validate user given resource schema, data, agianst our schema.

    :param dict data: the data as a dict from user resource
    :return: return True if validate, else throw exception
    :rtype: bool
    """
    schema_file = pkg_resources.resource_stream("firestone.schema", "resource.yaml")

    schema = get_resource_schema(schema_file.name)

    jsonschema.validate(instance=data, schema=schema)
