#
# Conditional build:
%bcond_without	systemtap	# systemtap/dtrace trace support
#
Summary:	JavaScript bindings for GNOME
Summary(pl.UTF-8):	Wiązania JavaScriptu dla GNOME
Name:		gjs
Version:	1.56.2
Release:	1
License:	MIT and (MPL v1.1 or GPL v2+ or LGPL v2+)
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gjs/1.56/%{name}-%{version}.tar.xz
# Source0-md5:	6744153c56e958ad496021062e21823f
Patch0:		%{name}-noc++17.patch
URL:		https://wiki.gnome.org/Projects/Gjs
BuildRequires:	autoconf >= 2.64
BuildRequires:	automake >= 1:1.11.1
BuildRequires:	cairo-devel
BuildRequires:	cairo-gobject-devel
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.54.0
BuildRequires:	gobject-introspection-devel >= 1.41.4
BuildRequires:	gtk+3-devel >= 3.20
BuildRequires:	libffi-devel
BuildRequires:	libstdc++-devel >= 6:5.0
BuildRequires:	libtool >= 2:2.2.0
BuildRequires:	mozjs60-devel >= 60
BuildRequires:	pkgconfig
BuildRequires:	readline-devel
%{?with_systemtap:BuildRequires:	systemtap-sdt-devel}
Requires:	glib2 >= 1:2.54.0
Requires:	gtk+3 >= 3.20
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
Requires:	glib2-devel >= 1:2.54.0
Requires:	gobject-introspection-devel >= 1.41.4
Requires:	gtk+3-devel >= 3.20
Requires:	libffi-devel
Requires:	mozjs60-devel >= 60

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

%description -n systemtap-gjs
systemtap/dtrace probes for gjs.

%description -n systemtap-gjs -l pl.UTF-8
Sondy systemtap/dtrace dla gjs.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{?with_systemtap:--enable-systemtap}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

cp examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING NEWS README
%attr(755,root,root) %{_bindir}/gjs
%attr(755,root,root) %{_bindir}/gjs-console
%attr(755,root,root) %{_libdir}/libgjs.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgjs.so.0
%dir %{_libdir}/gjs
%dir %{_libdir}/gjs/girepository-1.0
%{_libdir}/gjs/girepository-1.0/GjsPrivate-1.0.typelib
%{_datadir}/gjs-1.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgjs.so
%{_includedir}/gjs-1.0
%{_pkgconfigdir}/gjs-1.0.pc
%{_examplesdir}/%{name}-%{version}

%files -n systemtap-gjs
%defattr(644,root,root,755)
%{_datadir}/systemtap/tapset/gjs.stp
