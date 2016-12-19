%global __provides_exclude_from ^%{python2_sitearch}/cassandra/io/.*\\.so$
%global __provides_exclude_from ^%{python3_sitearch}/cassandra/io/.*\\.so$

%ifnarch x86_64 i686 aarch64 armv7hl
# disable debuginfo package on other platmorms
%global debug_package %{nil}
%endif

%global srcname python-driver
%global pypi_name cassandra-driver
%global modname cassandra
%global desc A modern, feature-rich and highly-tunable Python client library for\
Apache Cassandra (1.2+) and DataStax Enterprise (3.1+) using exclusively\
Cassandra's binary protocol and Cassandra Query Language v3.\

Name:           python-%{pypi_name}
Version:        3.7.1
Release:        2%{?dist}
Summary:        Python driver for Apache Cassandra
Group:          Development/Libraries
License:        ASL 2.0
URL:            https://github.com/datastax/%{srcname}
Source0:        https://github.com/datastax/%{srcname}/archive/%{version}.tar.gz

BuildRequires:  libev
BuildRequires:  libev-devel

BuildRequires:  Cython
BuildRequires:  python-futures
BuildRequires:  python2-setuptools
BuildRequires:  python2-devel
BuildRequires:  python-scales
BuildRequires:  python-blist
BuildRequires:  python2-nose
BuildRequires:  python2-mock
BuildRequires:  python-sure
BuildRequires:  python2-packaging

BuildRequires:  python3-Cython
BuildRequires:  python3-setuptools
BuildRequires:  python3-devel
BuildRequires:  python3-scales
BuildRequires:  python3-blist
BuildRequires:  python3-nose
BuildRequires:  python3-mock
BuildRequires:  python3-sure
BuildRequires:  python3-packaging

%description
%{desc}

%package doc
Summary:        Documentation for python-%{pypi_name}

%description doc
This package provides the documentation for python-%{pypi_name}.


%package -n python2-%{pypi_name}
Summary:        %{sumary}
%{?python_provide:%python_provide python2-%{pypi_name}}
Requires:       python-futures
Requires:       python-scales
Requires:       python-blist

%description -n python2-%{pypi_name}
%{desc}


%package -n python3-%{pypi_name}
Summary:        %{sumary}
%{?python_provide:%python_provide python3-%{pypi_name}}
Requires:       python3-scales
Requires:       python3-blist

%description -n python3-%{pypi_name}
%{desc}

%prep
%setup -q -n %{srcname}-%{version}

%build
%py2_build
%py3_build

%install
%py2_install
%py3_install

%if "%(%{__python2} -c 'import sys; print sys.byteorder')" == "little"
# ccache mock plugin can cause wrong mode to be set
chmod 0755 %{buildroot}%{python2_sitearch}/%{modname}/{io/,}*.so
%endif

%if "%(%{__python3} -c 'import sys; print(sys.byteorder)')" == "little"
# ccache mock plugin can cause wrong mode to be set
chmod 0755 %{buildroot}%{python3_sitearch}/%{modname}/{io/,}*.so
%endif

%check
# Just running the unit tests. Integration tests need ccm and cassandra
# running (neither shipped with Fedora)
%{__python2} -m nose tests/unit/ \
%ifnarch x86_64
|| :
%endif

%{__python3} -m nose tests/unit/ \
%ifnarch x86_64
|| :
%endif

%files doc
%doc docs/
%license LICENSE

%files -n python2-%{pypi_name}
%{python2_sitearch}/%{modname}/
%exclude %{python2_sitearch}/%{modname}/*.c
%exclude %{python2_sitearch}/%{modname}/*/*.c
%{python2_sitearch}/%{modname}*.egg-info/
%doc CHANGELOG.rst README.rst example_core.py example_mapper.py
%license LICENSE

%files -n python3-%{pypi_name}
%{python3_sitearch}/%{modname}/
%exclude %{python3_sitearch}/%{modname}/*.c
%exclude %{python3_sitearch}/%{modname}/*/*.c
%{python3_sitearch}/%{modname}*.egg-info/
%doc CHANGELOG.rst README.rst example_core.py example_mapper.py
%license LICENSE

%changelog
* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 3.7.1-2
- Rebuild for Python 3.6

* Wed Nov 02 2016 Lumír Balhar <lbalhar@redhat.com> - 3.7.1-1
- New upstream version

* Tue Oct 04 2016 Lumir Balhar <lbalhar@redhat.com> - 3.7.0-2
- Removed workaround for big-endians platforms which is not necessary anymore

* Thu Sep 15 2016 Lumir Balhar <lbalhar@redhat.com> - 3.7.0-1
- New upstream version

* Tue Aug 02 2016 Lumir Balhar <lbalhar@redhat.com> - 3.6.0-1
- New upstream version
- Python 2/3 subpackages

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-9
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 27 2015 Lubomir Rintel <lkundrak@v3.sk> - 1.1.1-6
- Fix up the previous patch

* Wed May 27 2015 Lubomir Rintel <lkundrak@v3.sk> - 1.1.1-5
- Fix build on 64-bit big-endians (Jakub Čajka, rh #1225487)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May 03 2014 Lubomir Rintel (GoodData) <lubo.rintel@gooddata.com> - 1.1.1-2
- Make sure the .so files have correct mode
- Fix license tag

* Wed Apr 23 2014 Lubomir Rintel (GoodData) <lubo.rintel@gooddata.com> - 1.1.1-1
- Update to 1.1.1
- Use versioned python macros

* Fri Mar 21 2014 Lubomir Rintel (GoodData) <lubo.rintel@gooddata.com> - 1.0.2-1
- Initial packaging
