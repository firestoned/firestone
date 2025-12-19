+++
title = "Running in Docker"
weight = 52
description = "Using the official Firestone Docker image."
+++

## Docker Usage

You can run Firestone without installing Python by using our Docker image. This ensures a consistent environment for generation.

**Pull the Image:**
```bash
docker pull ghcr.io/firestoned/firestone:latest
```

**Generate Spec:**
Mount your current directory (`$(pwd)`) to `/app` in the container to access your resource files.

```bash
docker run --rm -v $(pwd):/app -w /app ghcr.io/firestoned/firestone:latest \
    firestone generate --resources . openapi
```

**Generate Client:**
You can chain this with the official `openapitools/openapi-generator-cli` image:

```bash
# 1. Generate Spec
docker run --rm -v $(pwd):/app -w /app ghcr.io/firestoned/firestone:latest \
    firestone generate --resources . openapi > openapi.yaml

# 2. Generate Client
docker run --rm -v $(pwd):/local openapitools/openapi-generator-cli generate \
    -i /local/openapi.yaml -g python -o /local/client
```