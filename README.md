[![Last PR Build 🐍](https://github.com/firestoned/firestone/actions/workflows/pr.yml/badge.svg)](https://github.com/firestoned/firestone/actions/workflows/pr.yml)
<!-- Pytest Coverage Comment:Begin -->
<a href="https://github.com/firestoned/firestone/blob/main/README.md"><img alt="Coverage" src="https://img.shields.io/badge/Coverage-14%25-red.svg" /></a>
<!-- Pytest Coverage Comment:End -->

# Firestone

Resource-Based Approach to Building APIs

``firestone`` allows you to build OpneAPI, AsyncAPI and gRPC specs based off one or
more resource json schema files. This allows you to focus on what really
matters, the resource you are developing!

Once you have generated the appropriate specfication file for your project, you
can then use the myriad of libraries and fraemworks to geenrate stub code for
you.

**The primary premise of this project is not to introdue any new "language" to describe your
resources(s), use JSON Schema!**

THis makes it easy to come up to speed and little to no prior knowledge to get
going.

Having said that, the schema for a resource provides additional helpful functionality,
see [schema](#schema) section.

## Quick Start

You can use pip or poetry to run and use ``firestone``. We suggest using pip if you wish to install
`firestone`` machine-wode, else, for local use, use poetry.

### pip

It's a simple as running the following ``pip`` command:

```
sudo pip install firestone
```

### poetry

[Poetry](https://python-poetry.org/) is a great build tool for python that
allows you to build and run all locally in a virtual environment. This is great
for checking out the tool and playiong around.

```
brew install poetry
poetry install
poetry build
```

## Running

Now that you have a copy of ``firestone``, let's try running it wihtt he
example reosouce rpovided, an addressbook!

Note: if running wihtin poetry build, simply prepend commands with ``poetry run``

### Generate an OpenAPI Spec

```
firestone generate --title 'Addressbook resource' --description 'A simple addressbook example' --resources examples/addressbook/resource.yaml openapi
```

Let's quickly disect this command:

- we are telling firestone to generate an `openapi` spec, given the ``title``,
  ``description`` and the two given resource files.
- By default, this will output the speciificaton file to stdout, alternatively
  you can provide the `-O` option to output to a specific file.

You can also, add the command line `--ui-server` tot he end, which will launch a
small webserver and run the Swagger UI to view this specification file.

```
poetry run firestone --debug generate --title 'Example person and addressbook API' \
    --description 'An example API with more than one resource' \
    --resources examples/addressbook.yaml,examples/person.yaml \
    openapi \
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

Now you can use your browser to navigate to `http://127.0.0.1:5000/apidocs`

## Schema

It all begins with your resource definition! This is done usign JSON schema and
we have provided an example in our `examples` directory, called addressbook. We
will use this to describe how the schema is setup and how you can adapt to your
own.

Here is the full file:

```yaml
name: addressbook
description: An example of an addressbook resource
version: 1.0
versionInPath: false
schema:
  type: array
  key:
    name: address_key
    schema:
      description: A unique identitfier for an addressbook entry.
      type: string
  # You can limit the overal HTTP methods for the high level resource endpoint
  #methods:
  #  - get
  #responseCodes:
  # - 200
  # - 201
  query_params:
    - name: city
      description: Filter by city name
      schema:
        type: string
      methods:
        - get
  descriptions:
    get: List all addresses in this addressbook
    head: Determine the existence and size of addresses in this addressbook
    patch: Patch one or more addresses in this addressbook
    post: Create a new address in this addressbook, a new address key will be created
  items:
    descriptions:
      get: Get a specific address from this addressbook
      head: Determine the existence and size of this address
      patch: Patch this address in the addressbook
      put: Put a new address in this addressbook, with the given address key
    type: object
    properties:
      addrtype:
        description: The address type, e.g. work or home
        type: string
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
```

### Metadata

There is a certain amount of metadata that all of hese specifications
use/require, and this is done at the top of the resource,yaml; for posterity,
they are:

```yaml
name: addressbook
description: An example of an addressbook resource
version: 1.0
```

#### `name`

The name is used in various places, including as the root to API URLs, for
example in OpenAPI, `/addressbook`

#### `description`

This is self evident, I hope, the description of this resource and is used nt he
generated sopecification files.

#### `version`

The verison of this resource definition, this cna alternatively be used in the
URL as well, see beloe `versionInPath`

#### `versionInPath`

This attribute defines whether to prepend the version defined above in the URL paths, e.g., for the
above, you woudl get: `/v1.0/addressbook`.

## Contributing
