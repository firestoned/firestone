+++
title = "API Guides"
weight = 150
description = "Auto-generated API documentation for Firestone's Python libraries."
+++

# API Reference

This section provides detailed, auto-generated API documentation for the Firestone Python libraries. Unlike the narrative guides, which teach you *how* to use Firestone, the API reference documents *what* functions, classes, and modules are available at the code level.

## Documentation Philosophy: Docs from Code

A core principle of the firestoned project is that **API documentation should be generated directly from source code**. This ensures:

- Documentation is always up-to-date with the implementation
- Function signatures match what's actually in the code
- Docstrings drive both IDE tooltips and web documentation
- No drift between docs and reality

## What's Documented Here

### Python Projects
- **firestone** - The main CLI tool
- **firestone-lib** - Shared specification generation library

Documentation is generated using [pdoc](https://pdoc.dev/), which extracts Python docstrings and type hints to create comprehensive API documentation.

### Rust Projects (Referenced)
- **bindy** CRDs - Generated via `crddoc` from Rust types
- **bindcar** API - Standard rustdoc HTML documentation

## Who Should Use This Section

The API reference is intended for:

### Developers Extending Firestone
If you're building a new feature, fixing a bug, or integrating deeply with Firestone's internals, the API reference is essential for understanding the codebase structure.

### Library Users
If you're using `firestone-lib` directly in your own Python code (rather than using the CLI), you'll need the API reference to understand available functions and their signatures.

### Troubleshooters
When a high-level guide doesn't provide enough detail, the API reference gives you the ground truth of what the code actually does.

### Advanced Integrators
If you're building custom templates, plugins, or extensions, you'll need to understand Firestone's internal APIs.

## When to Use the Guides vs the API Reference

**Use the guides** (Getting Started, Resource Schema, etc.) when:
- You're learning how to use Firestone
- You want to understand concepts and workflows
- You need examples and tutorials
- You're following best practices

**Use the API reference** when:
- You need to know exact function signatures
- You're using firestone-lib as a library in your code
- You're debugging or contributing to Firestone
- You need to understand internal implementation details

## Topics Covered

- **[Overview](./overview/)** - About auto-generated API documentation
- **[Generating Python API Reference](./python-pdoc-generation/)** - How to build docs with pdoc
- **[Writing Effective Docstrings](./python-docstrings/)** - Best practices for contributing
- **[Rust API References](./rust-api-references/)** - Links to bindy and bindcar docs

## Accessing the API Documentation

### For Python (firestone, firestone-lib)

The API documentation is generated using pdoc. To build it locally:

```bash
# Install pdoc
pip install pdoc

# Generate docs for firestone-lib
pdoc firestone-lib/firestone_lib -o docs/api/

# Generate docs for firestone
pdoc firestone/firestone -o docs/api/
```

The generated HTML documentation includes:
- Module hierarchies
- Class definitions with methods
- Function signatures with type hints
- Docstring documentation
- Source code links

### For Rust Projects

Rust projects use standard rustdoc:

```bash
# Generate docs for bindy
cd bindy
cargo doc --open

# Generate docs for bindcar
cd bindcar
cargo doc --open
```

## Contributing to API Documentation

The best way to improve the API reference is to improve the **source code docstrings**. When you write clear, comprehensive docstrings, the generated documentation automatically improves.

See **[Writing Effective Docstrings](./python-docstrings/)** for guidelines on writing great documentation in code.


**Remember**: The API reference is comprehensive but not tutorial. For learning, start with the [Getting Started Guide](../getting-started/). Use the API reference when you need precise technical details.