#!/usr/bin/env bash
#
# Type-check firestone's generated rust against a real toolchain.
#
# The python tests can only inspect the generated text; nothing there catches a
# template that stops compiling. This regenerates into a throwaway crate and runs
# cargo test for the two variants that differ structurally:
#
#   1. a ruleset with CEL expressions, built with the cel feature on
#   2. a references-only ruleset, built with --no-default-features
#
# It then runs the committed example crates, which add hand written tests, and the
# generated axum server.
#
# Run it directly, or via `make verify-rust`.
set -euo pipefail

FIRESTONE="${FIRESTONE:-firestone}"

# brew installs it as openapi-generator, the npm wrapper as openapi-generator-cli,
# so take whichever is on PATH rather than assuming one of them.
OPENAPI_GEN="${OPENAPI_GEN:-}"
if [ -z "${OPENAPI_GEN}" ]; then
    for candidate in openapi-generator openapi-generator-cli; do
        if command -v "${candidate}" >/dev/null 2>&1; then
            OPENAPI_GEN="${candidate}"
            break
        fi
    done
fi
WORKDIR="$(mktemp -d)"
trap 'rm -rf "${WORKDIR}"' EXIT

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
RESOURCES="${REPO}/examples/addressbook/addressbook.yaml,${REPO}/examples/addressbook/person.yaml,${REPO}/examples/addressbook/postal_codes.yaml"

# A resource carrying only a reference, so the CEL runtime is never needed. The
# reference names its key explicitly, so the target resource does not have to be
# passed in and cannot smuggle a rule of its own into this variant.
cat > "${WORKDIR}/references_only.yaml" <<'YAML'
kind: tickets
apiVersion: v1
metadata:
  description: A resource whose only rule is a relationship
methods:
  resource: [get, post]
  instance: [get, put]
schema:
  type: array
  key:
    name: ticket_key
    schema:
      type: string
  items:
    type: object
    properties:
      owner:
        type: string
        references:
          kind: persons
          key: first_name
          immutable: true
YAML

build() {
    local name="$1" resources="$2" features="$3"
    local crate="${WORKDIR}/${name}"

    echo "==> ${name} (${features:-default features})"
    mkdir -p "${crate}/src"
    "${FIRESTONE}" generate \
        --title 'Validation type check' \
        --description 'Validation type check' \
        --resources "${resources}" \
        --version 1.0 \
        validations --language rust --output-dir "${crate}/src/validation"

    echo 'pub mod validation;' > "${crate}/src/lib.rs"
    cat > "${crate}/Cargo.toml" <<TOML
[package]
name = "${name}"
version = "0.1.0"
edition = "2021"
rust-version = "1.82"

[dependencies]
async-trait = "0.1"
serde = { version = "1", features = ["derive"] }
serde_json = "1"
cel-interpreter = { version = "0.10", optional = true }

[features]
default = ["cel"]
cel = ["dep:cel-interpreter"]

[dev-dependencies]
tokio = { version = "1", features = ["macros", "rt"] }
TOML

    # shellcheck disable=SC2086
    cargo test --manifest-path "${crate}/Cargo.toml" ${features}
    # shellcheck disable=SC2086
    cargo clippy --manifest-path "${crate}/Cargo.toml" --all-targets ${features} -- -D warnings

    for file in "${crate}"/src/validation/*.rs; do
        rustfmt --edition 2021 --check "${file}" \
            || { echo "generated ${file##*/} is not rustfmt clean"; exit 1; }
    done
}

build with_expressions "${RESOURCES}" ""
build references_only "${WORKDIR}/references_only.yaml" "--no-default-features"

# The committed example crate carries hand written behaviour tests for the parts of
# the engine's contract a rule's examples cannot express, so run those too.
echo "==> committed example crate"
cargo test --manifest-path "${REPO}/examples/addressbook/validation-rs/Cargo.toml"
cargo clippy --manifest-path "${REPO}/examples/addressbook/validation-rs/Cargo.toml" \
    --all-targets --all-features -- -D warnings

