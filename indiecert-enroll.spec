%global composer_namespace      fkooman/IndieCert/Enroll

%global github_owner            indiecert
%global github_name             enroll
%global github_commit           105e0e0533ece750ee8a5470c9bb3133c7d56c15
%global github_short            %(c=%{github_commit}; echo ${c:0:7})
%if 0%{?rhel} == 5
%global with_tests              0%{?_with_tests:1}
%else
%global with_tests              0%{!?_without_tests:1}
%endif

Name:       indiecert-enroll
Version:    1.0.0
Release:    6%{?dist}
Summary:    IndieCert Enrollment

Group:      Applications/Internet
License:    AGPLv3+

URL:        https://github.com/%{github_owner}/%{github_name}
Source0:    %{url}/archive/%{github_commit}/%{name}-%{version}-%{github_short}.tar.gz
Source1:    %{name}-autoload.php
Source2:    %{name}-httpd.conf

BuildArch:  noarch
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 

Requires:   httpd
Requires:   mod_ssl

Requires:   php(language) >= 5.3.0
Requires:   php-standard
Requires:   php-composer(fkooman/ini) >= 1.0.0
Requires:   php-composer(fkooman/ini) < 2.0.0
Requires:   php-composer(fkooman/io) >= 1.0.0
Requires:   php-composer(fkooman/io) < 2.0.0
Requires:   php-composer(fkooman/rest) >= 1.0.1
Requires:   php-composer(fkooman/rest) < 2.0.0
Requires:   php-composer(fkooman/tpl-twig) >= 1.0.0
Requires:   php-composer(fkooman/tpl-twig) < 2.0.0
Requires:   php-composer(phpseclib/phpseclib) >= 2.0.0
Requires:   php-composer(phpseclib/phpseclib) < 3.0.0
Requires:   php-composer(symfony/class-loader)

Requires(post): %{_sbindir}/semanage
Requires(postun): %{_sbindir}/semanage

%description
IndieCert Enrollment.

%prep
%setup -qn %{github_name}-%{github_commit} 
cp %{SOURCE1} src/%{composer_namespace}/autoload.php

sed -i "s|require_once dirname(__DIR__).'/vendor/autoload.php';|require_once '%{_datadir}/%{name}/src/%{composer_namespace}/autoload.php';|" bin/*
sed -i "s|require_once dirname(__DIR__).'/vendor/autoload.php';|require_once '%{_datadir}/%{name}/src/%{composer_namespace}/autoload.php';|" web/*.php
sed -i "s|dirname(__DIR__)|'%{_datadir}/%{name}'|" bin/*

%build

%install
# Apache configuration
install -m 0644 -D -p %{SOURCE2} ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf.d/%{name}.conf

# Application
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/%{name}
cp -pr web views src ${RPM_BUILD_ROOT}%{_datadir}/%{name}

mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
cp -pr bin/* ${RPM_BUILD_ROOT}%{_bindir}

# Config
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}
cp -p config/config.ini.default ${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}/config.ini
ln -s ../../../etc/%{name} ${RPM_BUILD_ROOT}%{_datadir}/%{name}/config

# Data
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/lib/%{name}

%post
semanage fcontext -a -t httpd_sys_rw_content_t '%{_localstatedir}/lib/%{name}(/.*)?' 2>/dev/null || :
restorecon -R %{_localstatedir}/lib/%{name} || :

%postun
if [ $1 -eq 0 ] ; then  # final removal
semanage fcontext -d -t httpd_sys_rw_content_t '%{_localstatedir}/lib/%{name}(/.*)?' 2>/dev/null || :
fi

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%dir %attr(-,apache,apache) %{_sysconfdir}/%{name}
%config(noreplace) %attr(0600,apache,apache) %{_sysconfdir}/%{name}/config.ini
%{_bindir}/*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/src
%{_datadir}/%{name}/web
%{_datadir}/%{name}/config
%{_datadir}/%{name}/views
%dir %attr(0700,apache,apache) %{_localstatedir}/lib/%{name}
%doc README.md CHANGES.md composer.json config/config.ini.default
%license agpl-3.0.txt

%changelog
* Mon Sep 28 2015 François Kooman <fkooman@tuxed.net> - 1.0.0-6
- simpler way to require semanage

* Mon Sep 28 2015 François Kooman <fkooman@tuxed.net> - 1.0.0-5
- fix selinux handling on fedora >= 23

* Sat Sep 26 2015 François Kooman <fkooman@tuxed.net> - 1.0.0-4
- add data dir

* Sat Sep 26 2015 François Kooman <fkooman@tuxed.net> - 1.0.0-3
- fix require path in bin script

* Sat Sep 26 2015 François Kooman <fkooman@tuxed.net> - 1.0.0-2
- install config file
- install scripts from bin directory

* Sat Sep 26 2015 François Kooman <fkooman@tuxed.net> - 1.0.0-1
- initial package
