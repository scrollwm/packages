
%global tag     1.12

Name:           scroll
Version:        1.12
Release:        1%{?dist}
Summary:        i3-compatible Wayland compositor with a scrolling layout
License:        MIT
URL:            https://github.com/dawsers/scroll
Source0:        %{url}/archive/refs/tags/%{tag}.tar.gz

# Minimal configuration file for headless or buildroot use
Source100:      config.minimal
Source101:      scroll-portals.conf
Source102:      50-systemd-user.conf

BuildRequires:  gcc-c++
BuildRequires:  meson >= 1.3
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(json-c) >= 0.13
BuildRequires:  pkgconfig(libdrm) >= 2.4.122
BuildRequires:  pkgconfig(libevdev)
BuildRequires:  pkgconfig(libinput) >= 1.26.0
BuildRequires:  pkgconfig(libpcre2-8)
BuildRequires:  pkgconfig(libsystemd) >= 239
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(lua) >= 5.4
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(pixman-1) >= 0.43.0
BuildRequires:  pkgconfig(scdoc)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-server) >= 1.23.1
BuildRequires:  pkgconfig(wayland-protocols) >= 1.41
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-icccm)
BuildRequires:  pkgconfig(xkbcommon) >= 1.5.0

# wlroots 0.20 dependencies (scroll 1.12+ uses its own wlroots fork)
# These are needed because scroll includes wlroots in the source tree
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gbm) >= 17.1.0
BuildRequires:  pkgconfig(hwdata)
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  (pkgconfig(libdisplay-info) >= 0.1.1 with pkgconfig(libdisplay-info) < 0.3)
BuildRequires:  (pkgconfig(libliftoff) >= 0.5.0 with pkgconfig(libliftoff) < 0.6)
BuildRequires:  pkgconfig(libseat)
BuildRequires:  pkgconfig(vulkan) >= 1.2.182
BuildRequires:  pkgconfig(xcb-composite)
BuildRequires:  pkgconfig(xcb-dri3)
BuildRequires:  pkgconfig(xcb-errors)
BuildRequires:  pkgconfig(xcb-ewmh)
BuildRequires:  pkgconfig(xcb-present)
BuildRequires:  pkgconfig(xcb-render)
BuildRequires:  pkgconfig(xcb-renderutil)
BuildRequires:  pkgconfig(xcb-res)
BuildRequires:  pkgconfig(xcb-shm)
BuildRequires:  pkgconfig(xcb-xfixes)
BuildRequires:  pkgconfig(xcb-xinput)
BuildRequires:  pkgconfig(xwayland)
BuildRequires:  glslang

# Require any of the available configuration packages;
# Prefer the -upstream one if none are directly specified in the package manager transaction
Requires:       %{name}-config
Suggests:       %{name}-config-upstream

%description
Scroll is a tiling window manager supporting Wayland compositor protocol and
i3/sway-compatible configuration. The main difference is scroll only supports
one layout, a scrolling layout similar to PaperWM, niri or hyprscroller.

Scroll 1.12 includes major updates:
- Uses its own wlroots fork (based on version 0.20), included in source and statically linked
- New decorations: rounded corner borders, title bars, dynamic shadows with blur, and dimming
- Improved gles2 and vulkan renderers (no decorations for pixman renderer)
- Smoother animation system with improved scheduling
- New fullscreen modes
- Better video recording/screencasting support
- Includes sway 1.12-dev changes
- Numerous bug fixes

Features include:
- Scrolling window layout with smooth animations
- Customizable N-order Bezier curve animations
- Independent content scaling for individual Wayland windows
- Overview and Jump modes for window management
- Workspace scaling
- Trackpad/Mouse scrolling navigation
- Support for both portrait and landscape monitor orientations
- Rounded corners, shadows, blur, and title bars
- Dimming of inactive windows

# Configuration presets:
#
%package        config-upstream
Summary:        Upstream configuration for Scroll
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Provides:       %{name}-config = %{version}-%{release}
Conflicts:      %{name}-config

