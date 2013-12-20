Name:		rapache
Version:	1.2.4
Release:	1%{?dist}
Summary:	rApache is a project supporting web application development using the R statistical language and environment and the Apache web server.

Group:		Applications/Engineering
License:	Apache 2.0
URL:		http://rapache.net/
Source0:	https://codeload.github.com/jeffreyhorner/rapache-1.2.4.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%define apxs `rpm -ql httpd-devel |egrep s?bin\/apxs2?$`
%define apache_libexecdir %(%{apxs} -q LIBEXECDIR)

BuildRequires:	httpd-devel >= 2.2.0, R-devel
Requires:	httpd >= 2.2.0, R-core

%description


%prep
%setup -q


%build
%configure --with-apache2-apxs=%{apxs}
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} -d
#%{apxs} -i -S LIBEXECDIR=%{buildroot}%{apache_libexecdir} -n R mod_R.la


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc



%changelog

