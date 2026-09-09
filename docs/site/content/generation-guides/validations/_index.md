+++
title = "Validations Generation"
weight = 50
description = "Generate a server side validation package that enforces the relationships and rules declared in your resources."
+++

# Validations Generation

## Business Rules, Declared Once

JSON Schema validates a body in isolation. Everything else - an address that may only name a person who exists, a postal code that has to match its city, a flag only an admin may flip, a person you cannot delete while something still points at them - normally ends up hand-written in every handler.

Firestone lets you declare those in the resource file and generates the engine that runs them, for **python or rust**. It never performs the lookups itself: it knows *what* each rule needs, and hands you an interface to say *how* to fetch it. That interface is the only code you write.

The feature is entirely opt-in. Resources that declare no `references` and no `validations` generate exactly what they always did.

### 1. [How Validations Work](./basics)
The two layers, what each is for, and how a rule is evaluated.

### 2. [Generating the Package](./generating)
The `firestone generate validations` command and the files it writes.

### 3. [Implementing a Resolver](./resolvers)
Connecting the rules to your database, in python or rust, and returning the failure.

### 4. [Testing Your Rules](./testing)
Turning examples in the schema into a pytest suite that needs no database.

### 5. [Schema Reference](../../core-concepts/resource-schema/validations)
Every field of the `references` and `validations` blocks.
