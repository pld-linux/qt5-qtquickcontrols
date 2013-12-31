# TODO:
# - cleanup

%define		orgname		qtquickcontrols
Summary:	The Qt5 Quick Controls
Name:		qt5-%{orgname}
Version:	5.2.0
Release:	0.1
License:	LGPL v2.1 or GPL v3.0
Group:		X11/Libraries
Source0:	http://download.qt-project.org/official_releases/qt/5.2/%{version}/submodules/%{orgname}-opensource-src-%{version}.tar.xz
# Source0-md5:	748ab947f59fb104db2ac1fefa073d81
URL:		http://qt-project.org/
BuildRequires:	qt5-qtbase-devel = %{version}
BuildRequires:	qt5-qtdeclarative-devel = %{version}
BuildRequires:	qt5-qtscript-devel = %{version}
BuildRequires:	qt5-qttools-devel = %{version}
BuildRequires:	rpmbuild(macros) >= 1.654
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreqdep	libGL.so.1 libGLU.so.1
%define		_noautostrip	'.*_debug\\.so*'

%define		specflags	-fno-strict-aliasing
%define		_qtdir		%{_libdir}/qt5

%description
Qt5 Quick Controls libraries.

%package devel
Summary:	The Qt5 Quick Controls - development files
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Qt5 Quick Controls - development files.

%package doc
Summary:	The Qt5 Quick Controls - docs
Group:		Documentation

%description doc
Qt5 Quick Controls - documentation.

%package examples
Summary:	Qt5 Quick Controls examples
Group:		X11/Development/Libraries

%description examples
Qt5 Quick Controls - examples.

%prep
%setup -q -n %{orgname}-opensource-src-%{version}

%build
qmake-qt5
%{__make}
%{__make} docs

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

%{__make} install_docs \
	INSTALL_ROOT=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post		-p /sbin/ldconfig
%postun		-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%{_qtdir}/qml

%files doc
%defattr(644,root,root,755)
%{_docdir}/qt5-doc
