%global composer_namespace      fkooman/IndieCert/Auth

%global github_owner            indiecert
%global github_name             auth
%global github_commit           6672462333420b594dd289fc53e3f5526df9543b
%global github_short            %(c=%{github_commit}; echo ${c:0:7})
%if 0%{?rhel} == 5
%global with_tests              0%{?_with_tests:1}
%else
%global with_tests              0%{!?_without_tests:1}
%endif

Name:       indiecert-auth
Version:    2.1.0
Release:    2%{?dist}
Summary:    IndieCert Authentication

Group:      Applications/Internet
License:    AGPLv3+

URL:        https://github.com/%{github_owner}/%{github_name}
Source0:    %{url}/archive/%{github_commit}/%{name}-%{version}-%{github_short}.tar.gz
Source1:    %{name}-autoload.php
Source2:    %{name}-httpd.conf

BuildArch:  noarch
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 

%if %{with_tests}
BuildRequires:  php(language) >= 5.4
BuildRequires:  php-apc
BuildRequires:  php-dom
BuildRequires:  php-filter
BuildRequires:  php-libxml
BuildRequires:  php-pcre
BuildRequires:  php-pdo
BuildRequires:  php-standard
BuildRequires:  php-composer(symfony/class-loader)
BuildRequires:  %{_bindir}/phpunit
BuildRequires:  %{_bindir}/phpab

BuildRequires:  php-composer(fkooman/config) >= 1.0.0
BuildRequires:  php-composer(fkooman/config) < 2.0.0
BuildRequires:  php-composer(fkooman/http) >= 1.0.0
BuildRequires:  php-composer(fkooman/http) < 2.0.0
BuildRequires:  php-composer(fkooman/io) >= 1.0.0
BuildRequires:  php-composer(fkooman/io) < 2.0.0
BuildRequires:  php-composer(fkooman/json) >= 1.0.0
BuildRequires:  php-composer(fkooman/json) < 2.0.0
BuildRequires:  php-composer(fkooman/rest) >= 1.1.0
BuildRequires:  php-composer(fkooman/rest) < 2.0.0
BuildRequires:  php-composer(fkooman/rest-plugin-authentication) >= 2.0.0
BuildRequires:  php-composer(fkooman/rest-plugin-authentication) < 3.0.0
BuildRequires:  php-composer(fkooman/rest-plugin-authentication-tls) >= 2.0.0
BuildRequires:  php-composer(fkooman/rest-plugin-authentication-tls) < 3.0.0
BuildRequires:  php-composer(fkooman/tpl) >= 2.0.0
BuildRequires:  php-composer(fkooman/tpl) < 3.0.0
BuildRequires:  php-composer(fkooman/tpl-twig) >= 1.0.0
BuildRequires:  php-composer(fkooman/tpl-twig) < 2.0.0
BuildRequires:  php-composer(phpseclib/phpseclib) >= 2.0.0
BuildRequires:  php-composer(phpseclib/phpseclib) < 3.0.0
BuildRequires:  php-composer(guzzlehttp/guzzle) >= 5.3
BuildRequires:  php-composer(guzzlehttp/guzzle) < 6.0
%endif

Requires:   httpd
Requires:   mod_ssl

Requires:   php(language) >= 5.4
Requires:   php-apc
Requires:   php-dom
Requires:   php-filter
Requires:   php-libxml
Requires:   php-pcre
Requires:   php-pdo
Requires:   php-standard
Requires:   php-composer(fkooman/config) >= 1.0.0
Requires:   php-composer(fkooman/config) < 2.0.0
Requires:   php-composer(fkooman/http) >= 1.0.0
Requires:   php-composer(fkooman/http) < 2.0.0
Requires:   php-composer(fkooman/io) >= 1.0.0
Requires:   php-composer(fkooman/io) < 2.0.0
Requires:   php-composer(fkooman/rest) >= 1.1.0
Requires:   php-composer(fkooman/rest) < 2.0.0
Requires:   php-composer(fkooman/rest-plugin-authentication) >= 2.0.0
Requires:   php-composer(fkooman/rest-plugin-authentication) < 3.0.0
Requires:   php-composer(fkooman/rest-plugin-authentication-tls) >= 2.0.0
Requires:   php-composer(fkooman/rest-plugin-authentication-tls) < 3.0.0
Requires:   php-composer(fkooman/tpl) >= 2.0.0
Requires:   php-composer(fkooman/tpl) < 3.0.0
Requires:   php-composer(fkooman/tpl-twig) >= 1.0.0
Requires:   php-composer(fkooman/tpl-twig) < 2.0.0
Requires:   php-composer(phpseclib/phpseclib) >= 2.0.0
Requires:   php-composer(phpseclib/phpseclib) < 3.0.0
Requires:   php-composer(guzzlehttp/guzzle) >= 5.3
Requires:   php-composer(guzzlehttp/guzzle) < 6.0
Requires:   php-composer(symfony/class-loader)

