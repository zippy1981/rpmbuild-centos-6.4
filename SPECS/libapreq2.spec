%{!?_httpd_apxs: %{expand: %%global _httpd_apxs %%{_sbindir}/apxs}}
%{!?_httpd_mmn: %{expand: %%global _httpd_mmn %%(cat %{_includedir}/httpd/.mmn || echo missing-httpd-devel)}}
%{!?_httpd_confdir:    %{expand: %%global _httpd_confdir    %%{_sysconfdir}/httpd/conf.d}}
# /etc/httpd/conf.d with httpd < 2.4 and defined as /etc/httpd/conf.modules.d with httpd >= 2.4
%{!?_httpd_modconfdir: %{expand: %%global _httpd_modconfdir %%{_sysconfdir}/httpd/conf.d}}

Name:           libapreq2
Version:        2.13
Release:        14%{?dist}
Summary:        Apache HTTP request library

Group:          System Environment/Libraries
License:        ASL 2.0
URL:            http://httpd.apache.org/apreq/
Source0:        http://www.apache.org/dist/httpd/libapreq/libapreq2-%{version}.tar.gz
Source1:        %{name}-httpd.conf
Source2:        %{name}.pc.in
Patch0:         %{name}-build.patch
Patch1:         %{name}-2.07-rc3-ldflags.patch
Patch2:         %{name}-2.09-pkgconfig.patch
Patch3:         %{name}-2.12-install.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  httpd-devel >= 2.0.48
BuildRequires:  libtool
BuildRequires:  apr-devel >= 0.9.4
BuildRequires:  apr-util-devel >= 0.9.4
BuildRequires:  perl(ExtUtils::XSBuilder)
BuildRequires:  perl(Apache::Test)
BuildRequires:  perl-devel
BuildRequires:  mod_perl-devel >= 2.0.0-0.rc5
Requires:       httpd-mmn = %{_httpd_mmn}
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Provides:       libapreq = %{version}-%{release}

%description
libapreq is a shared library with associated modules for manipulating
client request data via the Apache API.  Functionality includes
parsing of application/x-www-form-urlencoded and multipart/form-data
content, as well as HTTP cookies.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       httpd-devel >= 2.0.48
Requires:       pkgconfig
Provides:       libapreq-devel = %{version}-%{release}

%description    devel
%{summary}.

%package     -n perl-%{name}
Summary:        Perl interface to the Apache HTTP request library
Group:          Development/Libraries
Requires:       mod_perl >= 2.0.0-0.rc5
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Provides:       perl-libapreq = %{version}-%{release}

%description -n perl-%{name}
This package contains a Perl interface to the Apache HTTP request
library.


%prep
%setup -q

# Filter unversioned provides for which there's a versioned one in perl-*:
cat << \EOF > %{name}-perl-prov
#!/bin/sh
%{__perl_provides} $* \
| grep -v 'perl(APR::\(Request\(::\(Apache2\|CGI\|Error\)\)\?\))$' \
| grep -v 'perl(Apache2::\(Cookie\|Request\|Upload\))$'
EOF
%define __perl_provides %{_builddir}/%{name}-%{version}/%{name}-perl-prov
chmod +x %{__perl_provides}

# Fix up paths in doc tag files:
# ap*-1-config in FC5, ap*-config in earlier
%{__perl} -pi -e \
  "s|<path>.*?</path>|<path>%{_docdir}/%{name}-devel/</path>|" \
  docs/apreq2.tag
%{__perl} -pi -e \
  "s|<path>.*?</path>|<path>%{_docdir}/apr-devel/html/</path>|" \
  docs/apr.tag
%{__perl} -pi -e \
  "s|<path>.*?</path>|<path>%{_docdir}/apr-util-devel/html/</path>|" \
  docs/apu.tag

%patch0
%patch1
%patch2
%patch3 -p1

cp %{SOURCE2} .

./buildconf


%build
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing" \
%configure \
  --disable-dependency-tracking \
  --disable-static \
  --with-apache2-apxs=%{_httpd_apxs} \
  --enable-perl-glue \
  --with-mm-opts=INSTALLDIRS=vendor
make %{?_smp_mflags}

