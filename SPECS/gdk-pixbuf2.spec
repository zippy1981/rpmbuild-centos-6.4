Name:           gdk-pixbuf2
Version:        2.26.1
Release:        1%{?dist}
Summary:        An image loading library

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://www.gt.org
#VCS:           git:git://git.gnome.org/gdk-pixbuf
Source0:        http://download.gnome.org/sources/gdk-pixbuf/2.26/gdk-pixbuf-%{version}.tar.xz

BuildRequires:  glib2-devel >= 2.32.0
BuildRequires:  libpng-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libtiff-devel
BuildRequires:  jasper-devel
BuildRequires:  libX11-devel
BuildRequires:  gobject-introspection-devel >= 0.9.3
# gdk-pixbuf does a configure time check which uses the GIO mime
# layer; we need to actually have the mime type database.
BuildRequires:  shared-mime-info
# Bootstrap requirements
BuildRequires: autoconf automake libtool gtk-doc
BuildRequires: gettext-autopoint

# We also need MIME information at runtime
Requires: shared-mime-info

# gdk-pixbuf was included in gtk2 until 2.21.2
Conflicts: gtk2 <= 2.21.2

%description
gdk-pixbuf is an image loading library that can be extended by loadable
modules for new image formats. It is used by toolkits such as GTK+ or
clutter.

%package devel
Summary: Development files for gdk-pixbuf
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: glib2-devel

# gdk-pixbuf was included in gtk2 until 2.21.2
Conflicts: gtk2-devel <= 2.21.2

%description devel
This package contains the libraries and header files that are needed
for writing applications that are using gdk-pixbuf.


%prep
%setup -q -n gdk-pixbuf-%{version}

%build
(if ! test -x configure; then NOCONFIGURE=1 ./autogen.sh; CONFIGFLAGS=--enable-gtk-doc; fi;
 %configure $CONFIGFLAGS             \
        --with-x11                   \
        --with-libjasper             \
        --with-included-loaders=png  )
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT    \
             RUN_QUERY_LOADER_TEST=false

