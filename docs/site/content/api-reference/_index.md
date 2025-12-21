+++
title = "API Reference"
template = "section.html"
weight = 1
+++
# Table of Contents

* [firestone.spec.openapi](#firestone.spec.openapi)
  * [get\_responses](#firestone.spec.openapi.get_responses)
  * [get\_method\_op](#firestone.spec.openapi.get_method_op)
  * [get\_params](#firestone.spec.openapi.get_params)
  * [add\_resource\_methods](#firestone.spec.openapi.add_resource_methods)
  * [add\_instance\_methods](#firestone.spec.openapi.add_instance_methods)
  * [add\_instance\_attr\_methods](#firestone.spec.openapi.add_instance_attr_methods)
  * [get\_paths](#firestone.spec.openapi.get_paths)
  * [add\_rsrc\_components](#firestone.spec.openapi.add_rsrc_components)
  * [generate](#firestone.spec.openapi.generate)
* [firestone.spec.asyncapi](#firestone.spec.asyncapi)
  * [OperationType](#firestone.spec.asyncapi.OperationType)
  * [SupportedBindingType](#firestone.spec.asyncapi.SupportedBindingType)
  * [get\_payload](#firestone.spec.asyncapi.get_payload)
  * [get\_message](#firestone.spec.asyncapi.get_message)
  * [get\_binding](#firestone.spec.asyncapi.get_binding)
  * [get\_channel](#firestone.spec.asyncapi.get_channel)
  * [add\_resource\_level](#firestone.spec.asyncapi.add_resource_level)
  * [add\_instance\_level](#firestone.spec.asyncapi.add_instance_level)
  * [add\_instance\_attrs\_level](#firestone.spec.asyncapi.add_instance_attrs_level)
  * [get\_channels](#firestone.spec.asyncapi.get_channels)
  * [generate](#firestone.spec.asyncapi.generate)
* [firestone.spec.cli](#firestone.spec.cli)
  * [params\_to\_attrs](#firestone.spec.cli.params_to_attrs)
  * [get\_resource\_attrs](#firestone.spec.cli.get_resource_attrs)
  * [get\_instance\_ops](#firestone.spec.cli.get_instance_ops)
  * [get\_resource\_ops](#firestone.spec.cli.get_resource_ops)
  * [get\_ops](#firestone.spec.cli.get_ops)
  * [generate](#firestone.spec.cli.generate)
* [firestone.spec.streamlit](#firestone.spec.streamlit)
  * [params\_to\_attrs](#firestone.spec.streamlit.params_to_attrs)
  * [get\_resource\_attrs](#firestone.spec.streamlit.get_resource_attrs)
  * [get\_instance\_ops](#firestone.spec.streamlit.get_instance_ops)
  * [get\_resource\_ops](#firestone.spec.streamlit.get_resource_ops)
  * [get\_ops](#firestone.spec.streamlit.get_ops)
  * [generate](#firestone.spec.streamlit.generate)
* [firestone.spec.\_base](#firestone.spec._base)
  * [SchemaMissingAttribute](#firestone.spec._base.SchemaMissingAttribute)
  * [yaml\_pretty](#firestone.spec._base.yaml_pretty)
  * [get\_opid](#firestone.spec._base.get_opid)


# firestone.spec.openapi {#firestone.spec.openapi}

Generate OpenAPI 3.0 Spec


#### get\_responses {#firestone.spec.openapi.get_responses}

```python
def get_responses(method: str,
                  schema: dict,
                  content_type: str,
                  comp_name: str = None,
                  attr_name: bool = None,
                  is_list: bool = None)
```

Set schema for a given operation type.


#### get\_method\_op {#firestone.spec.openapi.get_method_op}

```python
def get_method_op(path: str,
                  method: str,
                  schema: dict,
                  desc: str = None,
                  comp_name: str = None,
                  attr_name: str = None,
                  is_list: bool = None)
```

Get the specified method section for the paths.


#### get\_params {#firestone.spec.openapi.get_params}

```python
def get_params(baseurl: str,
               method: str,
               schema: dict,
               keys: list = None,
               param_schema: dict = None)
```

Get the parameters for this method.


#### add\_resource\_methods {#firestone.spec.openapi.add_resource_methods}

```python
def add_resource_methods(rsrc_name: str,
                         schema: dict,
                         baseurl: str,
                         paths: dict,
                         methods: list = None,
                         descs: dict = None,
                         keys: list = None,
                         default_query_params: dict = None,
                         orig_rsrc_name: str = None,
                         security: dict = None)
```

Add resource level methods to the paths.

**Arguments**:

- `rsrc_name` (`str`): the resource name
- `schema` (`dict`): the schema for this resource name
- `baseurl` (`str`): the baseurl to use for paths
- `paths` (`dict`): the paths
- `keys` (`list`): the keys for the instance of this resource
- `default_query_params` (`dict`): the paths


#### add\_instance\_methods {#firestone.spec.openapi.add_instance_methods}

```python
def add_instance_methods(rsrc_name: str,
                         schema: dict,
                         baseurl: str,
                         paths: dict,
                         methods: list = None,
                         descs: dict = None,
                         keys: list = None,
                         orig_rsrc_name: str = None,
                         security: dict = None)
```

Add the instance methods to the paths.

**Arguments**:

- `rsrc_name` (`str`): the resource name
- `schema` (`dict`): the schema for this resource name
- `baseurl` (`str`): the baseurl to use for paths
- `keys` (`list`): the keys for the instance of this resource
- `paths` (`dict`): the paths


#### add\_instance\_attr\_methods {#firestone.spec.openapi.add_instance_attr_methods}

```python
def add_instance_attr_methods(rsrc_name: str,
                              schema: dict,
                              baseurl: str,
                              paths: dict,
                              methods: dict = None,
                              keys: list = None,
                              default_query_params: dict = None,
                              components: dict = None,
                              orig_rsrc_name: str = None,
                              security: dict = None)
```

Add the instance attr methods to the paths.

**Arguments**:

- `rsrc_name` (`str`): the resource name
- `schema` (`dict`): the schema for this resource name
- `baseurl` (`str`): the baseurl to use for paths
- `keys` (`list`): the keys for the instance of this resource
- `paths` (`dict`): the paths
- `default_query_params` (`dict`): the paths


#### get\_paths {#firestone.spec.openapi.get_paths}

```python
def get_paths(rsrc_name: str,
              rsrc: dict,
              baseurl: str,
              paths: dict = None,
              keys: list = None,
              default_query_params: dict = None,
              components: dict = None,
              orig_rsrc_name: str = None,
              security: dict = None)
```

Get the paths for resource.


#### add\_rsrc\_components {#firestone.spec.openapi.add_rsrc_components}

```python
def add_rsrc_components(components: dict, rsrc_name: str, methods: dict,
                        schema: dict, security: dict)
```

Get the components for this resource.


#### generate {#firestone.spec.openapi.generate}

```python
def generate(rsrc_data: list,
             title: str,
             desc: str,
             summary: str,
             version: str,
             prefix: str = None,
             openapi_version: str = None)
```

Generate an OpenAPI spec based on the resource data sent and other meta data.


# firestone.spec.asyncapi {#firestone.spec.asyncapi}

Generate AsyncAPI 2.5 Spec


## OperationType Objects {#firestone.spec.asyncapi.OperationType}

```python
class OperationType(enum.Enum)
```

The operation type for a channel.


## SupportedBindingType Objects {#firestone.spec.asyncapi.SupportedBindingType}

```python
class SupportedBindingType(enum.Enum)
```

The supported binding type for an operation.


#### get\_payload {#firestone.spec.asyncapi.get_payload}

```python
def get_payload(schema: dict,
                comp_name: str = None,
                attr_name: bool = None,
                is_list: bool = None)
```

Set schema for a given operation type.


#### get\_message {#firestone.spec.asyncapi.get_message}

```python
def get_message(rsrc_name: str,
                schema: dict,
                content_type: str,
                comp_name: str = None,
                attr_name: bool = None,
                is_list: bool = None)
```

Get a message for the operation.

**Arguments**:

- `rsrc_name` (`str`): the resource name
- `schema` (`dict`): the schema for this resource name
- `content_type` (`str`): the content type for the messages


#### get\_binding {#firestone.spec.asyncapi.get_binding}

```python
def get_binding(meta: dict, schema: dict, method: str)
```

Get a binding for the operation.

**Arguments**:

- `meta` (`dict`): the meta data in the resource
- `schema` (`dict`): the schema for this resource name
- `method` (`str`): the method being used in this binging


#### get\_channel {#firestone.spec.asyncapi.get_channel}

```python
def get_channel(meta: dict,
                baseurl: str,
                schema: dict,
                descs: dict,
                keys: list = None,
                rsrc_name: str = None,
                attr_name: str = None,
                is_list: bool = None)
```

Get a channel for the given info.

**Arguments**:

- `meta` (`dict`): the meta data in the resource
- `baseurl` (`str`): the baseurl to use for channels
- `schema` (`dict`): the schema for this resource name
- `descs` (`dict`): the descriptions
- `keys` (`list`): the keys dict for the instance of this resource
- `is_list` (`bool`): this schema is for a list


#### add\_resource\_level {#firestone.spec.asyncapi.add_resource_level}

```python
def add_resource_level(meta: dict,
                       baseurl: str,
                       schema: dict,
                       channels: dict,
                       keys: list = None,
                       rsrc_name: str = None)
```

Add resource level channels.

**Arguments**:

- `meta` (`dict`): the meta data in the resource
- `baseurl` (`str`): the baseurl to use for channels
- `schema` (`dict`): the schema for this resource name
- `channels` (`dict`): the channels
- `keys` (`list`): the keys list for the instance of this resource
- `rsrc_name` (`str`): override the resource name, defaults to meta data


#### add\_instance\_level {#firestone.spec.asyncapi.add_instance_level}

```python
def add_instance_level(meta: dict,
                       baseurl: str,
                       schema: dict,
                       channels: dict,
                       keys: list = None,
                       rsrc_name: str = None)
```

Add instance level channels.

**Arguments**:

- `meta` (`dict`): the meta data in the resource
- `baseurl` (`str`): the baseurl to use for channels
- `schema` (`dict`): the schema for this resource name
- `channels` (`dict`): the channels
- `keys` (`list`): the keys list for the instance of this resource
- `rsrc_name` (`str`): override the resource name, defaults to meta data


#### add\_instance\_attrs\_level {#firestone.spec.asyncapi.add_instance_attrs_level}

```python
def add_instance_attrs_level(meta: dict,
                             baseurl: str,
                             schema: dict,
                             channels: dict,
                             keys: list = None,
                             components: dict = None,
                             rsrc_name: str = None)
```

Add the instance attr level channels.

**Arguments**:

- `meta` (`dict`): the meta data in the resource
- `baseurl` (`str`): the baseurl to use for channels
- `schema` (`dict`): the schema for this resource name
- `channels` (`dict`): the channels
- `keys` (`dict`): the keys dict for the instance of this resource
- `rsrc_name` (`str`): override the resource name, defaults to meta data


#### get\_channels {#firestone.spec.asyncapi.get_channels}

```python
def get_channels(meta: dict,
                 baseurl: str,
                 schema: dict,
                 keys: list = None,
                 rsrc_name: str = None,
                 channels: dict = None,
                 components: dict = None)
```

Get the channels, based on the resource definition.


#### generate {#firestone.spec.asyncapi.generate}

```python
def generate(rsrc_data: list, title: str, desc: str, summary: str,
             version: str)
```

Generate an AsyncAPI spec based on the resource data sent and other meta data.


# firestone.spec.cli {#firestone.spec.cli}

Generate python Click based CLI from one or more resource schemas.


#### params\_to\_attrs {#firestone.spec.cli.params_to_attrs}

```python
def params_to_attrs(params: list,
                    required: list = None,
                    key_names: list = None)
```

Convert the params from OpenAPI spec to Click attributes.


#### get\_resource\_attrs {#firestone.spec.cli.get_resource_attrs}

```python
def get_resource_attrs(schema: dict,
                       params: dict = None,
                       check_required: bool = None,
                       key_names: list = None)
```

Get resource attributes.


#### get\_instance\_ops {#firestone.spec.cli.get_instance_ops}

```python
def get_instance_ops(rsrc_name: str,
                     schema: dict,
                     baseurl: str,
                     methods: list = None,
                     descs: list = None,
                     keys: list = None)
```

Add the instance methods to the paths.

**Arguments**:

- `rsrc_name` (`str`): the resource name
- `schema` (`dict`): the schema for this resource name
- `baseurl` (`str`): the baseurl to use for paths
- `methods` (`list`): optional set of methods to create for
- `keys` (`list`): the keys for the instance of this resource
- `paths` (`dict`): the paths


#### get\_resource\_ops {#firestone.spec.cli.get_resource_ops}

```python
def get_resource_ops(rsrc_name: str,
                     schema: dict,
                     baseurl: str,
                     methods: list = None,
                     descs: list = None,
                     keys: list = None,
                     default_query_params: dict = None)
```

Add resource level methods to the ops.

**Arguments**:

- `rsrc_name` (`str`): the resource name
- `schema` (`dict`): the schema for this resource name
- `baseurl` (`str`): the baseurl to use for ops
- `methods` (`list`): optional set of methods to create for
- `keys` (`list`): the keys for the instance of this resource
- `default_query_params` (`dict`): the ops


#### get\_ops {#firestone.spec.cli.get_ops}

```python
def get_ops(rsrc: dict,
            baseurl: str,
            ops: dict = None,
            keys: list = None,
            default_query_params: dict = None)
```

Get the operations for this resource.


#### generate {#firestone.spec.cli.generate}

```python
def generate(pkg: str,
             client_pkg: str,
             rsrc_data: list,
             title: str,
             desc: str,
             summary: str,
             version: str,
             as_modules: bool = False,
             template: str = None)
```

Generate a Click based CLI script based on the resource data sent and other meta data.


# firestone.spec.streamlit {#firestone.spec.streamlit}

Generate python streamlit WebUI from one or more resource schemas.


#### params\_to\_attrs {#firestone.spec.streamlit.params_to_attrs}

```python
def params_to_attrs(params: list,
                    required: list = None,
                    key_names: list = None)
```

Convert the params from OpenAPI spec to Click attributes.


#### get\_resource\_attrs {#firestone.spec.streamlit.get_resource_attrs}

```python
def get_resource_attrs(schema: dict,
                       params: dict = None,
                       check_required: bool = None,
                       key_names: list = None)
```

Get resource attributes.


#### get\_instance\_ops {#firestone.spec.streamlit.get_instance_ops}

```python
def get_instance_ops(rsrc_name: str,
                     schema: dict,
                     baseurl: str,
                     methods: list = None,
                     descs: list = None,
                     keys: list = None)
```

Add the instance methods to the paths.

**Arguments**:

- `rsrc_name` (`str`): the resource name
- `schema` (`dict`): the schema for this resource name
- `baseurl` (`str`): the baseurl to use for paths
- `methods` (`list`): optional set of methods to create for
- `keys` (`list`): the keys for the instance of this resource
- `paths` (`dict`): the paths


#### get\_resource\_ops {#firestone.spec.streamlit.get_resource_ops}

```python
def get_resource_ops(rsrc_name: str,
                     schema: dict,
                     baseurl: str,
                     methods: list = None,
                     descs: list = None,
                     keys: list = None)
```

Add resource level methods to the ops.

**Arguments**:

- `rsrc_name` (`str`): the resource name
- `schema` (`dict`): the schema for this resource name
- `baseurl` (`str`): the baseurl to use for ops
- `methods` (`list`): optional set of methods to create for
- `keys` (`list`): the keys for the instance of this resource


#### get\_ops {#firestone.spec.streamlit.get_ops}

```python
def get_ops(rsrc: dict, baseurl: str, ops: dict = None, keys: list = None)
```

Get the operations for this resource.


#### generate {#firestone.spec.streamlit.generate}

```python
def generate(rsrc_data: list,
             title: str,
             desc: str,
             summary: str,
             version: str,
             backend_url: str = None,
             as_modules: bool = False,
             template: str = None,
             col_mappings: dict = None)
```

Generate a streamlit based WebUI script based on the resource data sent and other meta data.


# firestone.spec.\_base {#firestone.spec._base}

Base functions for managing spec files


## SchemaMissingAttribute Objects {#firestone.spec._base.SchemaMissingAttribute}

```python
class SchemaMissingAttribute(Exception)
```

Schema is missing an attribute.


#### yaml\_pretty {#firestone.spec._base.yaml_pretty}

```python
def yaml_pretty(data, indent=2)
```

A simple YAML pretty print for Jinja.


#### get\_opid {#firestone.spec._base.get_opid}

```python
def get_opid(path: str, method: str)
```

Get a unique operationId given the path and method.