# Fix multilib
sed -i -e 's,^libdir=.*,libdir="`pkg-config --variable=libdir %{name}`",' \
       -e 's,^LDFLAGS=.*,LDFLAGS="`pkg-config --libs %{name}`",' \
       -e 's,^LIBS=.*,LIBS="`pkg-config --libs %{name}`",' \
       -e 's,^INCLUDES=.*,INCLUDES="`pkg-config --cflags-only-I %{name}`",' \
        apreq2-config


%install
rm -rf $RPM_BUILD_ROOT __docs
mkdir -p $RPM_BUILD_ROOT%{_libdir}/pkgconfig
install -m 644 %{name}.pc $RPM_BUILD_ROOT%{_libdir}/pkgconfig
PKG_CONFIG_PATH=$RPM_BUILD_ROOT%{_libdir}/pkgconfig make install DESTDIR=$RPM_BUILD_ROOT
install -Dpm 644 %{SOURCE1} \
  $RPM_BUILD_ROOT%{_httpd_modconfdir}/apreq.conf
cp -pR docs/html __docs ; rm __docs/installdox
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.la' -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*


%check
# make test # requires write access to system locations?


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc CHANGES LICENSE NOTICE README
%config(noreplace) %{_httpd_modconfdir}/apreq.conf
%{_libdir}/libapreq2.so.*
%{_libdir}/httpd/modules/mod_apreq2.so