# Remove unpackaged files
rm $RPM_BUILD_ROOT%{_libdir}/*.la
rm $RPM_BUILD_ROOT%{_libdir}/gdk-pixbuf-2.0/2.10.0/loaders/*.la

touch $RPM_BUILD_ROOT%{_libdir}/gdk-pixbuf-2.0/2.10.0/loaders.cache

(cd $RPM_BUILD_ROOT%{_bindir}
 mv gdk-pixbuf-query-loaders gdk-pixbuf-query-loaders-%{__isa_bits}
)

%find_lang gdk-pixbuf

%post
/sbin/ldconfig
gdk-pixbuf-query-loaders-%{__isa_bits} --update-cache || :

%postun
/sbin/ldconfig
if [ $1 -gt 0 ]; then
  gdk-pixbuf-query-loaders-%{__isa_bits} --update-cache || :
fi

%files -f gdk-pixbuf.lang
%doc AUTHORS COPYING NEWS
%{_libdir}/libgdk_pixbuf-2.0.so.*
%{_libdir}/libgdk_pixbuf_xlib-2.0.so.*
%{_libdir}/girepository-1.0
%dir %{_libdir}/gdk-pixbuf-2.0
%dir %{_libdir}/gdk-pixbuf-2.0/2.10.0
%dir %{_libdir}/gdk-pixbuf-2.0/2.10.0/loaders
%{_libdir}/gdk-pixbuf-2.0/2.10.0/loaders/*.so
%ghost %{_libdir}/gdk-pixbuf-2.0/2.10.0/loaders.cache
%{_bindir}/gdk-pixbuf-query-loaders-%{__isa_bits}
%{_mandir}/man1/gdk-pixbuf-query-loaders.1*

%files devel
%{_includedir}/gdk-pixbuf-2.0
%{_libdir}/libgdk_pixbuf-2.0.so
%{_libdir}/libgdk_pixbuf_xlib-2.0.so
%{_libdir}/pkgconfig/gdk-pixbuf-2.0.pc
%{_libdir}/pkgconfig/gdk-pixbuf-xlib-2.0.pc
%{_bindir}/gdk-pixbuf-csource
%{_bindir}/gdk-pixbuf-pixdata
%{_datadir}/gir-1.0
%{_datadir}/gtk-doc/html/*
%{_mandir}/man1/gdk-pixbuf-csource.1*


%changelog
* Sat Apr 14 2012 Matthias Clasen <mclasen@redhat.com> - 2.26.1-1
- Update to 2.26.1

* Tue Mar 20 2012 Kalev Lember <kalevlember@gmail.com> - 2.26.0-1
- Update to 2.26.0

* Mon Feb  6 2012 Matthias Clasen <mclasen@redhat.com> - 2.25.2-1
- Update to 2.25.2

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 16 2011 Matthias Clasen <mclasen@redhat.com> - 2.25.0-1
- Update to 2.25.0

* Mon Nov  7 2011 Matthias Clasen <mclasen@redhat.com> - 2.24.0-2
- Rebuild against new libpng

* Tue Aug 30 2011 Matthias Clasen <mclasen@redhat.com> - 2.24.0-1
- Update to 2.24.0

* Mon Jun 27 2011 Matthias Clasen <mclasen@redhat.com> - 2.23.5-1
- Update to 2.23.5 (fixes CVE-2011-2485)

* Wed Jun 15 2011 Tomas Bzatek <tbzatek@redhat.com> - 2.23.4-1
- Update to 2.23.4

* Wed Mar 30 2011 Matthias Clasen <mclasen@redhat.com> 2.23.3-1
- Update to 2.23.3

* Sat Mar  5 2011 Matthias Clasen <mclasen@redhat.com> 2.23.1-1
- Update to 2.23.1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.23.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan  9 2011 Matthias Clasen <mclasen@redhat.com> 2.23.0-1
- Update to 2.23.0

* Fri Nov  5 2010 Matthias Clasen <mclasen@redhat.com> 2.22.1-1
- Update to 2.22.1

* Wed Sep 29 2010 jkeating - 2.22.0-2
- Rebuilt for gcc bug 634757

* Tue Sep 21 2010 Matthias Clasen <mclasen@redhat.com> 2.22.0-1
- Update to 2.22.0

* Mon Jul 19 2010 Bastien Nocera <bnocera@redhat.com> 2.21.6-3
- Require libpng for linking

* Thu Jul 15 2010 Colin Walters <walters@verbum.org> - 2.21.6-2
- Rebuild with new gobject-introspection

* Mon Jul 12 2010 Matthias Clasen <mclasen@redhat.com> - 2.21.6-1
- Update to 2.21.6

* Fri Jul  2 2010 Colin Walters <walters@verbum.org> - 2.21.5-4
- Also Require shared-mime-info for same reason

* Fri Jul  2 2010 Colin Walters <walters@verbum.org> - 2.21.5-3
- BR shared-mime-info; see comment above it

* Tue Jun 29 2010 Colin Walters <walters@pocket> - 2.21.5-2
- Changes to support snapshot builds

* Mon Jun 28 2010 Matthias Clasen <mclasen@redhat.com> 2.21.5-1
- Update to 2.21.5

* Sat Jun 26 2010 Matthias Clasen <mclasen@redhat.com> 2.21.4-2
- Rename to gdk-pixbuf2 to avoid conflict with the
  existing gdk-pixbuf package

* Sat Jun 26 2010 Matthias Clasen <mclasen@redhat.com> 2.21.4-1
- Update to 2.21.4
- Incorporate package review feedback

* Sat Jun 26 2010 Matthias Clasen <mclasen@redhat.com> 2.21.3-1
- Initial packaging
