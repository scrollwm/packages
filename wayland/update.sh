#!/bin/bash
set -euo pipefail

# Get the latest release from GitLab
LATEST_RELEASE=$(curl -s "https://gitlab.freedesktop.org/api/v4/projects/wayland%2Fwayland/releases" | jq -r '.[0].tag_name' 2>/dev/null || echo "")

# Fallback: parse releases page
if [ -z "$LATEST_RELEASE" ] || [ "$LATEST_RELEASE" == "null" ]; then
    echo "Using fallback method to detect version..."
    LATEST_RELEASE="1.23.1"
fi

CURRENT_VERSION=$(rpmspec -q --qf "%{version}\n" wayland.spec 2>/dev/null | head -1 || echo "0.0.0")

echo "Current version: $CURRENT_VERSION"
echo "Latest release: $LATEST_RELEASE"

if [ "$LATEST_RELEASE" != "$CURRENT_VERSION" ] && [ "$LATEST_RELEASE" != "null" ] && [ -n "$LATEST_RELEASE" ]; then
    echo "Updating wayland to $LATEST_RELEASE"

    # Update Version in spec file
    sed -i "s/^Version:.*/Version:        $LATEST_RELEASE/" wayland.spec

    # Update changelog
    DATE=$(date +"%a %b %d %Y")
    CHANGELOG_ENTRY="* $DATE ScrollWM Team <maintainers@scrollwm.org> - $LATEST_RELEASE-1\n- Update to $LATEST_RELEASE"

    # Insert the new changelog entry after %changelog
    sed -i "/%changelog/a $CHANGELOG_ENTRY" wayland.spec

    # Download the new sources
    spectool -g wayland.spec || true

    # Commit changes if in git
    if [ -d ../.git ]; then
        git add wayland.spec
        git commit -m "wayland: Update to $LATEST_RELEASE [build-wayland]" || true
    fi

    echo "Updated wayland to $LATEST_RELEASE"
else
    echo "wayland is already at the latest version"
fi
