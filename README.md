UPDATE : no longer working on scrollfx

# ScrollWM Packages - Setup Guide

## Overview

This repository provides automated building and version tracking for ScrollWM packages via COPR and GitHub Actions.

## File Structure Created

```
scrollwm-packages/
├── .copr/
│   └── Makefile                    # COPR build automation
├── .github/
│   └── workflows/
│       ├── build.yml               # Package building workflow
│       └── update.yml              # Version checking workflow
├── COPR/
│   └── scenefx/                    # SceneFX (latest, wlroots 0.19)
├── scrollfx/
│   ├── scrollfx.spec
│   ├── config.minimal
│   ├── scrollfx-portals.conf
│   └── update.sh
├── scroll/
│   ├── scroll.spec
│   ├── config.minimal
│   ├── scroll-portals.conf
│   └── update.sh
└── README.md
```
└── README.md
```

## GitHub Secrets Required

You need to configure the following secrets in your GitHub repository settings:

### 1. COPR_CONFIG (Required)

Your COPR configuration file for authenticating with the COPR API.

**How to obtain:**

1. Log into https://copr.fedorainfracloud.org/
2. Go to Settings → API
3. Generate/view your API token
4. Copy the entire configuration block

**Format:**
```ini
[copr-cli]
login = your_username
username = scrollwm
token = your_very_long_token_here
copr_url = https://copr.fedorainfracloud.org
```

**How to add to GitHub:**
1. Go to your repository on GitHub
2. Navigate to: Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Name: `COPR_CONFIG`
5. Value: Paste your entire COPR config (including the `[copr-cli]` line)
6. Click "Add secret"

### 2. GITHUB_TOKEN (Automatic)

This is automatically provided by GitHub Actions. No configuration needed.

## COPR Setup (Web Dashboard)

### Step 1: Create COPR Project

1. Go to https://copr.fedorainfracloud.org/
2. Click "New Project"
3. Fill in:
   - **Project name:** `packages`
   - **Owner:** Select `scrollwm` (or create group first)
   - **Chroots:** Select:
     - `fedora-41-x86_64`
     - `fedora-40-x86_64`
     - `fedora-rawhide-x86_64`
   - **Description:** "ScrollWM packages: ScrollFX compositor with SceneFX rendering"
   - **Instructions:** 
     ```
     sudo dnf copr enable scrollwm/packages
     sudo dnf install scrollfx
     ```
4. Click "Create"

### Step 2: Add Packages to COPR

For each package, go to your project page and click "Packages" → "New Package" → "SCM"

#### SceneFX

- **Package name:** `scenefx`
- **Clone URL:** `https://github.com/scrollwm/packages.git`
- **Committish:** `main`
- **Subdirectory:** `COPR/scenefx`
- **Spec File:** `scenefx.rpkg.spec`
- **Type:** `git`
- **Method:** `make_srpm`

#### ScrollFX

- **Package name:** `scrollfx`
- **Clone URL:** `https://github.com/scrollwm/packages.git`
- **Committish:** `main`
- **Subdirectory:** `scrollfx`
- **Spec File:** `scrollfx.spec`
- **Type:** `git`
- **Method:** `make_srpm`

#### Scroll (Backup)

- **Package name:** `scroll`
- **Clone URL:** `https://github.com/scrollwm/packages.git`
- **Committish:** `main`
- **Subdirectory:** `scroll`
- **Spec File:** `scroll.spec`
- **Type:** `git`
- **Method:** `make_srpm`

## GitHub Actions Workflows

### Build Workflow (`.github/workflows/build.yml`)

**Triggers:**
- Manual trigger via "Actions" tab
- Push to main with `[build-all]` or `[build-wayland]` in commit message
- Changes to package files

**What it does:**
1. Builds SceneFX 0.3 and 0.4
2. Builds ScrollFX (after SceneFX 0.4 completes)
3. Builds Scroll
4. Shows build status summary

