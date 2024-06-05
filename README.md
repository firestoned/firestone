[![Last PR Build 🐍](https://github.com/firestoned/firestone/actions/workflows/pr.yml/badge.svg)](https://github.com/firestoned/firestone/actions/workflows/pr.yml)
<!-- Pytest Coverage Comment:Begin -->
<a href="https://github.com/bradpenney/firestone/blob/main/README.md"><img alt="Coverage" src="https://img.shields.io/badge/Coverage-43%25-orange.svg" /></a>
<!-- Pytest Coverage Comment:End -->

# Firestone

### A Resource-Based Approach to Building APIs

`firestone` allows you to build OpenAPI, AsyncAPI and gRPC specs based off one or more resource JSON schema files. This allows you to focus on what really matters, the resource you are developing!

Once you have generated the appropriate specification file for your project, you can then use the myriad of libraries and frameworks to generate stub code.

**The primary premise of this project is not to introduce any new "language" to describe your resources(s), rather, use JSON Schema!**

This makes it easy to come up to speed with little to no prior knowledge to get going.

Having said that, the schema for a resource provides additional helpful functionality, see the [schema](#schema) section for further details.

## Quick Start

You can use `pip` or `poetry` to install and run `firestone`. We suggest using `pip` if you wish to install `firestone` globally, or for virtual environments, use `poetry`.

### `pip`

It's a simple as running the following `pip` command:

```zsh
sudo pip install firestoned
```

> Yes, `firestone**d**`, not `firestone`! This is because there already is a, albeit emtpy, repository on [pypi.org](https://pypi.org/) with the same name ...

### `poetry`

[Poetry](https://python-poetry.org/) is a great build tool for Python that allows you to build and run all locally in a virtual environment. This is great for checking out the tool and playing around with `firestone` itself.

If you're starting with a new project, declare `firestoned` in your dependencies during the `poetry install` process:

```zsh
poetry install
poetry build
```

If you're adding `firestone` to a `poetry` project:

```zsh
poetry add firestoned
poetry build
```

## Running

Now that you have a copy of `firestone`, let's try running it with the example resource provided, an addressbook!

> If running within `poetry` build, simply prepend commands with `poetry run`.

> For the remainder of this documentation, we will assume you have installed `firestone`.

### Generate an OpenAPI Spec

```zsh
firestone \
    generate \
    --title 'Addressbook resource' \
    --description 'A simple addressBook example' \
    --resources examples/addressBook/resource.yaml \
    openapi
    --security '{"name": "bearer_auth", "scheme": "bearer", "type": "http", "bearerFormat": "JWT"}' \
```

Let's quickly dissect this command:

- We are telling firestone to generate an `openapi` spec, given the `title`, `description`, and the two given resource files.
- By default, this will output the specification file to `stdout`, alternatively, you can provide the `-O` option to output to a specific file.

You can also add the command line `--ui-server` to the end, which will launch a small webserver and run the Swagger UI to view this specification file.

```zsh
firestone --debug generate --title 'Example person and addressBook API' \
    --description 'An example API with more than one resource' \
    --resources examples/addressBook.yaml,examples/person.yaml \
    openapi \
    --security '{"name": "bearer_auth", "scheme": "bearer", "type": "http", "bearerFormat": "JWT"}' \
    --ui-server
# ...
* Serving Quart app 'firestone.__main__'
* Environment: production
* Please use an ASGI server (e.g. Hypercorn) directly in production
* Debug mode: False
* Running on http://127.0.0.1:5000 (CTRL + C to quit)
[2022-10-31 02:47:17 -0500] [87590] [INFO] Running on http://127.0.0.1:5000 (CTRL + C to quit)
# 2022-10-31 02:47:17,120 - [MainThread] hypercorn.error:102 INFO - Running on http://127.0.0.1:5000 (CTRL + C to quit)
```

Now you can use your browser to navigate to `http://127.0.0.1:5000/apidocs` to view the Swagger UI.

## Schema

It all begins with your resource definition! This is done using JSON schema and we have provided an example in our `examples` directory, called addressBook. We will use this to describe how the schema is setup and how you can adapt to your own.

Here is the full file:

```yaml
# Metadata: start
name: addressbook
description: An example of an addressbook resource
version: 1.0
version_in_path: false
default_query_params:
  - name: limit
    description: Limit the number of responses back
    in: query
    schema:
      type: integer
  - name: offset
    description: The offset to start returning resources
    in: query
    schema:
      type: integer
asyncapi:
  servers:
    dev:
      url: ws://localhost
      protocol: ws
      description: The development websocket server
  channels:
    resources: true
    instances: true
    instance_attrs: true
# You can limit the overall HTTP methods for the high level resource endpoint
methods:
  resource:
    - get
    - post
  instance:
    - delete
    - get
    - head
    - put
  instance_attrs:
    - delete
    - get
    - head
    - put
descriptions:
  resource:
    get: List all addresses in this addressbook.
    head: Determine the existence and size of addresses in this addressbook.
    patch: Patch one or more addresses in this addressbook.
    post: Create a new address in this addressbook, a new address key will be created.
    delete: Delete all addresses from this addressbook.
  instance:
    get: Get a specific address from this addressbook.
    head: Determine the existence and size of this address.
    patch: Patch this address in the addressbook.
    put: Update an existing address in this addressbook, with the given address key.
    delete: Delete an address from this addressbook.
# Metadata: end
schema:
  type: array
  key:
    name: address_key
    description: A unique identifier for an addressbook entry.
    schema:
      type: string
  #responseCodes:
  # - 200
  # - 201
  query_params:
    - name: city
      description: Filter by city name
      required: false
      schema:
        type: string
      methods:
        - get
  items:
    type: object
    properties:
      # embeded person
      person:
        description: This is a person object that lives at this address.
        schema:
          $ref: "person.yaml#/schema"
      addrtype:
        description: The address type, e.g. work or home
        type: string
        # Don't expose this attribute in the URL/specification
        # expose: false
        enum:
          - work
          - home
      street:
        description: The street and civic number of this address
        type: string
      city:
        description: The city of this address
        type: string
      state:
        description: The state of this address
        type: string
      country:
        description: The country of this address
        type: string
      people:
        description: A list of people's names living there
        type: array
        items:
          type: string
    required:
      - addrtype
      - street
      - city
      - state
      - country
```

### Schema Metadata Fields

#### `name`

Name is used in various places, including as the root to API URLs, for example in OpenAPI, `/addressBook`

#### `description`

The description of this resource is used in the generated specification files.

#### `version`

The version of this resource definition, this can alternatively be used in the URL as well, see below `version_in_path`.

#### `version_in_path`

This attribute defines whether to prepend the version defined above in the URL paths.  For example, for the
above, you would get: `/v1.0/addressBook`.

#### `default_query_params`

You can provide a list of default query parameters that will be added to all HTTP methods,
or optionally you can provide a list of the HTTP methods, for which `firestone` will add.

#### `methods`

This is a map/dict of `resource`, and/or `instance`, and/or `instance_attrs` (the instance attributes to expose), and a list of methods to explicitly expose.

#### `descriptions`

This is a map/dict of either `resource` and/or `instance`, which itself is a map or methods to descriptions.

### Generate OpenAPI Client

Now, to generate your OpenAPI client, you will need the `openapi-generator` command ([installation instructions](https://openapi-generator.tech/docs/installation) to generate client code in many languages. 

> Please check out the [OpenAPI Project](https://openapi-generator.tech/) for more details.

This client code can then be used as an SDK or used by our CLI generation, for example:

```zsh
openapi-generator generate \
    -i examples/addressbook/openapi.yaml \
    -g python-nextgen \
    -o /tmp/addressbook-client \
    --skip-validate-spec \
    -c examples/addressbook/openapi-gen-config.json
```

### Generate Python CRUD CLI

Now that you have generated the client code, you can also generate a CRUD, Python Click-based CLI around your code. This generator creates a standalone script or as a module to be used in your console scripts, as part of your project build.

> Please checkout the [Click Project](https://click.palletsprojects.com) for more details.

Here is an example command we use to generate the example Addressbook.

```
firestone generate \
    --title 'Addressbook CLI' \
    --description 'This is the CLI for the example Addressbook' \
    --resources examples/addressbook/addressbook.yaml,examples/addressbook/person.yaml \
    --version 1.0 \
     cli \
     --pkg addressbook \
     --client-pkg addressbook.client > examples/addressbook/main.py
```

## Contributing

`firestone` and the larger [**Firestone Project**](https://github.com/firestoned) are open-source projects and we welcome contributions.  Please follow standard GitHub practices, including forking the project, creating a branch, and submitting a PR.
