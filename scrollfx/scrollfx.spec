%global tag     0.1.8
%global scroll_base 1.11.7

Name:           scrollfx
Version:        0.1.8
Release:        1%{?dist}
Summary:        Scroll window manager with SceneFX eye candy rendering
License:        MIT
URL:            https://github.com/scrollwm/scrollfx
Source0:        %{url}/archive/refs/tags/%{tag}.tar.gz

# Configuration files
Source100:      config.minimal
Source101:      scrollfx-portals.conf

BuildRequires:  gcc-c++
BuildRequires:  meson >= 1.3
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(json-c) >= 0.13
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libevdev)
BuildRequires:  pkgconfig(libinput) >= 1.26.0
BuildRequires:  pkgconfig(libpcre2-8)
BuildRequires:  pkgconfig(libsystemd) >= 239
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(lua) >= 5.4
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(scdoc)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-server) >= 1.23.1
BuildRequires:  pkgconfig(wayland-protocols) >= 1.41
# Require scenefx-0.4 and wlroots-0.19.1
BuildRequires:  pkgconfig(scenefx-0.4) >= 0.4.1
BuildRequires:  pkgconfig(wlroots-0.19) >= 0.19.1
BuildRequires:  pkgconfig(wlroots-0.19) < 0.19.2
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-icccm)
BuildRequires:  pkgconfig(xkbcommon) >= 1.5.0

# Require configuration package
Requires:       %{name}-config
Suggests:       %{name}-config-upstream

# Conflicts with other window managers
Conflicts:      sway
Conflicts:      swayfx
Conflicts:      scroll
Provides:       scroll = %{scroll_base}
Provides:       wayland-compositor

%description
ScrollFX combines the scrolling window manager layout of Scroll with the
eye-candy rendering effects of SceneFX/SwayFX. It is an i3-compatible
Wayland compositor that supports a scrolling layout similar to PaperWM,
niri, or hyprscroller, enhanced with beautiful visual effects.

Features include:
- Scrolling window layout with animations
- SceneFX rendering with blur, shadows, and corner rounding
- Customizable N-order Bezier curve animations
- Independent content scaling for individual windows
- Overview and Jump modes for window management
- Workspace scaling
- Trackpad/Mouse scrolling navigation
- Portrait and landscape monitor support

# Configuration packages
%package        config-upstream
Summary:        Upstream configuration for ScrollFX
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Provides:       %{name}-config = %{version}-%{release}
Conflicts:      %{name}-config

# Essential dependencies
Requires:       mesa-dri-drivers
Requires:       polkit
Requires:       swaybg
Requires:       xorg-x11-server-Xwayland

# Recommended packages
Recommends:     foot
Recommends:     grim
Recommends:     wmenu
Recommends:     sway-systemd
Recommends:     swayidle
Recommends:     swaylock
Recommends:     (qt5-qtwayland if qt5-qtbase-gui)
Recommends:     (qt6-qtwayland if qt6-qtbase-gui)

%description    config-upstream
Upstream configuration for ScrollFX with all recommended dependencies
for a typical desktop system.


%package        config-minimal
RemovePathPostfixes:  .minimal
Summary:        Minimal configuration for ScrollFX
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Provides:       %{name}-config = %{version}-%{release}
Conflicts:      %{name}-config

%description    config-minimal
Minimal configuration for ScrollFX without extra dependencies.
Suitable for headless or buildroot use.


%prep
%autosetup -n %{name}-%{tag}

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
# Create directory for extra config snippets
install -d -m755 -pv %{buildroot}%{_sysconfdir}/%{name}/config.d

%files
%license LICENSE
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/config.d
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
* Tue Oct 28 2025 ScrollWM Team <maintainers@scrollwm.org> - 0.1.7-1
- Update to 0.1.7
* Tue Oct 28 2025 ScrollWM Team <maintainers@scrollwm.org> - 0.1.6-1
- Update to 0.1.6
* Tue Oct 28 2025 ScrollWM Team <maintainers@scrollwm.org> - 0.1.5-1
- Update to 0.1.5
* Mon Oct 27 2025 ScrollWM Team <maintainers@scrollwm.org> - 0.1.2-1
- Updated meson.build
* Mon Oct 27 2025 ScrollWM Team <maintainers@scrollwm.org> - 0.1.0-1
- Initial release of ScrollFX
- Combines Scroll %{scroll_base} with SceneFX rendering
- First stable release with eye-candy effects