# The server is openapi-generator's; this is the implementation firestone writes for
# the traits it declares. Regenerated here so a template that stops compiling, or a
# name the two no longer agree on, fails.
echo "==> generated axum server implementation"
if [ -n "${OPENAPI_GEN}" ]; then
    SERVER="${WORKDIR}/server"
    mkdir -p "${SERVER}"
    "${FIRESTONE}" generate \
        --title 'Server type check' --description 'Server type check' \
        --resources "${RESOURCES}" --version 1.0 \
        openapi > "${WORKDIR}/openapi.yaml"
    "${OPENAPI_GEN}" generate -i "${WORKDIR}/openapi.yaml" -g rust-axum \
        -o "${SERVER}/api" --skip-validate-spec \
        -p packageName=type_check_api,packageVersion=1.0.0 >/dev/null
    "${FIRESTONE}" generate \
        --title 'Server type check' --description 'Server type check' \
        --resources "${RESOURCES}" --version 1.0 \
        server --pkg type_check_server --api-pkg type_check_api \
        --output-dir "${SERVER}/app"
    cat > "${SERVER}/Cargo.toml" <<'TOML'
[workspace]
members = ["api", "app"]
resolver = "2"
TOML
    cargo clippy --manifest-path "${SERVER}/Cargo.toml" --all-targets -- -D warnings
    cargo test --manifest-path "${SERVER}/Cargo.toml"

    # A schema whose operation set differs from the addressbook's exercises other
    # branches of the handlers template, and other import sets. The example alone
    # would let a two-line schema ship broken.
    # Every shape declares methods.resource explicitly, because leaving it out
    # defaults to all of them and so always produces a POST body: that hid a
    # missing models import for any schema with path params and no body.
    for shape in "resource: [post]" \
                 "resource: [get]" \
                 "resource: [get, delete]" \
                 "resource: [get]
  instance: [get]" \
                 "resource: [get]
  instance: [get, delete]" \
                 "resource: [get]
  instance_attrs: [get]" \
                 "resource: [head]
  instance: [head]" \
                 "resource: [delete]
  instance: [get]" \
                 "instance: [get, delete]" \
                 "instance: [head]" \
                 "instance_attrs: [get, put, delete]"; do
        # Printed so a failure in CI names the shape that produced it.
        echo "    shape: methods.${shape}" | tr '\n' ' '
        echo
        cat > "${WORKDIR}/shape.yaml" <<YAML
kind: things
apiVersion: v1
metadata:
  description: One operation set
methods:
  ${shape}
schema:
  type: array
  key:
    name: thing_key
    schema:
      type: string
  items:
    type: object
    properties:
      name:
        type: string
YAML
        rm -rf "${WORKDIR}/shape"
        mkdir -p "${WORKDIR}/shape"
        "${FIRESTONE}" generate --title S --description S --version 1.0 \
            --resources "${WORKDIR}/shape.yaml" openapi > "${WORKDIR}/shape.json"
        "${OPENAPI_GEN}" generate -i "${WORKDIR}/shape.json" -g rust-axum \
            -o "${WORKDIR}/shape/api" --skip-validate-spec \
            -p packageName=shape_api,packageVersion=1.0.0 >/dev/null
        "${FIRESTONE}" generate --title S --description S --version 1.0 \
            --resources "${WORKDIR}/shape.yaml" \
            server --pkg shape_app --api-pkg shape_api \
            --output-dir "${WORKDIR}/shape/app"
        cat > "${WORKDIR}/shape/Cargo.toml" <<'TOML'
[workspace]
members = ["api", "app"]
resolver = "2"
TOML
        cargo clippy --manifest-path "${WORKDIR}/shape/Cargo.toml" \
            --all-targets -- -D warnings
        # Not only clippy: a generated test that panics is a generator bug too.
        cargo test --manifest-path "${WORKDIR}/shape/Cargo.toml"
    done
elif [ -n "${CI:-}" ]; then
    # CI installs it, so missing here means the step that does was dropped and this
    # whole leg would quietly stop running.
    echo "no openapi-generator on PATH, and this is CI" >&2
    exit 1
else
    echo "    skipped: openapi-generator is not installed"
fi

echo "==> committed example server"
cargo clippy --manifest-path "${REPO}/examples/addressbook/server-rs/Cargo.toml" \
    --all-targets --all-features -- -D warnings
cargo test --manifest-path "${REPO}/examples/addressbook/server-rs/Cargo.toml"
cargo fmt --manifest-path "${REPO}/examples/addressbook/server-rs/Cargo.toml" --all --check

echo "==> committed example validation crate is formatted"
cargo fmt --manifest-path "${REPO}/examples/addressbook/validation-rs/Cargo.toml" --check

echo "==> generated rust type check clean"
