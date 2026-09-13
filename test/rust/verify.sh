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
# Run it directly, or via `make verify-validations-rust`.
set -euo pipefail

FIRESTONE="${FIRESTONE:-firestone}"
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

# The server crate is generated from the same resources, so a template that stops
# compiling, or a route that stops matching the schema, fails here.
echo "==> generated axum server"
SERVER="${WORKDIR}/server"
"${FIRESTONE}" generate \
    --title 'Server type check' \
    --description 'Server type check' \
    --resources "${RESOURCES}" \
    --version 1.0 \
    server --pkg type_check_server --output-dir "${SERVER}"

# The server generator does not format, so the documented workflow is applied here
# before anything else looks at the crate.
cargo fmt --manifest-path "${SERVER}/Cargo.toml"
cargo test --manifest-path "${SERVER}/Cargo.toml"
cargo clippy --manifest-path "${SERVER}/Cargo.toml" --all-targets -- -D warnings

echo "==> committed example server crate"
# Committed rather than generated on the fly, so it has to have been formatted. This
# fails when someone regenerates and forgets the cargo fmt that gen-server-rust runs.
cargo fmt --manifest-path "${REPO}/examples/addressbook/server-rs/Cargo.toml" --check
cargo test --manifest-path "${REPO}/examples/addressbook/server-rs/Cargo.toml"
cargo clippy --manifest-path "${REPO}/examples/addressbook/server-rs/Cargo.toml" \
    --all-targets --all-features -- -D warnings

echo "==> committed example validation crate is formatted"
cargo fmt --manifest-path "${REPO}/examples/addressbook/validation-rs/Cargo.toml" --check

echo "==> generated rust type check clean"
