Name:           perl-ExtUtils-XSBuilder
Version:        0.28
Release:        18%{?dist}
Summary:        Modules that parse C header files and create XS glue code
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/ExtUtils-XSBuilder/
Source0:        http://search.cpan.org/CPAN/authors/id/G/GR/GRICHTER/ExtUtils-XSBuilder-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(Parse::RecDescent)
BuildRequires:  perl(Tie::IxHash)
# Tests:
BuildRequires:  perl(ExtUtils::testlib)
Requires:       perl(Tie::IxHash)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
ExtUtils::XSBuilder is a set of modules to parse C header files and create 
XS glue code and documentation out of it. Ideally this allows one to "write" 
an interface to a C library without coding a line. Since no C-API is ideal,
some adjuments are necessary most of the time. So to use this module you
must still be familiar with C and XS programming, but it removes a lot of
stupid work and copy&paste from you. Also when the C API changes, most
of the time you only have to rerun XSBuilder to get your new Perl API.

%prep
%setup -q -n ExtUtils-XSBuilder-%{version}
find . -type f | xargs chmod -x

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make

%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%check
make test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/ExtUtils
%{_mandir}/man3/*.3*

%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 Petr Pisar <ppisar@redhat.com> - 0.28-17
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 0.28-14
- Perl 5.16 rebuild
- Specify all dependencies

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jun 19 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.28-12
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.28-10
- 661697 rebuild for fixing problems with vendorach/lib

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.28-9
- Mass rebuild with perl-5.12.0

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.28-8
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.28-7
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb  2 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.28-4
- rebuild for new perl

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> 0.28-3.1
- add BR: perl(ExtUtils::MakeMaker)

* Sun Aug 26 2007 Tom "spot" Callaway <tcallawa@redhat.com> 0.28-3
- license tag fix

* Fri Sep 15 2006 Tom "spot" Callaway <tcallawa@redhat.com> 0.28-2
- rebuild for fc6

* Mon Apr 24 2006 Tom "spot" Callaway <tcallawa@redhat.com> 0.28-1
- bump to 0.28

* Fri Jul  8 2005 Tom "spot" Callaway <tcallawa@redhat.com> 0.27-2
- cleanups

* Wed Jul  6 2005 Tom "spot" Callaway <tcallawa@redhat.com> 0.27-1
- Initial package for Fedora Extras
