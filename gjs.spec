#TODO: systemtap/dtrace
#
Summary:	JavaScript bindings for GNOME
Summary(pl.UTF-8):	Wiązania JavaScriptu dla GNOME
Name:		gjs
Version:	1.38.1
Release:	1
License:	MIT and (MPL v1.1 or GPL v2+ or LGPL v2+)
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gjs/1.38/%{name}-%{version}.tar.xz
# Source0-md5:	0f3422a114cb69735274e75e325013a3
URL:		http://live.gnome.org/Gjs
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake
BuildRequires:	cairo-devel
BuildRequires:	cairo-gobject-devel
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.36.0
BuildRequires:	gobject-introspection-devel >= 1.38.0
BuildRequires:	mozjs17-devel
BuildRequires:	libffi-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	readline-devel
Requires:	glib2 >= 1:2.36.0
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
Requires:	dbus-devel
Requires:	glib2-devel >= 1:2.36.0
Requires:	gobject-introspection-devel >= 1.36.0
Requires:	js185-devel

%description devel
Header files for gjs library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki gjs.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules
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
%{_pkgconfigdir}/gjs-internals-1.0.pc
%{_examplesdir}/%{name}-%{version}
