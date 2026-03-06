#!/bin/bash

# Pickle Rick's Post-Build Script 🥒
# Copies resources to the build output directory

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Parse arguments
BUILD_PROFILE="release"

for arg in "$@"; do
    case $arg in
        --profile)
            BUILD_PROFILE="$2"
            shift 2
            ;;
    esac
done

# Map profile to directory name
case "$BUILD_PROFILE" in
    dev)
        TARGET_DIR="target/debug"
        ;;
    fast)
        TARGET_DIR="target/fast"
        ;;
    *)
        TARGET_DIR="target/$BUILD_PROFILE"
        ;;
esac

echo "🥒 Post-build: Copying resources..."

# Remove old resources if they exist
rm -rf "$TARGET_DIR/resources"

# Create target directory if it doesn't exist
mkdir -p "$TARGET_DIR"

# Copy resources
cp -r resources/ "$TARGET_DIR/resources"
