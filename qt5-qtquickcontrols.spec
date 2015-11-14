#
# Conditional build:
%bcond_without	qch	# documentation in QCH format
%bcond_without	qm	# QM translations

%define		orgname		qtquickcontrols
%define		qtbase_ver		%{version}
%define		qtdeclarative_ver	%{version}
%define		qttools_ver		%{version}
Summary:	The Qt5 Quick Controls modules
Summary(pl.UTF-8):	Moduły Qt5 Quick Controls
Name:		qt5-%{orgname}
Version:	5.5.1
Release:	1
License:	LGPL v3 or GPL v2 or commercial
Group:		X11/Libraries
Source0:	http://download.qt.io/official_releases/qt/5.5/%{version}/submodules/%{orgname}-opensource-src-%{version}.tar.xz
# Source0-md5:	01ace647bda006b61200f61ebe6ef93b
Source1:	http://download.qt.io/official_releases/qt/5.5/%{version}/submodules/qttranslations-opensource-src-%{version}.tar.xz
# Source1-md5:	1f89d53fe759db123b4b6d9de9d9e8c9
URL:		http://www.qt.io/
BuildRequires:	Qt5Core-devel >= %{qtbase_ver}
BuildRequires:	Qt5Gui-devel >= %{qtbase_ver}
BuildRequires:	Qt5Network-devel >= %{qtbase_ver}
BuildRequires:	Qt5Qml-devel >= %{qtdeclarative_ver}
BuildRequires:	Qt5Quick-devel >= %{qtdeclarative_ver}
BuildRequires:	Qt5Widgets-devel >= %{qtbase_ver}
%if %{with qch}
BuildRequires:	qt5-assistant >= %{qttools_ver}
%endif
BuildRequires:	qt5-build >= %{qtbase_ver}
%{?with_qm:BuildRequires:	qt5-linguist >= %{qttools_ver}}
BuildRequires:	qt5-qmake >= %{qtbase_ver}
BuildRequires:	rpmbuild(macros) >= 1.654
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	-fno-strict-aliasing
%define		qt5dir		%{_libdir}/qt5

%description
Qt is a cross-platform application and UI framework. Using Qt, you can
write web-enabled applications once and deploy them across desktop,
mobile and embedded systems without rewriting the source code.

This package contains Qt5 Quick Controls, Dialogs, Layouts modules.

%description -l pl.UTF-8
Qt to wieloplatformowy szkielet aplikacji i interfejsów użytkownika.
Przy użyciu Qt można pisać aplikacje powiązane z WWW i wdrażać je w
systemach biurkowych, przenośnych i wbudowanych bez przepisywania kodu
źródłowego.

Ten pakiet zawiera moduły Qt5 Quick Controls, Dialogs i Layouts.

%package -n Qt5Quick-controls
Summary:	The Qt5 Quick Controls modules
Summary(pl.UTF-8):	Moduły Qt5 Quick Controls
Group:		X11/Libraries
Requires:	Qt5Core >= %{qtbase_ver}
Requires:	Qt5Gui >= %{qtbase_ver}
Requires:	Qt5Qml >= %{qtdeclarative_ver}
Requires:	Qt5Quick >= %{qtdeclarative_ver}
Requires:	Qt5Widgets >= %{qtbase_ver}
Obsoletes:	qt5-qtquickcontrols

%description -n Qt5Quick-controls
Qt5 Quick Controls, Dialogs, Layouts modules.

This package provides a set of widgets/controls that can be used to
build complete interfaces in Qt5 Quick (v2).

%description -n Qt5Quick-controls -l pl.UTF-8
Moduły Qt5 Quick Controls, Dialogs i Layouts.

Ten pakiet dostarcza zestaw widgetów/kontrolek, które można
wykorzystywać do tworzenia kompletnych interfejsów przy użyciu Qt5
Quick (v2).

%package doc
Summary:	Qt5 Quick Controls documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt5 Quick Controls w formacie HTML
Group:		Documentation
Requires:	qt5-doc-common >= %{qtbase_ver}
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description doc
Qt5 Quick Controls documentation in HTML format.

%description doc -l pl.UTF-8
Dokumentacja do biblioteki Qt5 Quick Controls w formacie HTML.

%package doc-qch
Summary:	Qt5 Quick Controls documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt5 Quick Controls w formacie QCH
Group:		Documentation
Requires:	qt5-doc-common >= %{qtbase_ver}
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description doc-qch
Qt5 Quick Controls documentation in QCH format.

%description doc-qch -l pl.UTF-8
Dokumentacja do biblioteki Qt5 Quick Controls w formacie QCH.

