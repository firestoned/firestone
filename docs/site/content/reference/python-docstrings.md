---
title: "Writing Effective Python Docstrings"
weight: 3
---

# Writing Effective Python Docstrings for the API Reference

The quality of the generated Python API reference is directly proportional to the quality of the docstrings in the source code. To contribute effectively, it's important to write clear, concise, and well-formatted docstrings. We follow the **[Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#s3.8-comments-and-docstrings)** for docstrings.

## General Docstring Guidelines

-   Every public module, function, class, and method should have a docstring.
-   The first line should be a short, imperative summary of the function's purpose (e.g., "Generate an OpenAPI specification.").
-   This should be followed by a blank line, and then a more detailed description if necessary.

## Docstring for a Simple Function

For a function, the docstring should describe its arguments, what it returns, and any exceptions it might raise.

```python
def generate_spec(resource: Resource, title: str) -> dict:
    """Generates a complete OpenAPI specification from a resource.

    This function takes a validated resource object and transforms it
    into a dictionary that conforms to the OpenAPI 3.x standard.

    Args:
        resource: A validated Resource object.
        title: The title to be used in the 'info' section of the spec.

    Returns:
        A dictionary representing the complete OpenAPI specification.

    Raises:
        SchemaError: If the resource schema contains invalid structures
            that were not caught by the initial validation.
    """
    # ... function implementation ...
```

### Key Sections:

-   **`Args:`**: List each argument on a new line. The format is `argument_name (type): Description`.
-   **`Returns:`**: Describe the return value of the function. If the function returns a complex type (like a dictionary or object), explain what it represents.
-   **`Raises:`**: List any exceptions that the function is expected to raise during normal operation, and under what conditions.

## Docstring for a Class

For a class, the docstring should summarize its purpose. The `__init__` method should have its own docstring that describes the class's attributes.

```python
class SpecGenerator:
    """Generates API specifications from resource schemas.

    This class encapsulates the logic for different types of specification
    generation, such as OpenAPI and AsyncAPI.

    Attributes:
        output_format: The format for the generated output, e.g., 'json' or 'yaml'.
    """

    def __init__(self, output_format: str = "yaml"):
        """Initializes the SpecGenerator.

        Args:
            output_format: The desired output format for the spec.
                           Defaults to 'yaml'.
        """
        self.output_format = output_format

    def to_openapi(self, resource: Resource) -> str:
        """Converts a resource to an OpenAPI spec string."""
        # ... method implementation ...
```

### Key Sections:

-   **Class Docstring**: A high-level summary of the class's responsibility.
-   **`Attributes:`**: A list of the public attributes of the class. This should be in the class docstring, not the `__init__` docstring.
-   **`__init__` Docstring**: The docstring for the initializer follows the same format as a regular function, describing its `Args`.

By writing detailed and well-structured docstrings, you not only make the code easier to read but also directly contribute to creating a high-quality, comprehensive API reference for all users of Firestone.
