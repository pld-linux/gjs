#
# Conditional build:
%bcond_without	sysprof		# sysprof profiling
%bcond_without	systemtap	# systemtap/dtrace trace support
#
Summary:	JavaScript bindings for GNOME
Summary(pl.UTF-8):	Wiązania JavaScriptu dla GNOME
Name:		gjs
Version:	1.86.0
Release:	1
License:	MIT and (MPL v1.1 or GPL v2+ or LGPL v2+)
Group:		Libraries
Source0:	https://download.gnome.org/sources/gjs/1.86/%{name}-%{version}.tar.xz
# Source0-md5:	e11b56c1f8938a544000db4cbec31e39
URL:		https://gitlab.gnome.org/GNOME/gjs/-/wikis/Home
BuildRequires:	cairo-devel
BuildRequires:	cairo-gobject-devel
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.86.0
BuildRequires:	gobject-introspection-devel >= 1.72.0
BuildRequires:	libffi-devel
# C++17, but gcc<12 hits https://gcc.gnu.org/bugzilla/show_bug.cgi?id=67829
BuildRequires:	libstdc++-devel >= 6:12
BuildRequires:	meson >= 1.4
BuildRequires:	mozjs140-devel >= 140
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	readline-devel
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.042
# pkgconfig(sysprof-capture-4)
%{?with_sysprof:BuildRequires:	sysprof-devel >= 3.36}
%{?with_systemtap:BuildRequires:	systemtap-sdt-devel}
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	glib2 >= 1:2.86.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# dtrace script expects CPP to be cpp, not "gcc -E", so force it regardless of rpm version
# (autotools-based rpm<4.19 used to have "gcc -E", cmake builds for 4.19+ switched to cpp)
%define		__cpp	cpp

%description
Gjs allows using GNOME libraries from JavaScript. It is mainly based
on Spidermonkey JavaScript engine and the GObject introspection
framework.

%description -l pl.UTF-8
Gjs pozwala używać bibliotek GNOME z JavaScriptem. Jest oparty głównie
na silniku JavaScriptu Spidermonkey i systemie GObject introspection.

%package devel
Summary:	Header files for gjs library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki gjs
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	cairo-devel
Requires:	cairo-gobject-devel
Requires:	glib2-devel >= 1:2.86.0
Requires:	gobject-introspection-devel >= 1.72.0
Requires:	libffi-devel
Requires:	mozjs140-devel >= 140

%description devel
Header files for gjs library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki gjs.

%package -n systemtap-gjs
Summary:	systemtap/dtrace probes for gjs
Summary(pl.UTF-8):	Sondy systemtap/dtrace dla gjs
Group:		Development/Tools
Requires:	%{name} = %{version}-%{release}
Requires:	systemtap-client
BuildArch:	noarch

%description -n systemtap-gjs
systemtap/dtrace probes for gjs.

%description -n systemtap-gjs -l pl.UTF-8
Sondy systemtap/dtrace dla gjs.

%prep
%setup -q

%build
# <mozilla/UniquePtrExtensions.h> included from some mozjs headers expects platform configuration flags
CXXFLAGS="%{rpmcxxflags} -DXP_UNIX=1"
%meson \
	-Ddtrace=%{__true_false systemtap} \
	-Dinstalled_tests=false \
	-Dreadline=enabled \
	-Dprofiler=%{__enabled_disabled sysprof} \
	-Dskip_gtk_tests=true \
	-Dsystemtap=%{__true_false systemtap}

%meson_build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%meson_install

cp -p examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

# still present with -Dinstalled_tests=false
%{__rm} -r $RPM_BUILD_ROOT%{_libexecdir}/installed-tests

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING NEWS README.md
%attr(755,root,root) %{_bindir}/gjs
%attr(755,root,root) %{_bindir}/gjs-console
%attr(755,root,root) %{_libdir}/libgjs.so.*.*.*
%ghost %{_libdir}/libgjs.so.0
%dir %{_libdir}/gjs
%dir %{_libdir}/gjs/girepository-1.0
%{_libdir}/gjs/girepository-1.0/GjsPrivate-1.0.typelib
%{_datadir}/gjs-1.0

%files devel
%defattr(644,root,root,755)
%{_libdir}/libgjs.so
%{_includedir}/gjs-1.0
%{_pkgconfigdir}/gjs-1.0.pc
%{_examplesdir}/%{name}-%{version}

%if %{with systemtap}
%files -n systemtap-gjs
%defattr(644,root,root,755)
%{_datadir}/systemtap/tapset/gjs.stp
%endif
