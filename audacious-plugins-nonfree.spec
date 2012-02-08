%global aud_plugin_api %(grep '[ ]*#define[ ]*_AUD_PLUGIN_VERSION[ ]\\+' %{_includedir}/audacious/plugin.h 2>/dev/null | sed 's!.*_AUD_PLUGIN_VERSION[ ]*\\([0-9]\\+\\).*!\\1!')
%if 0%{aud_plugin_api} > 0
%global aud_plugin_dep Requires: audacious(plugin-api)%{?_isa} = %{aud_plugin_api}
%endif

Name:           audacious-plugins-nonfree
Version:        3.0.4
Release:        2%{?dist}
Summary:        Audacious media player plugins with non free dependencies
Group:          Applications/Multimedia
License:        GPLv3
URL:            http://audacious-media-player.org/
Source0:        http://distfiles.atheme.org/audacious-plugins-%{version}.tar.gz
Source1:        audacious-sid.desktop
BuildRequires:  audacious-devel >= %{version}
BuildRequires:  zlib-devel, libxml2-devel, desktop-file-utils >= 0.9
BuildRequires:  taglib-devel >= 1.4
BuildRequires:  gettext, libbinio-devel
BuildRequires:  dbus-devel >= 0.60, dbus-glib-devel >= 0.60
BuildRequires:  libsidplay-devel
BuildRequires:  sidplay-libs-devel >= 2.1.1-11
Requires(post):  desktop-file-utils >= 0.9
Requires(postun): desktop-file-utils >= 0.9
%{?aud_plugin_dep}
# People who have the non free repo enabled and have the audacious sid plugin
# installed likely will want this package's sid plugin which is compiled with
# support for both the free libsidplay v1 and the non free libsidplay v2
Obsoletes:      audacious-plugins-sid <= %{version}
# Note we add a .1 to avoid self obsoletion
Provides:       audacious-plugins-sid = %{version}.1

%description
This package contains plugins for the Audacious media player which have
non free dependencies.


%prep
%setup -q -n audacious-plugins-%{version}
sed -i '\,^.SILENT:,d' buildsys.mk.in


%build
%configure \
        --disable-rpath \
        --enable-chardet \
        --disable-altivec \
        --disable-dependency-tracking
make V=1 %{?_smp_mflags} -C src/sid


%install
make -C src/sid install DESTDIR=$RPM_BUILD_ROOT

desktop-file-install --vendor "" \
    --dir $RPM_BUILD_ROOT%{_datadir}/applications   \
    %{SOURCE1}

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'


%post
update-desktop-database %{_datadir}/applications

%postun
update-desktop-database %{_datadir}/applications


%files
%doc COPYING
%{_libdir}/audacious/Input/sid.so
%{_datadir}/applications/audacious-sid.desktop


%changelog
* Thu Feb 09 2012 Nicolas Chauvet <kwizart@gmail.com> - 3.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov  3 2011 Hans de Goede <j.w.r.degoede@gmail.com> 3.0.4-1
- Upgrade to 3.0.4

* Wed Sep  7 2011 Hans de Goede <j.w.r.degoede@gmail.com> 3.0.2-1
- Initial rpmfusion package
