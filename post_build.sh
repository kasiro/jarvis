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

TARGET_DIR="target/$BUILD_PROFILE"

echo "🥒 Post-build: Copying resources to $TARGET_DIR..."

# Remove old resources if they exist
rm -rf "$TARGET_DIR/resources"

# Create target directory if it doesn't exist
mkdir -p "$TARGET_DIR"

# Copy resources
cp -r resources/ "$TARGET_DIR/resources"

echo "✓ Resources copied to $TARGET_DIR/resources/"
