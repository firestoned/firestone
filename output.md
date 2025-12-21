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

<a id="firestone.spec.openapi"></a>

# firestone.spec.openapi

Generate OpenAPI 3.0 Spec

<a id="firestone.spec.openapi.get_responses"></a>

#### get\_responses

```python
def get_responses(method: str,
                  schema: dict,
                  content_type: str,
                  comp_name: str = None,
                  attr_name: bool = None,
                  is_list: bool = None)
```

Set schema for a given operation type.

<a id="firestone.spec.openapi.get_method_op"></a>

#### get\_method\_op

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

<a id="firestone.spec.openapi.get_params"></a>

#### get\_params

```python
def get_params(baseurl: str,
               method: str,
               schema: dict,
               keys: list = None,
               param_schema: dict = None)
```

Get the parameters for this method.

<a id="firestone.spec.openapi.add_resource_methods"></a>

#### add\_resource\_methods

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

<a id="firestone.spec.openapi.add_instance_methods"></a>

#### add\_instance\_methods

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

<a id="firestone.spec.openapi.add_instance_attr_methods"></a>

#### add\_instance\_attr\_methods

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

<a id="firestone.spec.openapi.get_paths"></a>

#### get\_paths

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

<a id="firestone.spec.openapi.add_rsrc_components"></a>

#### add\_rsrc\_components

```python
def add_rsrc_components(components: dict, rsrc_name: str, methods: dict,
                        schema: dict, security: dict)
```

Get the components for this resource.

<a id="firestone.spec.openapi.generate"></a>

#### generate

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

