%global composer_namespace      fkooman/IndieCert/Demo

%global github_owner            indiecert
%global github_name             demo
%global github_commit           58ded4e0ae287b7ec6f95f8f0f4be6dd8c575397
%global github_short            %(c=%{github_commit}; echo ${c:0:7})

Name:       indiecert-demo
Version:    1.0.1
Release:    2%{?dist}
Summary:    IndieCert Demo

Group:      Applications/Internet
License:    AGPLv3+

URL:        https://github.com/%{github_owner}/%{github_name}
Source0:    %{url}/archive/%{github_commit}/%{name}-%{version}-%{github_short}.tar.gz
Source1:    %{name}-autoload.php
Source2:    %{name}-httpd.conf

BuildArch:  noarch
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 

Requires:   httpd
Requires:   php(language) >= 5.4
Requires:   php-standard
Requires:   php-composer(fkooman/config) >= 1.0.0
Requires:   php-composer(fkooman/config) < 2.0.0
Requires:   php-composer(fkooman/http) >= 1.0.0
Requires:   php-composer(fkooman/http) < 2.0.0
Requires:   php-composer(fkooman/rest) >= 1.0.1
Requires:   php-composer(fkooman/rest) < 2.0.0
Requires:   php-composer(fkooman/rest-plugin-authentication-indieauth) >= 2.0.0
Requires:   php-composer(fkooman/rest-plugin-authentication-indieauth) < 3.0.0
Requires:   php-composer(fkooman/tpl-twig) >= 1.1.0
Requires:   php-composer(fkooman/tpl-twig) < 2.0.0
Requires:   php-composer(guzzlehttp/guzzle) >= 5.3
Requires:   php-composer(guzzlehttp/guzzle) < 6.0
Requires:   php-composer(symfony/class-loader)

%description
IndieCert Demo.

%prep
%setup -qn %{github_name}-%{github_commit} 
cp %{SOURCE1} src/%{composer_namespace}/autoload.php

sed -i "s|require_once dirname(__DIR__).'/vendor/autoload.php';|require_once '%{_datadir}/%{name}/src/%{composer_namespace}/autoload.php';|" web/*.php

%build

%install
rm -rf %{buildroot}

install -m 0644 -D -p %{SOURCE2} ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf.d/%{name}.conf
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/%{name}
cp -pr web views src ${RPM_BUILD_ROOT}%{_datadir}/%{name}
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}
cp -p config/config.yaml.example ${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}/config.yaml
ln -s ../../../etc/%{name} ${RPM_BUILD_ROOT}%{_datadir}/%{name}/config
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/lib/%{name}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%dir %attr(-,apache,apache) %{_sysconfdir}/%{name}
%config(noreplace) %attr(0600,apache,apache) %{_sysconfdir}/%{name}/config.yaml
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/src
%{_datadir}/%{name}/web
%{_datadir}/%{name}/views
%{_datadir}/%{name}/config
%doc README.md CHANGES.md composer.json config/config.yaml.example
%license agpl-3.0.txt

%changelog
* Fri Jan 22 2016 François Kooman <fkooman@tuxed.net> - 1.0.1-2
- add configuration file

* Fri Jan 22 2016 François Kooman <fkooman@tuxed.net> - 1.0.1-1
- update to 1.0.1

* Fri Jan 22 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-1
- initial package
