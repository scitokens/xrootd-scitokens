Name: xrootd-scitokens
Version: 0.6.0
Release: 1%{?dist}
Summary: SciTokens authentication plugin for XRootD
License: Apache 2.0
URL: https://github.com/scitokens/xrootd-scitokens

# Generated from:
# git archive v%{version} --prefix=xrootd-scitokens-%{version}/ | gzip -7 > ~/rpmbuild/SOURCES/xrootd-scitokens-%{version}.tar.gz
Source0: %{name}-%{version}.tar.gz

BuildRequires: gcc-c++
BuildRequires: cmake
BuildRequires: boost-devel
BuildRequires: python-devel
BuildRequires: xrootd-server-devel

Requires: python2-scitokens >= 1.2.1
#Requires: boost-python

%description
SciTokens authentication plugin for XRootD

%prep
%setup -q

%build
mkdir build
cd build
%cmake -DPython_ADDITIONAL_VERSIONS=2.7 ..
make 

%install
pushd build
rm -rf $RPM_BUILD_ROOT
echo $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
popd

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%{_libdir}/libXrdAccSciTokens-4.so
%{_libdir}/python2.7/site-packages/_scitokens_xrootd.so
%{_libdir}/python2.7/site-packages/scitokens_xrootd.py*
%config(noreplace) %{_sysconfdir}/xrootd/scitokens.cfg
%config %{_sysconfdir}/xrootd/config.d/30-scitokens-auth.cfg

%defattr(-,root,root,-)

%changelog
* Tue Oct 23 2018 Derek Weitzel <dweitzel@cse.unl.edu> - 0.6.0-1
- Add support for audiences and multiple audience support

* Thu Mar 08 2018 Brian Bockelman <bbockelm@cse.unl.edu> - 0.5.0-1
- Add support for multiple base paths of an issuer.
- Add concept of restricting authorized paths within an issuer's namespace.
- Fix potential segfault when a user environment isnt available.

* Tue Feb 06 2018 Derek Weitzel <dweitzel@cse.unl.edu> - 0.4.0-1
- Update to v0.4.0

* Mon Nov 06 2017 Brian Bockelman <bbockelm@cse.unl.edu> - 0.3.1-1
- Fix issue with translating write authz.

* Wed Sep 20 2017 Brian Bockelman <bbockelm@cse.unl.edu> - 0.2.0-1
- Remove urltools dependency.

* Wed Sep 20 2017 Lincoln Bryant <lincolnb@uchicago.edu> - 0.1.0-1
- Initial package
