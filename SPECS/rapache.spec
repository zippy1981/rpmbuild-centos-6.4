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
%define apreq2config `rpm -ql libapreq2-devel |egrep s?bin\/apreq2-config$`
%define apache_libexecdir %(%{apxs} -q LIBEXECDIR)

BuildRequires:	httpd-devel >= 2.2.0, R-devel, libapreq2-devel
Requires:	httpd >= 2.2.0, R-core, libapreq2

%description


%prep
%setup -q


%build
%configure --with-apreq2-config=%{apreq2config} --with-apache2-apxs=%{apxs} 
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

