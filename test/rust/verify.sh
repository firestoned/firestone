#!/usr/bin/env bash
#
# Type-check the generated rust validation package against a real toolchain.
#
# The python tests can only inspect the generated text; nothing there catches a
# template that stops compiling. This regenerates into a throwaway crate and runs
# cargo test for the two variants that differ structurally:
#
#   1. a ruleset with CEL expressions, built with the cel feature on
#   2. a references-only ruleset, built with --no-default-features
#
# It then runs the committed example crate, which adds hand written behaviour tests.
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

echo "==> generated rust validations type check clean"
