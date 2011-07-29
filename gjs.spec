Summary:	JavaScript bindings for GNOME
Summary(pl.UTF-8):	Wiązania JavaScript dla GNOME
Name:		gjs
Version:	1.29.15
Release:	1
License:	MIT and (MPL v1.1 / GPL v2+ / LGPL v2+)
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gjs/1.29/%{name}-%{version}.tar.bz2
# Source0-md5:	01aa4dfb422975d22a031295b9cbc299
Patch0:		%{name}-rpath.patch
URL:		http://live.gnome.org/Gjs
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake
BuildRequires:	cairo-devel
BuildRequires:	cairo-gobject-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.18.0
BuildRequires:	gobject-introspection-devel >= 1.29.16
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	readline-devel
BuildRequires:	xulrunner-devel >= 1.9.2
%requires_eq	xulrunner-libs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Gjs allows using GNOME libraries from JavaScript. It is mainly based
on Spidermonkey JavaScript engine and the GObject introspection
framework.

%description -l pl.UTF-8
Gjs pozwala używać bibliotek GNOME z JavaScript. Bazuje głównie na
silniku JavaScript Spidermonkey i systemie GObject introspection.

%package devel
Summary:	Header files for gjs library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki gjs
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	dbus-devel
Requires:	glib2-devel >= 1:2.16.0
Requires:	gobject-introspection-devel >= 1.29.16
Requires:	xulrunner-devel

%description devel
Header files for gjs library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki gjs.

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
	--enable-introspection
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

cp examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__rm} $RPM_BUILD_ROOT%{_libdir}/gjs-1.0/*.la \
	$RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING NEWS README
%attr(755,root,root) %{_bindir}/gjs
%attr(755,root,root) %{_bindir}/gjs-console
%attr(755,root,root) %{_libdir}/libgjs-dbus.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgjs-dbus.so.0
%attr(755,root,root) %{_libdir}/libgjs-gdbus.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgjs-gdbus.so.0
%attr(755,root,root) %{_libdir}/libgjs.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgjs.so.0
%dir %{_libdir}/gjs-1.0
%attr(755,root,root) %{_libdir}/gjs-1.0/cairoNative.so
%attr(755,root,root) %{_libdir}/gjs-1.0/console.so
%attr(755,root,root) %{_libdir}/gjs-1.0/dbusNative.so
%attr(755,root,root) %{_libdir}/gjs-1.0/debugger.so
%attr(755,root,root) %{_libdir}/gjs-1.0/gettextNative.so
%attr(755,root,root) %{_libdir}/gjs-1.0/langNative.so
%attr(755,root,root) %{_libdir}/gjs-1.0/mainloop.so
%{_datadir}/gjs-1.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgjs-dbus.so
%attr(755,root,root) %{_libdir}/libgjs-gdbus.so
%attr(755,root,root) %{_libdir}/libgjs.so
%{_includedir}/gjs-1.0
%{_pkgconfigdir}/gjs-1.0.pc
%{_pkgconfigdir}/gjs-dbus-1.0.pc
%{_pkgconfigdir}/gjs-internals-1.0.pc
%{_examplesdir}/%{name}-%{version}
