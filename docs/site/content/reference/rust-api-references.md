---
title: "Understanding the Rust API References"
weight: 4
---

# Understanding the Rust API References

The Rust projects in the Firestone ecosystem (`bindy` and `bindcar`) have their own auto-generated documentation, separate from the Python `pdoc` reference. These are generated using standard Rust tooling and provide deep insight into the infrastructure layer.

## Bindy: CRD API Reference (`crddoc`)

The `bindy` project's most important public API is its set of Custom Resource Definitions (CRDs). The documentation for these CRDs is not standard `rustdoc` because it needs to be presented in a human-readable, Kubernetes-centric way.

As outlined in `CLAUDE.md`, we use a custom tool, `crddoc`, for this purpose.

### Generating the Bindy CRD Reference

1.  **Navigate to the `bindy` directory**:
    ```bash
    cd bindy/
    ```
2.  **Run the `crddoc` binary**:
    ```bash
    cargo run --bin crddoc > docs/site/content/reference/api.md
    ```

This command:
1.  Analyzes the Rust types in `bindy/src/crd.rs` that define the CRDs.
2.  Uses the `///` documentation comments on the structs and their fields.
3.  Generates a single, large Markdown file: `docs/site/content/reference/api.md`.

This generated Markdown file is then automatically picked up by the main `website` build via the Hugo Content Mounts system.

### How to Contribute
To improve the CRD documentation, you don't edit the Markdown file directly. Instead, you edit the `///` doc comments on the Rust structs and fields in `bindy/src/crd.rs` and then regenerate the file.

## Bindcar: Rustdoc API Reference

The `bindcar` project is a REST API server written in Rust. Its internal API reference is generated using the standard `rustdoc` tool, which is bundled with the Rust toolchain.

### Generating the Bindcar Reference

The `bindcar` Makefile provides a convenient command for this.

1.  **Navigate to the `bindcar` directory**:
    ```bash
    cd bindcar/
    ```
2.  **Run the `docs` command**:
    ```bash
    make docs
    ```

This command runs `cargo doc`, which generates a self-contained HTML website with the full API reference for `bindcar` and all its dependencies.

### Accessing the Bindcar Reference
The output is placed in the `target/doc/` directory within the `bindcar` project. You can open the main page by opening `target/doc/bindcar/index.html` in your browser.

Unlike the `pdoc` and `crddoc` outputs, this `rustdoc` site is **not** integrated into the main Hugo website. It is a separate artifact. The main website may link to it, but it is a standalone piece of documentation.

### How to Contribute
Similar to `bindy`, you improve the `rustdoc` output by editing the `///` and `//!` documentation comments within the `bindcar/src/` source code files. After editing, run `make docs` again to see your changes.
