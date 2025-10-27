#!/bin/bash
set -euo pipefail

# Get the latest release from GitHub
LATEST_RELEASE=$(curl -s https://api.github.com/repos/scrollwm/scrollfx/releases/latest | jq -r .tag_name)
CURRENT_VERSION=$(rpmspec -q --qf "%{version}\n" scrollfx.spec 2>/dev/null | head -1 || echo "0.0.0")

echo "Current version: $CURRENT_VERSION"
echo "Latest release: $LATEST_RELEASE"

if [ "$LATEST_RELEASE" != "$CURRENT_VERSION" ] && [ "$LATEST_RELEASE" != "null" ]; then
    echo "Updating scrollfx to $LATEST_RELEASE"
    
    # Update Version and tag in spec file
    sed -i "s/^%global tag.*/%global tag     $LATEST_RELEASE/" scrollfx.spec
    sed -i "s/^Version:.*/Version:        $LATEST_RELEASE/" scrollfx.spec
    
    # Update changelog
    DATE=$(date +"%a %b %d %Y")
    CHANGELOG_ENTRY="* $DATE ScrollWM Team <maintainers@scrollwm.org> - $LATEST_RELEASE-1\n- Update to $LATEST_RELEASE"
    
    # Insert the new changelog entry after %changelog
    sed -i "/%changelog/a $CHANGELOG_ENTRY" scrollfx.spec
    
    # Download the new sources
    spectool -g scrollfx.spec || true
    
    # Commit changes if in git
    if [ -d ../.git ]; then
        git add scrollfx.spec
        git commit -m "scrollfx: Update to $LATEST_RELEASE [build-gcc]" || true
    fi
    
    echo "Updated scrollfx to $LATEST_RELEASE"
else
    echo "scrollfx is already at the latest version or no release found"
fi
