#!/bin/bash
set -e

# Configuration
# "Gold Standard" Tooling for Zola:
# 1. zola check: Internal structure & integrity (Official Zola recommendation)
# 2. lychee: External link validation (Official Zola recommendation)
#
# STRATEGY:
# This script mirrors the GitHub Actions workflow.
# - CI uses the official 'lycheeverse/lychee-action' for best integration.
# - This script uses the 'lychee' binary for local reproducibility.
# - Both share the same 'lychee.toml' configuration file.

LYCHEE_VERSION="0.20.0"
LYCHEE_URL="https://github.com/lycheeverse/lychee/releases/download/lychee-v${LYCHEE_VERSION}/lychee-x86_64-unknown-linux-musl.tar.gz"
CONFIG_FILE="../lychee.toml"

# Setup local bin directory for caching
SCRIPT_DIR="$(dirname "$0")"
TOOLS_DIR="$SCRIPT_DIR/bin"
mkdir -p "$TOOLS_DIR"
PATH="$TOOLS_DIR:$PATH"

echo "🧪 Testing Firestone Documentation Site (Gold Standard)"
echo "===================================================="

# Ensure we are in the site directory
cd "$SCRIPT_DIR/.."

# ---------------------------------------------------------
# 1. Static Analysis & Internal Integrity
# ---------------------------------------------------------
echo "🔍 Phase 1: Zola Static Analysis"
if ! command -v zola &> /dev/null; then
    echo "  ❌ Zola not found in PATH."
    exit 1
fi

echo "  Running 'zola check'..."
# Note: We allow external link failures here since Lychee handles those better
# with retries and timeout management. Only fail if internal links are broken.
if zola check 2>&1 | tee /tmp/zola-check.log; then
    echo "  ✅ Internal links and anchors valid."
elif grep -q "Successfully checked.*internal link" /tmp/zola-check.log; then
    echo "  ⚠️  External link timeouts detected (will be checked by Lychee)"
    echo "  ✅ Internal links and anchors valid."
else
    echo "  ❌ 'zola check' failed with internal link errors."
    exit 1
fi

# ---------------------------------------------------------
# 2. Build Verification
# ---------------------------------------------------------
echo ""
echo "🏗️  Phase 2: Build Production Site"
# Build to 'public' as normal
if zola build; then
    echo "  ✅ Site built successfully."
else
    echo "  ❌ Build failed."
    exit 1
fi

# ---------------------------------------------------------
# 3. Comprehensive Link Validation (Internal & External)
# ---------------------------------------------------------
echo ""
echo "🔗 Phase 3: Comprehensive Link Validation (Lychee)"

if [ "$SKIP_LYCHEE" = "true" ]; then
    echo "  ⏭️  Skipping Lychee (handled by GitHub Action in CI)..."
else
    # Check if lychee is installed locally
    if ! command -v lychee &> /dev/null; then
            TEMP_LYCHEE_ARCHIVE="$TOOLS_DIR/lychee-v${LYCHEE_VERSION}.tar.gz"
            echo "  Element 'lychee' not found. Downloading v${LYCHEE_VERSION} to $TOOLS_DIR..."
            if curl -fsL "$LYCHEE_URL" -o "$TEMP_LYCHEE_ARCHIVE"; then
                if tar -xzf "$TEMP_LYCHEE_ARCHIVE" -C "$TOOLS_DIR"; then
                    echo "  ✅ Lychee installed."
                else
                    echo "  ❌ Failed to extract Lychee from $TEMP_LYCHEE_ARCHIVE."
                    echo "  Content of downloaded file (first 1000 bytes):"
                    head -c 1000 "$TEMP_LYCHEE_ARCHIVE"
                    rm "$TEMP_LYCHEE_ARCHIVE" # Clean up potentially corrupt archive
                    exit 1
                fi
                rm "$TEMP_LYCHEE_ARCHIVE" # Clean up archive after successful extraction
            else
                echo "  ❌ Failed to download Lychee from $LYCHEE_URL."
                exit 1
            fi    else
        echo "  ✅ Lychee found in $(which lychee)"
    fi

    echo "  Scanning 'public/' directory using config from $CONFIG_FILE..."
    lychee --config "$CONFIG_FILE" ./public

    echo "  ✅ No broken links found."
fi

# ---------------------------------------------------------
# 4. Critical Content Smoke Test
# ---------------------------------------------------------
echo ""
echo "👀 Phase 4: Content Smoke Tests"
required_pages=(
    "public/index.html"
    "public/getting-started/index.html"
    "public/api-reference/index.html"
    "public/404.html"
)

all_exist=true
for page in "${required_pages[@]}"; do
    if [ ! -f "$page" ]; then
        echo "  ❌ Missing critical page: $page"
        all_exist=false
    fi
done

if [ "$all_exist" = true ]; then
    echo "  ✅ Critical pages present."
else
    exit 1
fi

echo ""
echo "========================================"
echo "🎉 Gold Standard Validation Complete!"
