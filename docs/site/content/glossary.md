+++
title = "Glossary"
weight = 170
description = "Definitions of key terms and concepts used throughout the Firestone ecosystem."
+++

## Key Terms

### AsyncAPI
An open-source initiative that seeks to improve the current state of Event-Driven Architectures (EDA). It provides a specification that allows you to define asynchronous APIs (using message brokers like Kafka, RabbitMQ, MQTT, WebSockets, etc.) in a machine-readable format. Firestone generates AsyncAPI documents from resource definitions.

### Blueprint (Resource Blueprint)
The YAML file where you define your resource's schema, metadata, methods, and other configuration. This is the "source of truth" for Firestone. Also referred to as "Resource Schema" or "Resource Definition".

### CLI (Command Line Interface)
A text-based interface used to interact with software and operating systems. Firestone can generate a Python-based CLI tool (using the Click library) that allows users to interact with your API directly from their terminal.

### Firestone
The core CLI tool (`firestone`) that reads resource blueprints and generates various outputs (OpenAPI, AsyncAPI, CLI, UI).

### firestone-lib
The underlying Python library that powers the `firestone` CLI. It can be imported and used directly in other Python projects for programmatic generation capabilities.

### JSON Schema
A vocabulary that allows you to annotate and validate JSON documents. Firestone uses JSON Schema to define the structure of resources (fields, types, validation rules).

### Kind
A string identifier for a resource (e.g., `book`, `user`). It is a required field in the resource blueprint and is used to generate URL paths, CLI commands, and documentation tags.

### Metadata
A section in the resource blueprint used to provide human-readable descriptions and other non-functional information about the resource.

### OpenAPI
A standard specification for describing RESTful APIs. Previously known as Swagger. Firestone generates OpenAPI 3.0+ specifications.

### Resource
An abstract entity that your API manages. Examples include `Users`, `Products`, `Orders`. In RESTful design, resources are the nouns of the API.

### Streamlit
An open-source Python framework for data apps. Firestone can generate a Streamlit application that serves as an interactive UI for managing your resources.

### Swagger UI
A popular tool that renders OpenAPI specifications as interactive documentation, allowing users to visualize and test API endpoints in a browser. Firestone includes a built-in command to serve Swagger UI.
