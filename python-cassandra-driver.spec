%{?scl:%scl_package python-futures}
%{!?scl:%global pkg_name %{name}}

%if 0%{?fedora}
%global with_python3 1
%global with_tests 1
%endif

%global __provides_exclude_from ^%{python2_sitearch}/cassandra/io/.*\\.so$
%if 0%{?with_python3}
%global __provides_exclude_from ^%{python3_sitearch}/cassandra/io/.*\\.so$
%endif

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

Name:           %{?scl_prefix}python-%{pypi_name}
Version:        3.11.0
Release:        4%{?dist}
Summary:        Python driver for Apache Cassandra
Group:          Development/Libraries
License:        ASL 2.0
URL:            https://github.com/datastax/%{srcname}
Source0:        https://github.com/datastax/%{srcname}/archive/%{version}.tar.gz

BuildRequires:  libev
BuildRequires:  libev-devel

BuildRequires:  %{?scl_prefix}python2-futures
BuildRequires:  python2-devel
BuildRequires:  %{?scl_prefix}python2-scales
BuildRequires:  %{?scl_prefix}python2-blist
#BuildRequires:  python2-mock
BuildRequires:  %{?scl_prefix}python2-sure
BuildRequires:  %{?scl_prefix}python2-packaging
BuildRequires:  %{?scl_prefix}python2-eventlet

%if 0%{?fedora}
BuildRequires:  Cython
BuildRequires:  python2-setuptools
BuildRequires:  python2-nose
%else
BuildRequires:  python-setuptools
BuildRequires:  python-nose
%endif

%if 0%{?with_python3}
BuildRequires:  python%{python3_pkgversion}-Cython
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-scales
BuildRequires:  python%{python3_pkgversion}-blist
BuildRequires:  python%{python3_pkgversion}-nose
BuildRequires:  python%{python3_pkgversion}-mock
BuildRequires:  python%{python3_pkgversion}-sure
BuildRequires:  python%{python3_pkgversion}-packaging
BuildRequires:  python%{python3_pkgversion}-eventlet
%endif

%{?scl:Requires: %scl_runtime}
%{?scl:BuildRequires: %scl-scldevel}

%description
%{desc}

%package doc
Summary:        Documentation for python-%{pypi_name}

%description doc
This package provides the documentation for python-%{pypi_name}.


%package -n %{?scl_prefix}python2-%{pypi_name}
Summary:        %{summary}
%{!?scl:%{?python_provide:%python_provide python2-%{pypi_name}}}
Requires:       %{?scl_prefix}python2-futures
Requires:       %{?scl_prefix}python2-scales
Requires:       %{?scl_prefix}python2-blist

Provides:       %{?scl_prefix}%{name} = %{version}-%{release}
Obsoletes:      %{?scl_prefix}%{name} < 3.7.1-5

%description -n %{?scl_prefix}python2-%{pypi_name}
%{desc}

%if 0%{?with_python3}
%package -n %{?scl_prefix}python%{python3_pkgversion}-%{pypi_name}
Summary:        %{summary}
%{!?scl:%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}}
Requires:       %{?scl_prefix}python%{python3_pkgversion}-scales
Requires:       %{?scl_prefix}python%{python3_pkgversion}-blist

%description -n %{?scl_prefix}python%{python3_pkgversion}-%{pypi_name}
%{desc}
%endif

%prep
%autosetup -n %{srcname}-%{version}
# Fix Cython version requirements (remove upper limit)
sed -i 's/\([cC]ython.*\),<0.25/\1/g' test-requirements.txt setup.py

%build
%{?scl:scl enable %{scl} - << "EOF"}
# Build with Cython only in Fedora
%if 0%{?fedora}
%py2_build
%else
%py2_build -- --no-cython
%endif

%if 0%{?with_python3}
%py3_build
%endif
%{?scl:EOF}

%install
%{?scl:scl enable %{scl} - << "EOF"}
%if 0%{?fedora}
%py2_install
%else
%py2_install -- --no-cython --prefix %{?_prefix}
%endif
%if 0%{?with_python3}
%py3_install
%endif