%files devel
%defattr(-,root,root,-)
%doc STATUS __docs/* docs/*.tag
%{_bindir}/apreq2-config
%{_includedir}/apreq2/
%{_includedir}/httpd/apreq2/
%{_libdir}/libapreq2.so
%{_libdir}/pkgconfig/*.pc

%files -n perl-%{name}
%defattr(-,root,root,-)
%doc glue/perl/README
%{perl_vendorarch}/auto/APR/
%{perl_vendorarch}/APR/
%{perl_vendorarch}/Apache2/
%{_mandir}/man3/A*::*.3*


%changelog
* Thu Aug  8 2013 Bojan Smojver <bojan@rexursive.com> - 2.13-14
- switch to unversioned documentation directory

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.13-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Petr Pisar <ppisar@redhat.com> - 2.13-12
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.13-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.13-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 29 2012 Petr Pisar <ppisar@redhat.com> - 2.13-9
- Perl 5.16 rebuild

* Wed Apr 18 2012 Joe Orton <jorton@redhat.com> - 2.13-8
- update for httpd 2.4.x
- drop httpd restart on post/postun

* Wed Mar 28 2012 Bojan Smojver <bojan@rexursive.com> - 2.13-7
- rebuild for Apache 2.4.1

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.13-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 13 2011 Bojan Smojver <bojan@rexursive.com> - 2.13-5
- rebuild for bug #766551

* Sun Jun 19 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.13-4
- Perl mass rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 28 2011 Bojan Smojver <bojan@rexursive.com> - 2.13-2
- rebuild for new Perl

* Tue Dec  7 2010 Bojan Smojver <bojan@rexursive.com> - 2.13-1
- bump up to 2.13 release

* Tue Jun 22 2010 Bojan Smojver <bojan@rexursive.com> - 2.12-6
- Fix linkage of Perl bindings: try again

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.12-6
- Mass rebuild with perl-5.12.0

* Mon Mar 29 2010 Lubomir Rintel <lkundrak@v3.sk> - 2.12-5
- Fix linkage of Perl bindings

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 2.12-3
- rebuild against perl 5.10.1

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Mar 15 2009 Bojan Smojver <bojan@rexursive.com> - 2.12-1
- bump up to 2.12 release

* Sat Mar  7 2009 Bojan Smojver <bojan@rexursive.com> - 2.12-0.rc2.1
- bump up to 2.12-RC2

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-0.rc1.3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan  7 2009 Bojan Smojver <bojan@rexursive.com> - 2.10-0.rc1.3
- better fix for apreq2-config

* Wed Jan  7 2009 Bojan Smojver <bojan@rexursive.com> - 2.10-0.rc1.2
- delay changing apreq2-config, so we don't pick up wrong libs

* Thu Nov 13 2008 Bojan Smojver <bojan@rexursive.com> - 2.10-0.rc1.1
- bump up to 2.10-RC1

* Tue Jul  8 2008 Bojan Smojver <bojan@rexursive.com> - 2.09-0.18.rc2
- add patch to use --avoid-ldap with apu-1-config

* Thu Jun  5 2008 Bojan Smojver <bojan@rexursive.com> - 2.09-0.17.rc2
- bump to re-tag

* Thu Jun  5 2008 Bojan Smojver <bojan@rexursive.com> - 2.09-0.16.rc2
- new autoconf changed the format of config.status

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.09-0.15.rc2
- Rebuild for perl 5.10 (again)

* Sat Feb  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.09-0.rc2.14
- rebuild for GCC 4.3

* Sat Feb  2 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.09-0.rc2.13
- rebuild for new perl

* Mon Dec  3 2007 Bojan Smojver <bojan at rexursive.com> - 2.09-0.rc2.12
- tag for rebuild

* Fri Oct 26 2007 Bojan Smojver <bojan at rexursive.com> - 2.09-0.rc2.11
- err on the side of caution and include more in LIBS

* Tue Oct 23 2007 Bojan Smojver <bojan at rexursive.com> - 2.09-0.rc2.10
- retag for rebuild

* Tue Oct 23 2007 Bojan Smojver <bojan at rexursive.com> - 2.09-0.rc2.9
- only use pkg-config for --ldflags in apreq2-config (closer, but not perfect)

* Mon Oct 22 2007 Bojan Smojver <bojan at rexursive.com> - 2.09-0.rc2.8
- attempt to fix multilib issues (bug #341901)

* Sat Sep 01 2007 Bojan Smojver <bojan at rexursive.com> - 2.09-0.rc2.7
- rebuild against apr-1.2.9-3 (bug #254241)

* Wed Aug 29 2007 Bojan Smojver <bojan at rexursive.com> - 2.09-0.rc2.6
- rebuild against expat 2.0.1 (bug #195888)

* Wed Aug 22 2007 Bojan Smojver <bojan at rexursive.com> - 2.09-0.rc2.5
- fix license

* Thu Mar 01 2007 Bojan Smojver <bojan at rexursive.com> - 2.09-0.rc2.4
- build requires perl-devel

* Thu Mar 01 2007 Bojan Smojver <bojan at rexursive.com> - 2.09-0.rc2.3
- build requires perl(Apache::Test)

* Wed Jan 31 2007 Bojan Smojver <bojan at rexursive.com> - 2.09-0.rc2.2
- fix version_check.pl

* Fri Nov 10 2006 Bojan Smojver <bojan at rexursive.com> - 2.09-0.rc2.1
- bump up to 2.09-rc2

* Sat Sep 16 2006 Bojan Smojver <bojan at rexursive.com> - 2.09-0.rc1.3.1
- mass rebuild

* Sat Sep 09 2006 Bojan Smojver <bojan at rexursive.com> - 2.09-0.rc1.3
- fix cleanup of the symlink

* Sat Sep 09 2006 Bojan Smojver <bojan at rexursive.com> - 2.09-0.rc1.2
- re-tag

* Sat Sep 09 2006 Bojan Smojver <bojan at rexursive.com> - 2.09-0.rc1.1
- bump up to 2.09-rc1

* Fri Aug 11 2006 Bojan Smojver <bojan at rexursive.com> - 2.08-1
- bump up to 2.08

* Mon Aug 07 2006 Bojan Smojver <bojan at rexursive.com> - 2.08-0.rc5.1
- bump up to 2.08-RC5

* Fri Jul 21 2006 Bojan Smojver <bojan at rexursive.com> - 2.08-0.rc4.1
- bump up to 2.08-RC4

* Mon Jul 10 2006 Bojan Smojver <bojan at rexursive.com> - 2.08-0.rc3.1
- bump up to 2.08-RC3

* Thu Jun 01 2006 Bojan Smojver <bojan at rexursive.com> - 2.08-0.rc2.3
- include exisiting CFLAGS too

* Thu Jun 01 2006 Bojan Smojver <bojan at rexursive.com> - 2.08-0.rc2.2
- add -fno-strict-aliasing to CFLAGS (prevent endless loop)

* Tue May 23 2006 Bojan Smojver <bojan at rexursive.com> - 2.08-0.rc2.1
- bump up to 2.08-RC2 for Rawhide
- revert back some changes to spec file made for 2.08-RC1

* Fri May 19 2006 Bojan Smojver <bojan at rexursive.com> - 2.08-0.rc1.1
- bump up to 2.08-RC1 for Rawhide

* Wed Mar 01 2006 Bojan Smojver <bojan at rexursive.com> - 2.07-1.1
- rebuild

* Mon Feb 13 2006 Bojan Smojver <bojan at rexursive.com> - 2.07-1
- bump up to 2.07

* Fri Feb 03 2006 Bojan Smojver <bojan at rexursive.com> - 2.07-0.2.rc4
- re-tag for rebuild

* Fri Feb 03 2006 Bojan Smojver <bojan at rexursive.com> - 2.07-0.1.rc4
- bump up to 2.07-rc4

* Sat Dec 10 2005 Ville Skyttä <ville.skytta at iki.fi> - 2.07-0.2.rc3
- Filter unversioned perl(*) provides for which a versioned one exists.

* Thu Dec  8 2005 Ville Skyttä <ville.skytta at iki.fi> - 2.07-0.1.rc3
- Adapt to new apr, httpd.
- Don't print -L for standard dirs in apreq2-config --link-ld output.

* Sun Oct 16 2005 Ville Skyttä <ville.skytta at iki.fi> - 2.07-0.rc3
- 2.07-rc3.

* Sat Oct 15 2005 Ville Skyttä <ville.skytta at iki.fi> - 2.07-0.rc2
- 2.07-rc2.

* Fri Aug  5 2005 Ville Skyttä <ville.skytta at iki.fi> - 2.06-2
- Include *.tag files in -devel docs, thanks to Bojan Smojver.
- Remove *.la instead of using %%exclude.

* Thu Jul 21 2005 Ville Skyttä <ville.skytta at iki.fi> - 2.06-1
- 2.06.

* Tue Jul 19 2005 Ville Skyttä <ville.skytta at iki.fi> - 2.06-0.2.rc4
- 2.06-dev-rc4.

* Sat Jul 16 2005 Ville Skyttä <ville.skytta at iki.fi> - 2.06-0.2.rc3
- 2.06-dev-rc3.

* Wed Jul 13 2005 Ville Skyttä <ville.skytta at iki.fi> - 2.06-0.2.rc2
- 2.06-dev-rc2.

* Sun Jul 10 2005 Ville Skyttä <ville.skytta at iki.fi> - 2.06-0.1.rc1
- 2.06-dev-rc1.
- Improve summaries and descriptions.

* Wed Jun 29 2005 Ville Skyttä <ville.skytta at iki.fi> - 2.05-0.6
- Rebuild with mod_perl 2.0.1.
- Drop static libs.

* Sat Jun 18 2005 Ville Skyttä <ville.skytta at iki.fi> - 2.05-0.5
- Rebuild for FC4.

* Tue May 24 2005 Ville Skyttä <ville.skytta at iki.fi> - 2.05-0.4
- Require httpd-mmn.

* Sat May 21 2005 Ville Skyttä <ville.skytta at iki.fi> - 2.05-0.3
- Rebuild with mod_perl 2.0.0.

* Wed May 18 2005 Ville Skyttä <ville.skytta at iki.fi> - 2.05-0.2
- Prevent %%post from failing at first install if httpd is not running.
- Provide (perl-)libapreq(-devel).

* Thu May  5 2005 Ville Skyttä <ville.skytta at iki.fi> - 2.05-0.1
- 2.05-dev, aclocal patch applied upstream.

* Sat Dec  4 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:2.04_03-0.fdr.2
- Buildrequire mod_perl-devel, not mod_perl.

* Wed Aug 18 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:2.03_04-0.fdr.1
- Update to 2.03_04.
- Disable dependency tracking to speed up the build.

* Thu May 27 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:2.03-0.fdr.1
- First build.
