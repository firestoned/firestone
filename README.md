![PR Build](https://github.com/firestoned/firestone/actions/workflows/pr.yml/badge.svg)

# Firestone

Resource-Based Approach to Building APIs

``firestone`` allows you to build OpneAPI, AsyncAPI and gRPC specs based off one or
more resource json schema files. This allows you to focus on what really
matters, the resource you are developing!

Once you have generated the appropriate specfication file for your project, you
can then use the myriad of libraries and fraemworks to geenrate stub code for
you

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
  ``description`` and the given resource file at ``examples/addressbook/resource.yaml``.
- By default, this will output the speciificaton file to stdout, alternatively
  you can provide the `-O` option to output to a specific file.

You can also, add the command line `--ui-server` tot he end, which will launch a
small webserver and run the Swagger UI to view this specification file.

```
firestone generate --title 'Addressbook resource' --description 'A simple addressbook example' --resources examples/addressbook/resource.yaml openapi
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

## Contributing