%if "%(%{__python2} -c 'import sys; print sys.byteorder')" == "little"
# ccache mock plugin can cause wrong mode to be set
chmod 0755 %{buildroot}%{python2_sitearch}/%{modname}/{io/,}*.so
%endif

%if 0%{?with_python3}
%if "%(%{__python3} -c 'import sys; print(sys.byteorder)')" == "little"
# ccache mock plugin can cause wrong mode to be set
chmod 0755 %{buildroot}%{python3_sitearch}/%{modname}/{io/,}*.so
%endif
%endif
%{?scl:EOF}


%check
# Just running the unit tests. Integration tests need ccm and cassandra
# running (neither shipped with Fedora)
%if 0%{?with_tests}
%{__python2} -m nose tests/unit/ \
%ifarch ppc64
-e test_murmur3_python
%endif # ifarch
%ifarch aarch64
-e test_nts_token_performance
%endif # ifarch
%ifarch s390x
-e test_murmur3_python -e test_multi_timer_validation -e test_nts_token_performance
%endif # ifarch

%if 0%{?with_python3}
%{__python3} -m nose tests/unit/ \
%ifarch ppc64
-e test_murmur3_python
%endif # ifarch
%ifarch aarch64
-e test_nts_token_performance
%endif # ifarch
%ifarch s390x
-e test_murmur3_python -e test_multi_timer_validation -e test_nts_token_performance
%endif # ifarch
%endif # with_python3
%endif # with_tests

%files doc
%doc docs/
%license LICENSE

%files -n %{?scl_prefix}python2-%{pypi_name}
%{python2_sitearch}/%{modname}/
%exclude %{python2_sitearch}/%{modname}/*.c
%exclude %{python2_sitearch}/%{modname}/*/*.c
%{python2_sitearch}/%{modname}*.egg-info/
%doc CHANGELOG.rst README.rst example_core.py example_mapper.py
%license LICENSE

%if 0%{?with_python3}
%files -n %{?scl_prefix}python%{python3_pkgversion}-%{pypi_name}
%{python3_sitearch}/%{modname}/
%exclude %{python3_sitearch}/%{modname}/*.c
%exclude %{python3_sitearch}/%{modname}/*/*.c
%{python3_sitearch}/%{modname}*.egg-info/
%doc CHANGELOG.rst README.rst example_core.py example_mapper.py
%license LICENSE
%endif

%changelog
* Thu Oct 05 2017 Augusto Mecking Caringi <acaringi@redhat.com> - 3.11.0-4
- fixed runtime dependencies

* Wed Oct 04 2017 Augusto Mecking Caringi <acaringi@redhat.com> - 3.11.0-3
- scl conversion

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Mon Jul 31 2017 Lumír Balhar <lbalhar@redhat.com> - 3.11.0-1
- New upstream version

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri May 26 2017 Lumír Balhar <lbalhar@redhat.com> - 3.10.0-1
- New upstream release
- Skip new test for specific platforms

* Thu May 18 2017 Lumír Balhar <lbalhar@redhat.com> - 3.9.0-3
- Skip only specific tests on centrain unsupported platforms

* Tue May 16 2017 Lumír Balhar <lbalhar@redhat.com> - 3.9.0-2
- Fix and enable tests on more (big endian) platforms

* Sun Apr 16 2017 Lumír Balhar <lbalhar@redhat.com> - 3.9.0-1
- New upstream release

* Wed Mar 29 2017 Lumír Balhar <lbalhar@redhat.com> - 3.8.1-3
- Disable Cython integration and tests in Epel7

* Mon Mar 27 2017 Lumír Balhar <lbalhar@redhat.com> - 3.8.1-2
- Epel7 update

* Fri Mar 17 2017 Lumír Balhar <lbalhar@redhat.com> - 3.8.1-1
- New upstream release

* Thu Feb 23 2017 Lumír Balhar <lbalhar@redhat.com> - 3.8.0-1
- New upstream release

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 04 2017 Lumír Balhar <lbalhar@redhat.com> - 3.7.1-4
- Added Provides and Obsoletes to specfile

* Mon Jan 02 2017 Lumír Balhar <lbalhar@redhat.com> - 3.7.1-3
- Fixed typo in summary macro in specfile
- Added hotfix for Cython version requirements

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