Requires(post): %{_sbindir}/semanage
Requires(postun): %{_sbindir}/semanage

%description
IndieCert Authentication.

%prep
%setup -qn %{github_name}-%{github_commit} 
cp %{SOURCE1} src/%{composer_namespace}/autoload.php

sed -i "s|require_once dirname(__DIR__).'/vendor/autoload.php';|require_once '%{_datadir}/%{name}/src/%{composer_namespace}/autoload.php';|" bin/*
sed -i "s|require_once dirname(__DIR__).'/vendor/autoload.php';|require_once '%{_datadir}/%{name}/src/%{composer_namespace}/autoload.php';|" web/*.php
sed -i "s|dirname(__DIR__)|'%{_datadir}/%{name}'|" bin/*

%build

%install
rm -rf %{buildroot}

install -m 0644 -D -p %{SOURCE2} ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf.d/%{name}.conf
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/%{name}
cp -pr web views src ${RPM_BUILD_ROOT}%{_datadir}/%{name}

mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
(
cd bin
for f in `ls *`
do
    cp -pr ${f} ${RPM_BUILD_ROOT}%{_bindir}/%{name}-${f}
done
)

mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}
cp -p config/config.yaml.example ${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}/config.yaml
ln -s ../../../etc/%{name} ${RPM_BUILD_ROOT}%{_datadir}/%{name}/config
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/lib/%{name}

%if %{with_tests} 
%check
%{_bindir}/phpab --output tests/bootstrap.php tests
echo 'require_once "%{buildroot}%{_datadir}/%{name}/src/%{composer_namespace}/autoload.php";' >> tests/bootstrap.php
%{_bindir}/phpunit \
    --bootstrap tests/bootstrap.php
%endif

%clean
rm -rf %{buildroot}

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
%config(noreplace) %attr(0600,apache,apache) %{_sysconfdir}/%{name}/config.yaml
%{_bindir}/*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/src
%{_datadir}/%{name}/web
%{_datadir}/%{name}/views
%{_datadir}/%{name}/config
%dir %attr(0700,apache,apache) %{_localstatedir}/lib/%{name}
%doc README.md CHANGES.md composer.json config/config.yaml.example
%license agpl-3.0.txt

%changelog
* Wed Jan 27 2016 François Kooman <fkooman@tuxed.net> - 2.1.0-2
- rebuilt

* Wed Jan 27 2016 François Kooman <fkooman@tuxed.net> - 2.1.0-1
- update to 2.1.0

* Sat Jan 23 2016 François Kooman <fkooman@tuxed.net> - 2.0.1-1
- update to 2.0.1

* Fri Jan 22 2016 François Kooman <fkooman@tuxed.net> - 2.0.0-1
- update to 2.0.0

* Mon Sep 28 2015 François Kooman <fkooman@tuxed.net> - 1.0.1-3
- simpler way to require semanage

* Mon Sep 28 2015 François Kooman <fkooman@tuxed.net> - 1.0.1-2
- fix selinux handling on fedora >= 23

* Sun Sep 27 2015 François Kooman <fkooman@tuxed.net> - 1.0.1-1
- update to 1.0.1

* Sun Sep 27 2015 François Kooman <fkooman@tuxed.net> - 1.0.0-5
- add fkooman/ini and fkooman/tpl-twig to BuildRequires

* Sun Sep 27 2015 François Kooman <fkooman@tuxed.net> - 1.0.0-4
- run tests during build

* Sat Sep 26 2015 François Kooman <fkooman@tuxed.net> - 1.0.0-3
- fix GuzzleHttp autoload for now

* Sat Sep 26 2015 François Kooman <fkooman@tuxed.net> - 1.0.0-2
- update description
- update rewrite base in httpd config

* Sat Sep 26 2015 François Kooman <fkooman@tuxed.net> - 1.0.0-1
- initial package