%prep
%setup -q -n %{orgname}-opensource-src-%{version} %{?with_qm:-a1}

%build
qmake-qt5
%{__make}
%{__make} %{!?with_qch:html_}docs

%if %{with qm}
cd qttranslations-opensource-src-%{version}
qmake-qt5
%{__make}
cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

%{__make} install_%{!?with_qch:html_}docs \
	INSTALL_ROOT=$RPM_BUILD_ROOT

%if %{with qm}
%{__make} -C qttranslations-opensource-src-%{version} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT
# keep only qtquickcontrols
%{__rm} $RPM_BUILD_ROOT%{_datadir}/qt5/translations/{assistant,designer,linguist,qmlviewer,qt,qtbase,qtconfig,qtconnectivity,qtdeclarative,qtlocation,qtmultimedia,qtquick1,qtscript,qtwebsockets,qtxmlpatterns}_*.qm
%endif

# find_lang --with-qm supports only PLD qt3/qt4 specific %{_datadir}/locale/*/LC_MESSAGES layout
find_qt5_qm()
{
	name="$1"
	find $RPM_BUILD_ROOT%{_datadir}/qt5/translations -name "${name}_*.qm" | \
		sed -e "s:^$RPM_BUILD_ROOT::" \
		    -e 's:\(.*/'$name'_\)\([a-z][a-z][a-z]\?\)\(_[A-Z][A-Z]\)\?\(\.qm\)$:%lang(\2\3) \1\2\3\4:'
}

echo '%defattr(644,root,root,755)' > qtquickcontrols.lang
%if %{with qm}
find_qt5_qm qtquickcontrols >> qtquickcontrols.lang
%endif

# no example sources installed, just built binary; clean up it
%{__rm} $RPM_BUILD_ROOT%{_examplesdir}/qt5/quick/dialogs/systemdialogs/systemdialogs

%clean
rm -rf $RPM_BUILD_ROOT

%files -n Qt5Quick-controls -f qtquickcontrols.lang
%defattr(644,root,root,755)
%doc README dist/changes-*
%dir %{qt5dir}/qml/QtQuick/Controls
%{qt5dir}/qml/QtQuick/Controls/Private
%{qt5dir}/qml/QtQuick/Controls/Styles
%attr(755,root,root) %{qt5dir}/qml/QtQuick/Controls/libqtquickcontrolsplugin.so
%{qt5dir}/qml/QtQuick/Controls/*.qml
%{qt5dir}/qml/QtQuick/Controls/plugins.qmltypes
%{qt5dir}/qml/QtQuick/Controls/qmldir
%dir %{qt5dir}/qml/QtQuick/Dialogs
%{qt5dir}/qml/QtQuick/Dialogs/Private
%attr(755,root,root) %{qt5dir}/qml/QtQuick/Dialogs/libdialogplugin.so
%{qt5dir}/qml/QtQuick/Dialogs/plugins.qmltypes
%{qt5dir}/qml/QtQuick/Dialogs/qmldir
%dir %{qt5dir}/qml/QtQuick/Extras
%{qt5dir}/qml/QtQuick/Extras/designer
%attr(755,root,root) %{qt5dir}/qml/QtQuick/Extras/libqtquickextrasplugin.so
%{qt5dir}/qml/QtQuick/Extras/plugins.qmltypes
%{qt5dir}/qml/QtQuick/Extras/qmldir
%dir %{qt5dir}/qml/QtQuick/Layouts
%attr(755,root,root) %{qt5dir}/qml/QtQuick/Layouts/libqquicklayoutsplugin.so
%{qt5dir}/qml/QtQuick/Layouts/plugins.qmltypes
%{qt5dir}/qml/QtQuick/Layouts/qmldir
%dir %{qt5dir}/qml/QtQuick/PrivateWidgets
%attr(755,root,root) %{qt5dir}/qml/QtQuick/PrivateWidgets/libwidgetsplugin.so
%{qt5dir}/qml/QtQuick/PrivateWidgets/plugins.qmltypes
%{qt5dir}/qml/QtQuick/PrivateWidgets/qmldir

%files doc
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtquickcontrols
%{_docdir}/qt5-doc/qtquickdialogs
%{_docdir}/qt5-doc/qtquickextras
%{_docdir}/qt5-doc/qtquicklayouts

%if %{with qch}
%files doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtquickcontrols.qch
%{_docdir}/qt5-doc/qtquickdialogs.qch
%{_docdir}/qt5-doc/qtquickextras.qch
%{_docdir}/qt5-doc/qtquicklayouts.qch
%endif