**Manual trigger:**
1. Go to Actions tab
2. Select "Build ScrollWM Packages"
3. Click "Run workflow"

### Update Workflow (`.github/workflows/update.yml`)

**Triggers:**
- Every 6 hours (automatic)
- Manual trigger via "Actions" tab

**What it does:**
1. Checks GitHub releases for:
   - ScrollFX updates
   - Scroll updates
   - SceneFX 0.4 updates
   - SceneFX 0.3 updates
2. Updates spec files if new versions found
3. Commits with `[build-wayland]` tag to trigger builds
4. Pushes changes

## Testing the Setup

### 1. Verify GitHub Secrets

```bash
# Check if COPR_CONFIG is set (via GitHub UI)
# Settings → Secrets and variables → Actions
# You should see COPR_CONFIG listed
```

### 2. Test Build Workflow

```bash
# Method 1: Commit with trigger
git commit --allow-empty -m "Test build [build-all]"
git push

# Method 2: Manual trigger via GitHub UI
# Go to Actions → Build ScrollWM Packages → Run workflow
```

### 3. Monitor Builds

- **GitHub Actions:** https://github.com/scrollwm/packages/actions
- **COPR Builds:** https://copr.fedorainfracloud.org/coprs/scrollwm/packages/builds/

### 4. Test Installation

```bash
# Enable repository
sudo dnf copr enable scrollwm/packages

# List available packages
dnf list --available | grep -E 'scenefx|scrollfx|scroll'

# Install ScrollFX
sudo dnf install scrollfx scrollfx-config-upstream

# Verify installation
scrollfx --version
```

## Commit Message Conventions

Use these tags in commit messages to trigger builds:

- `[build-all]` - Build all packages
- `[build-wayland]` - Build wayland-related packages (scenefx, scrollfx, scroll)

Example:
```bash
git commit -m "scrollfx: Update configuration [build-wayland]"
```

## Troubleshooting

### Build Fails in GitHub Actions

1. Check Actions log: https://github.com/scrollwm/packages/actions
2. Look for error messages in the build step
3. Common issues:
   - Missing COPR_CONFIG secret
   - Incorrect COPR project name
   - Missing package definitions in COPR

### Build Fails in COPR

1. Go to https://copr.fedorainfracloud.org/coprs/scrollwm/packages/builds/
2. Click on failed build
3. View build logs
4. Common issues:
   - Missing BuildRequires
   - Source download failures
   - Compilation errors

### Packages Not Found After Build

```bash
# Check build status
copr-cli list-builds scrollwm/packages

# Verify repository is enabled
dnf repolist | grep scrollwm

# Regenerate repository metadata
sudo dnf clean all
sudo dnf makecache
```

### Update Workflow Not Running

1. Verify workflow file is in `.github/workflows/update.yml`
2. Check Actions tab for scheduled runs
3. Manually trigger: Actions → Update Package Versions → Run workflow

## Package Dependencies

```
scenefx (wlroots 0.19)
  └── scrollfx
      └── Depends on scenefx

scroll
  └── Independent package (backup/reference)
```

## Maintenance

### Adding a New Package

1. Create package directory with spec file
2. Add update.sh script if applicable
3. Add package to COPR via web interface
4. Update build workflow if needed

### Updating Package Versions

**Automatic:** Update workflow checks every 6 hours

**Manual:**
```bash
cd scrollfx  # or scroll, etc.
./update.sh
git add scrollfx.spec  # or scroll.spec
git commit -m "scrollfx: Update to X.Y.Z [build-wayland]"
git push
```

## Support

- **Issues:** https://github.com/scrollwm/packages/issues
- **COPR:** https://copr.fedorainfracloud.org/coprs/scrollwm/packages/
- **ScrollFX:** https://github.com/scrollwm/scrollfx
- **Scroll:** https://github.com/dawsers/scroll
- **SceneFX:** https://github.com/wlrfx/scenefx

## License

This repository is licensed under MIT License. Individual packages may have different licenses.
