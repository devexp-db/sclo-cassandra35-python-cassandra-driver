%global __provides_exclude_from ^%{python2_sitearch}/cassandra/io/.*\\.so$
%global commit 840064a9e27929c5f44ba06b72bfc3e69d905ee6

Name:           python-cassandra-driver
Version:        1.1.1
Release:        9%{?dist}
Summary:        DataStax Python Driver for Apache Cassandra

Group:          Development/Libraries
License:        ASL 2.0 and MIT
URL:            https://github.com/datastax/python-driver
Source0:        https://github.com/datastax/python-driver/archive/%{commit}/python-driver-%{commit}.tar.gz

# Not upstreamable
Patch0:         0001-Remove-unnecessary-test-dependencies.patch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-futures
BuildRequires:  python-scales
BuildRequires:  python-blist
BuildRequires:  python-nose
BuildRequires:  python-mock
BuildRequires:  libev-devel

Requires:       python-futures
Requires:       python-scales
Requires:       python-blist

%description
A Python client driver for Apache Cassandra. This driver works exclusively
with the Cassandra Query Language v3 (CQL3) and Cassandra's native protocol.
As such, only Cassandra 1.2+ is supported.


%prep
%setup -q -n python-driver-%{commit}
%patch0 -p1


%build
CFLAGS="%{optflags}" %{__python2} setup.py build


%install
%{__python2} setup.py install --skip-build --root %{buildroot}

# "The optional C extensions are not supported on big-endian systems."
# ...which causes setup.py to install it into arch-agnostic directory,
# which is not what we want, since we can't build a noarch package
%if "%(%{__python2} -c 'import sys; print sys.byteorder')" != "little" && 0%{?__isa_bits} > 32
mkdir -p %{buildroot}%{python2_sitearch}
mv %{buildroot}{%{python2_sitelib}/*,%{python2_sitearch}}
%endif

%if "%(%{__python2} -c 'import sys; print sys.byteorder')" == "little"
# ccache mock plugin can cause wrong mode to be set
chmod 0755 %{buildroot}%{python2_sitearch}/cassandra/{io/,}*.so
%endif


%check
# Just running the unit tests. Integration tests need ccm and cassandra
# running (neither shipped with Fedora)
%{__python2} setup.py nosetests --tests tests/unit/ \
%ifnarch x86_64
|| :
%endif


%files
%{python2_sitearch}/cassandra/
%exclude %{python2_sitearch}/cassandra/*.c
%exclude %{python2_sitearch}/cassandra/*/*.c
%{python2_sitearch}/cassandra*.egg-info/
%doc CHANGELOG.rst README.rst LICENSE example.py


%changelog
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
