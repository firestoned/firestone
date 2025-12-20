---
title: "Installation"
linkTitle: "Installation"
weight: 1
description: >
  Install firestone using Poetry or pip and verify your installation.
---

## Overview

Firestone can be installed in two ways:

- **Poetry (recommended)** - Best for project-based development and virtual environments
- **pip** - For global installation or quick experimentation

Both methods install the same package, but **Poetry is the officially supported and recommended approach** for the firestone ecosystem.

## Prerequisites

Before installing, ensure you have:

- **Python 3.9 or higher**
  ```bash
  python --version
  # Should show Python 3.9.x or higher
  ```

- **Poetry (recommended)** - [Install Poetry](https://python-poetry.org/docs/#installation)
  ```bash
  poetry --version
  # Should show Poetry 1.2.0 or higher
  ```

  OR

- **pip (alternative)** - Usually comes with Python
  ```bash
  pip --version
  ```

## Installation Methods

### Method 1: Poetry (Recommended)

Poetry is the preferred installation method because it:
- Creates isolated virtual environments automatically
- Manages dependencies cleanly
- Works seamlessly with the firestone ecosystem
- Matches the development workflow used by firestone maintainers

#### For New Projects

If you're starting a new project:

```bash
# Create a new project directory
mkdir my-api-project
cd my-api-project

# Initialize a new Poetry project
poetry init -n

# Add firestone as a dependency
poetry add firestoned

# The package is installed in a virtual environment
# Run firestone commands with 'poetry run'
poetry run firestone --version
```

#### For Existing Poetry Projects

If you already have a Poetry-managed project:

```bash
cd my-existing-project

# Add firestone to your project
poetry add firestoned

# Verify installation
poetry run firestone --version
```

#### Installing from Source

To install the latest development version:

```bash
# Clone the repository
git clone https://github.com/firestoned/firestone.git
cd firestone

# Install dependencies and build
poetry install
poetry build

# Run from source
poetry run firestone --version
```

### Method 2: pip (Alternative)

While Poetry is recommended, pip works fine for global installations or quick experimentation.

#### Global Installation

```bash
# Install globally (may require sudo on Linux/Mac)
pip install firestoned

# Verify installation
firestone --version
```

#### Virtual Environment Installation

It's good practice to use virtual environments even with pip:

```bash
# Create a virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install firestone
pip install firestoned

# Verify installation
firestone --version
```

### The "firestoned" vs "firestone" Package Name

You might have noticed we install `firestoned` (with a 'd') but import and use `firestone` (without a 'd').

**Why?**

The package name `firestone` was already taken on PyPI (though it's essentially empty). So the firestone project publishes as `firestoned` on PyPI, but the Python module is still `firestone`.

**In practice:**

```bash
# Install the package
poetry add firestoned  # Note the 'd'

# Run the CLI
firestone --version  # No 'd'

# Import in Python
import firestone  # No 'd'
```

This is slightly awkward, but it's a one-time learning curve. Once you know, it's straightforward.

## Verifying Installation

After installation, verify everything works:

### Check Version

```bash
# If installed with Poetry
poetry run firestone --version

# If installed with pip (global or venv)
firestone --version
```

You should see output like:
```
firestone, version 0.4.0
```

### Check Help

```bash
poetry run firestone --help
```

You should see the full help output:

```
Usage: firestone [OPTIONS] COMMAND [ARGS]...

  Firestone - Generate OpenAPI, AsyncAPI, and CLI from resource schemas.

Options:
  --debug          Enable debug logging
  --version        Show the version and exit
  --help           Show this message and exit

Commands:
  generate  Generate specifications or code from resource files
```

### Generate a Simple Spec

Test generation with a minimal example:

```bash
# Create a minimal resource file
cat > test-resource.yaml <<EOF
kind: test
apiVersion: v1
metadata:
  description: A test resource
methods:
  resource:
    - get
schema:
  type: array
  key:
    name: id
    schema:
      type: string
  items:
    type: object
    properties:
      name:
        type: string
EOF

# Generate OpenAPI spec
poetry run firestone generate \
    --title "Test API" \
    --resources test-resource.yaml \
    openapi
```

You should see OpenAPI YAML output. If you do, firestone is working correctly!

## Installing Additional Tools

Firestone generates specs and code, but you'll often want additional tools for the full workflow:

### OpenAPI Generator (for client/server code)

```bash
# macOS (Homebrew)
brew install openapi-generator

# Linux (download JAR)
wget https://repo1.maven.org/maven2/org/openapitools/openapi-generator-cli/7.0.0/openapi-generator-cli-7.0.0.jar -O openapi-generator.jar

# Windows (Chocolatey)
choco install openapi-generator

# Verify
openapi-generator version
```

### AsyncAPI Generator (for AsyncAPI specs)

```bash
npm install -g @asyncapi/generator

# Verify
asyncapi --version
```

### Streamlit (for UI generation)

If you plan to use firestone's Streamlit generation:

```bash
# With Poetry
poetry add streamlit

# With pip
pip install streamlit
```

## Common Installation Issues

### Issue: "firestone: command not found"

**Problem:** The firestone binary isn't in your PATH.

**Solutions:**

1. If using Poetry, always run with `poetry run`:
   ```bash
   poetry run firestone --version
   ```

2. If using pip in a virtual environment, ensure it's activated:
   ```bash
   source venv/bin/activate  # Then run firestone
   ```

3. If installed globally with pip, check your Python scripts directory is in PATH:
   ```bash
   python -m site --user-base  # Note the path
   export PATH="$PATH:/path/to/python/scripts"
   ```

### Issue: "No module named 'firestone'"

**Problem:** Package not installed in current environment.

**Solutions:**

1. Check which Python environment is active:
   ```bash
   which python
   ```

2. Install in the correct environment:
   ```bash
   poetry add firestoned  # For Poetry
   # or
   pip install firestoned  # For pip
   ```

### Issue: "ImportError: cannot import name 'X'"

**Problem:** Version mismatch or corrupted installation.

**Solutions:**

1. Reinstall:
   ```bash
   poetry add firestoned --force  # Poetry
   # or
   pip install --force-reinstall firestoned  # pip
   ```

2. Clear cache:
   ```bash
   poetry cache clear --all pypi  # Poetry
   # or
   pip cache purge  # pip
   ```

### Issue: Permission denied (Linux/Mac)

**Problem:** Trying to install globally without permissions.

**Solutions:**

1. Use Poetry (creates venv automatically, no sudo needed):
   ```bash
   poetry add firestoned
   ```

2. Or use pip with --user:
   ```bash
   pip install --user firestoned
   ```

3. Or create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install firestoned
   ```

## Development Installation

If you want to contribute to firestone or modify it:

```bash
# Clone the repository
git clone https://github.com/firestoned/firestone.git
cd firestone

# Install in editable mode with dev dependencies
poetry install

# Run tests
poetry run pytest

# Check formatting
poetry run black --check .

# Run linting
poetry run pylint firestone
```

See the [Developer Guide](../reference) for more details on contributing.

## Upgrading Firestone

### With Poetry

```bash
# Update to latest version
poetry update firestoned

# Or specify a version
poetry add firestoned@^0.5.0
```

### With pip

```bash
# Update to latest
pip install --upgrade firestoned

# Or specify a version
pip install firestoned==0.5.0
```

### Check for Updates

```bash
# Poetry (shows available updates)
poetry show firestoned

# pip (shows current version)
pip show firestoned

# Check PyPI for latest
pip index versions firestoned
```

## Uninstalling

### With Poetry

```bash
poetry remove firestoned
```

### With pip

```bash
pip uninstall firestoned
```

## Next Steps

Now that firestone is installed:

1. **[Complete the Quickstart](./quickstart)** - Build your first resource in 5 minutes
2. **[Learn Resource Anatomy](../core-concepts/resource-schema-anatomy)** - Understand resource structure
3. **[Explore Examples](../examples/)** - See real-world resource definitions

## Getting Help

If you encounter issues:

- **Check the [Troubleshooting Guide](../advanced-topics/troubleshooting-generation-failures.md)**
- **Review [Common Issues](../advanced-topics/troubleshooting-generation-failures.md)**
- **Ask on [GitHub Issues](https://github.com/firestoned/firestone/issues)**
- **File a [Bug Report](https://github.com/firestoned/firestone/issues)**