# Lack of graphical drivers may hurt the common use case
Requires:       mesa-dri-drivers
# Logind needs polkit to create a graphical session
Requires:       polkit
# swaybg is used in the default config
Requires:       swaybg
# dmenu (as well as rxvt any many others) requires XWayland on Scroll
Requires:       xorg-x11-server-Xwayland

# Scroll binds the terminal shortcut to one specific terminal. In our case foot
Recommends:     foot
# grim is the recommended way to take screenshots on scroll 1.0+
Recommends:     grim
# wmenu is the default launcher in scroll
Recommends:     wmenu
# Install configs and scripts for better integration with systemd user session
Recommends:     sway-systemd
# Both utilities are suggested in the default configuration
Recommends:     swayidle
Recommends:     swaylock

# Minimal installation doesn't include Qt Wayland backend
Recommends:     (qt5-qtwayland if qt5-qtbase-gui)
Recommends:     (qt6-qtwayland if qt6-qtbase-gui)

%description    config-upstream
Upstream configuration for Scroll.
Includes all important dependencies for a typical desktop system
with minimal or no divergence from the upstream.


%package        config-minimal
RemovePathPostfixes:  .minimal
Summary:        Minimal configuration for Scroll
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Provides:       %{name}-config = %{version}-%{release}
Conflicts:      %{name}-config
# List of dependencies for headless or buildroot use

%description    config-minimal
Minimal configuration for Scroll without any extra dependencies.
Suitable for headless or buildroot use.


%prep
%autosetup -n %{name}-%{tag} -p1


%build
%meson \
    -Dsd-bus-provider=libsystemd \
    -Dwerror=false
%meson_build

%install
%meson_install

# Remove wallpaper assets to prevent unpackaged files error
rm -rf %{buildroot}%{_datadir}/backgrounds 2>/dev/null || true

# Install minimal configuration file
install -D -m644 -pv %{SOURCE100} %{buildroot}%{_sysconfdir}/%{name}/config.minimal
# Install portals.conf for xdg-desktop-portal
install -D -m644 -pv %{SOURCE101} %{buildroot}%{_datadir}/xdg-desktop-portal/%{name}-portals.conf
# Install systemd integration
install -D -m644 -pv %{SOURCE102} %{buildroot}%{_sysconfdir}/%{name}/config.d/50-systemd-user.conf
# Create directory for extra config snippets
install -d -m755 -pv %{buildroot}%{_sysconfdir}/%{name}/config.d

%files
%license LICENSE
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/config.d
%config(noreplace) %{_sysconfdir}/%{name}/config.d/50-systemd-user.conf
%{_mandir}/man1/%{name}*
%{_mandir}/man5/*
%{_mandir}/man7/*
%caps(cap_sys_nice=ep) %{_bindir}/%{name}
%{_bindir}/%{name}bar
%{_bindir}/%{name}msg
%{_bindir}/%{name}nag
%dir %{_datadir}/xdg-desktop-portal
%{_datadir}/xdg-desktop-portal/%{name}-portals.conf
%{bash_completions_dir}/%{name}*
%{fish_completions_dir}/%{name}*.fish
%{zsh_completions_dir}/_%{name}*

%files config-upstream
%config(noreplace) %{_sysconfdir}/%{name}/config
%{_datadir}/wayland-sessions/%{name}.desktop

%files config-minimal
%config(noreplace) %{_sysconfdir}/%{name}/config.minimal

%changelog
* Fri Nov 21 2025 ScrollWM Team <maintainers@scrollwm.org> - 1.12-1
- Update to 1.12
* Mon Oct 27 2025 ScrollWM Team <maintainers@scrollwm.org> - 1.11.8-1
- Update to 1.11.8
* Mon Oct 27 2025 ScrollWM Team <maintainers@scrollwm.org> - 1.11.7-1
- Backup scroll package in scrollwm repository
