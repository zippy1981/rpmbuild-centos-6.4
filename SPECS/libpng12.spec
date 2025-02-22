Summary: Old version of libpng, needed to run old binaries
Name: libpng12
Version: 1.2.50
Release: 3%{?dist}
License: zlib
Group: System Environment/Libraries
URL: http://www.libpng.org/pub/png/

# Obsolete old temporary packaging of libpng 1.2
Obsoletes: libpng-compat <= 2:1.5.10

# Note: non-current tarballs get moved to the history/ subdirectory,
# so look there if you fail to retrieve the version you want
Source: ftp://ftp.simplesystems.org/pub/png/src/libpng-%{version}.tar.bz2

Patch0: libpng12-multilib.patch
Patch1: libpng12-pngconf.patch

BuildRequires: zlib-devel, pkgconfig

%description
The libpng12 package provides libpng 1.2, an older version of the libpng
library for manipulating PNG (Portable Network Graphics) image format files.
This version should be used only if you are unable to use the current
version of libpng.

%package devel
Summary: Development files for libpng 1.2
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: zlib-devel%{?_isa} pkgconfig%{?_isa}
Conflicts: libpng-devel

%description devel
The libpng12-devel package contains header files and documentation necessary
for developing programs using libpng12.

%prep
%setup -q -n libpng-%{version}

%patch0 -p1
%patch1 -p1

%build
%configure
make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT install

# We don't ship .la files.
rm -rf $RPM_BUILD_ROOT%{_libdir}/libpng.la
rm -rf $RPM_BUILD_ROOT%{_libdir}/libpng12.la
# We're not providing any static libraries, either.
rm -rf $RPM_BUILD_ROOT%{_libdir}/*.a
# Also drop man5 files, because these are in the base libpng package,
# which we don't want to conflict with.
rm -rf $RPM_BUILD_ROOT%{_mandir}/man5/*

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc *.txt example.c README TODO CHANGES LICENSE 
%{_libdir}/libpng*.so.*

%files devel
%{_bindir}/*
%{_includedir}/*
%{_libdir}/libpng*.so
%{_libdir}/pkgconfig/*
%{_mandir}/man3/*

%changelog
* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.50-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Aug 22 2012 Tom Lane <tgl@redhat.com> 1.2.50-2
- Remove unnecessary use of epoch
Related: #850628

* Fri Aug  3 2012 Tom Lane <tgl@redhat.com> 1.2.50-1
- Update to 1.2.50 (just on general principles)
- Add Obsoletes: libpng-compat

* Wed Aug  1 2012 Tom Lane <tgl@redhat.com> 1.2.49-1
- Created from libpng
