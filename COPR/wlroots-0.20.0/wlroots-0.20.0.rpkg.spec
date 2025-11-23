
# vim: syntax=spec

# PINNED VERSION - DO NOT AUTO-UPDATE
# This package is pinned to wlroots 0.20.0 for scroll 1.12+ compatibility

%global abi_ver 0.20
%global pinned_version 0.20.0
# libliftoff does not bump soname on API changes
%global liftoff_ver 0.5.0

Name:           wlroots-0.20.0
Version:        0.20.0
Release:        1%{?dist}
Summary:        A modular Wayland compositor library (pinned to 0.20.0)

# Source files/overall project licensed as MIT, but
# - HPND-sell-variant
#   * protocol/drm.xml
#   * protocol/wlr-data-control-unstable-v1.xml
#   * protocol/wlr-foreign-toplevel-management-unstable-v1.xml
#   * protocol/wlr-gamma-control-unstable-v1.xml
#   * protocol/wlr-input-inhibitor-unstable-v1.xml
#   * protocol/wlr-layer-shell-unstable-v1.xml
#   * protocol/wlr-output-management-unstable-v1.xml
# - LGPL-2.1-or-later
#   * protocol/server-decoration.xml
License:        MIT
URL:            https://gitlab.freedesktop.org/wlroots/wlroots
Source0:        %{url}/-/releases/%{pinned_version}/downloads/wlroots-%{pinned_version}.tar.gz

BuildRequires:  gcc
BuildRequires:  glslang
BuildRequires:  meson >= 0.60.0

BuildRequires:  (pkgconfig(libdisplay-info) >= 0.1.1 with pkgconfig(libdisplay-info) < 0.3)
BuildRequires:  (pkgconfig(libliftoff) >= %{liftoff_ver} with pkgconfig(libliftoff) < 0.6)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gbm) >= 17.1.0
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(hwdata)
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(libdrm) >= 2.4.122
BuildRequires:  pkgconfig(libinput) >= 1.21.0
BuildRequires:  pkgconfig(libseat)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(pixman-1) >= 0.43.0
BuildRequires:  pkgconfig(vulkan) >= 1.2.182
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols) >= 1.41
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(wayland-server) >= 1.23.1
BuildRequires:  pkgconfig(x11-xcb)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-composite)
BuildRequires:  pkgconfig(xcb-dri3)
BuildRequires:  pkgconfig(xcb-errors)
BuildRequires:  pkgconfig(xcb-ewmh)
BuildRequires:  pkgconfig(xcb-icccm)
BuildRequires:  pkgconfig(xcb-present)
BuildRequires:  pkgconfig(xcb-render)
BuildRequires:  pkgconfig(xcb-renderutil)
BuildRequires:  pkgconfig(xcb-res)
BuildRequires:  pkgconfig(xcb-shm)
BuildRequires:  pkgconfig(xcb-xfixes)
BuildRequires:  pkgconfig(xcb-xinput)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(xwayland)
# libliftoff does not bump soname on API changes
Requires:       libliftoff%{?_isa} >= %{liftoff_ver}

# Conflict with other wlroots versions
Conflicts:      wlroots-0.19.1
Conflicts:      wlroots-0.19.2

%description
Pinned version of wlroots 0.20.0 for scroll 1.12+ compatibility.
This package provides a stable wlroots 0.20.0 that will not auto-update.

Scroll 1.12+ uses its own wlroots fork (based on 0.20) that is included
in the source tree and linked statically. This external package is provided
for system integration and to satisfy other packages that may need wlroots-0.20.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} == %{version}-%{release}
Provides:       wlroots-devel = %{version}-%{release}
Conflicts:      wlroots-0.19.1-devel
Conflicts:      wlroots-0.19.2-devel
# not required per se, so not picked up automatically by RPM
Recommends:     pkgconfig(xcb-icccm)
# for examples
Suggests:       gcc
Suggests:       meson >= 0.60.0
Suggests:       pkgconfig(wayland-egl)

%description    devel
Development files for %{name}.


%prep
%autosetup -N -n wlroots-%{pinned_version}


%build
MESON_OPTIONS=(
    # Disable options requiring extra/unpackaged dependencies
    -Dexamples=false
    -Dwerror=false
)

%{meson} "${MESON_OPTIONS[@]}"
%{meson_build}


%install
%{meson_install}


%check
%{meson_test}


%files
%license LICENSE
%doc README.md
%{_libdir}/libwlroots-%{abi_ver}.so


%files  devel
%{_includedir}/wlroots-%{abi_ver}/wlr
%{_libdir}/pkgconfig/wlroots-%{abi_ver}.pc


%changelog
* Mon Nov 23 2025 ScrollWM Team <maintainers@scrollwm.org> - 0.20.0-1
- Initial pinned package for scroll 1.12+
- Pinned to wlroots 0.20.0 for scroll compatibility
- Note: Scroll 1.12+ includes its own statically-linked wlroots fork
