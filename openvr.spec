#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	OpenVR SDK - API and runtime that allows access to VR hardware
Summary(pl.UTF-8):	OpenVR SDK - API i biblioteka uruchomieniowa pozwalająca na dostęp do sprzętu VR
Name:		openvr
Version:	1.23.8
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/ValveSoftware/openvr/tags
Source0:	https://github.com/ValveSoftware/openvr/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	2dd6945040b63c9a2d1ce4ece00bda7e
Patch0:		%{name}-pc.patch
URL:		https://github.com/ValveSoftware/openvr
BuildRequires:	cmake >= 2.8
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OpenVR is an API and runtime that allows access to VR hardware from
multiple vendors without requiring that applications have specific
knowledge of the hardware they are targeting. This is an SDK that
contains the API and samples. The runtime is under SteamVR in Tools on
Steam.

%description -l pl.UTF-8
OpenVR to API i biblioteka uruchomieniowa, poozwalająca na dostęp do
sprzętu VR różnych producentów bez wymagania od aplikacji wiedzy o
sprzęcie, z jakim ma być używana. Ten pakiet zawiera API i przykłady.
Biblioteka uruchomieniowa jest umieszczona w StreamVR w Tools on
Steam.

%package devel
Summary:	Header files for OpenVR SDK library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki OpenVR SDK
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel >= 6:4.7

%description devel
Header files for OpenVR SDK library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki OpenVR SDK.

%package static
Summary:	Static OpenVR SDK library
Summary(pl.UTF-8):	Statyczna biblioteka OpenVR SDK
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static OpenVR SDK library.

%description static -l pl.UTF-8
Statyczna biblioteka OpenVR SDK.

%prep
%setup -q
%patch0 -p1

# prebuilt binaries
%{__rm} -r bin lib

%build
%if %{with static_libs}
install -d build-static
cd build-static
%cmake .. \
	-DINSTALL_PKGCONFIG_DIR=%{_pkgconfigdir}

%{__make}
cd ..
%endif

install -d build-shared
cd build-shared
%cmake .. \
	-DBUILD_SHARED=ON \
	-DINSTALL_PKGCONFIG_DIR=%{_pkgconfigdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%if %{with static_libs}
%{__make} -C build-static install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%{__make} -C build-shared install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%attr(755,root,root) %{_libdir}/libopenvr_api.so

%files devel
%defattr(644,root,root,755)
%doc src/README docs/Driver_API_Documentation.md
%{_includedir}/openvr
%{_pkgconfigdir}/openvr.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libopenvr_api.a
%endif
