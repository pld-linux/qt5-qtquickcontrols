#
# Conditional build:
%bcond_without	doc	# Documentation
%bcond_without	qm	# QM translations

%define		orgname		qtquickcontrols
%define		qtbase_ver		%{version}
%define		qtdeclarative_ver	5.12.3-2
%define		qttools_ver		%{version}
Summary:	The Qt5 Quick Controls modules
Summary(pl.UTF-8):	Moduły Qt5 Quick Controls
Name:		qt5-%{orgname}
Version:	5.15.16
Release:	1
License:	LGPL v3 or GPL v2 or GPL v3 or commercial
Group:		X11/Libraries
Source0:	https://download.qt.io/official_releases/qt/5.15/%{version}/submodules/%{orgname}-everywhere-opensource-src-%{version}.tar.xz
# Source0-md5:	99cc215eaa6db82db43a3d4a0dd50d1b
Source1:	https://download.qt.io/official_releases/qt/5.15/%{version}/submodules/qttranslations-everywhere-opensource-src-%{version}.tar.xz
# Source1-md5:	2f9320ff53b3cb51482cd45eec25a470
URL:		https://www.qt.io/
BuildRequires:	Qt5Core-devel >= %{qtbase_ver}
BuildRequires:	Qt5Gui-devel >= %{qtbase_ver}
BuildRequires:	Qt5Qml-devel >= %{qtdeclarative_ver}
BuildRequires:	Qt5Quick-devel >= %{qtdeclarative_ver}
BuildRequires:	Qt5Widgets-devel >= %{qtbase_ver}
%if %{with doc}
BuildRequires:	qt5-assistant >= %{qttools_ver}
%endif
BuildRequires:	qt5-build >= %{qtbase_ver}
%{?with_qm:BuildRequires:	qt5-linguist >= %{qttools_ver}}
BuildRequires:	qt5-qmake >= %{qtbase_ver}
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.016
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	-fno-strict-aliasing
%define		qt5dir		%{_libdir}/qt5

%description
Qt is a cross-platform application and UI framework. Using Qt, you can
write web-enabled applications once and deploy them across desktop,
mobile and embedded systems without rewriting the source code.

This package contains Qt5 Quick Controls, Dialogs modules.

%description -l pl.UTF-8
Qt to wieloplatformowy szkielet aplikacji i interfejsów użytkownika.
Przy użyciu Qt można pisać aplikacje powiązane z WWW i wdrażać je w
systemach biurkowych, przenośnych i wbudowanych bez przepisywania kodu
źródłowego.

Ten pakiet zawiera moduły Qt5 Quick Controls, Dialogs.

%package -n Qt5Quick-controls
Summary:	The Qt5 Quick Controls modules
Summary(pl.UTF-8):	Moduły Qt5 Quick Controls
Group:		X11/Libraries
%requires_eq_to	Qt5Core Qt5Core-devel
Requires:	Qt5Gui >= %{qtbase_ver}
Requires:	Qt5Qml >= %{qtdeclarative_ver}
Requires:	Qt5Quick >= %{qtdeclarative_ver}
Requires:	Qt5Widgets >= %{qtbase_ver}
Obsoletes:	qt5-qtquickcontrols < 5.3.0

%description -n Qt5Quick-controls
Qt5 Quick Controls, Dialogs modules.

This package provides a set of widgets/controls that can be used to
build complete interfaces in Qt5 Quick (v2).

%description -n Qt5Quick-controls -l pl.UTF-8
Moduły Qt5 Quick Controls, Dialogs.

Ten pakiet dostarcza zestaw widgetów/kontrolek, które można
wykorzystywać do tworzenia kompletnych interfejsów przy użyciu Qt5
Quick (v2).

%package doc
Summary:	Qt5 Quick Controls documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt5 Quick Controls w formacie HTML
Group:		Documentation
Requires:	qt5-doc-common >= %{qtbase_ver}
BuildArch:	noarch

%description doc
Qt5 Quick Controls documentation in HTML format.

%description doc -l pl.UTF-8
Dokumentacja do biblioteki Qt5 Quick Controls w formacie HTML.

%package doc-qch
Summary:	Qt5 Quick Controls documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt5 Quick Controls w formacie QCH
Group:		Documentation
Requires:	qt5-doc-common >= %{qtbase_ver}
BuildArch:	noarch

%description doc-qch
Qt5 Quick Controls documentation in QCH format.

%description doc-qch -l pl.UTF-8
Dokumentacja do biblioteki Qt5 Quick Controls w formacie QCH.

%package examples
Summary:	Qt5 Quick Controls examples
Summary(pl.UTF-8):	Przykłady do bibliotek Qt5 Quick Controls
Group:		X11/Development/Libraries
BuildArch:	noarch

%description examples
Qt5 Quick Controls examples.

%description examples -l pl.UTF-8
Przykłady do bibliotek Qt5 Quick Controls.

%prep
%setup -q -n %{orgname}-everywhere-src-%{version} %{?with_qm:-a1}

%build
%{qmake_qt5}
%{__make}
%{?with_doc:%{__make} docs}

%if %{with qm}
cd qttranslations-everywhere-src-%{version}
%{qmake_qt5}
%{__make}
cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

%if %{with doc}
%{__make} install_docs \
	INSTALL_ROOT=$RPM_BUILD_ROOT
%endif

%if %{with qm}
%{__make} -C qttranslations-everywhere-src-%{version} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT
# keep only qtquickcontrols
%{__rm} $RPM_BUILD_ROOT%{_datadir}/qt5/translations/{assistant,designer,linguist,qt,qtbase,qtconnectivity,qtdeclarative,qtlocation,qtmultimedia,qtquickcontrols2,qtserialport,qtscript,qtwebengine,qtwebsockets,qtxmlpatterns}_*.qm
%endif

# Prepare some files list
ifecho() {
	r="$RPM_BUILD_ROOT$2"
	if [ -d "$r" ]; then
		echo "%%dir $2" >> $1.files
	elif [ -x "$r" ] ; then
		echo "%%attr(755,root,root) $2" >> $1.files
	elif [ -f "$r" ]; then
		echo "$2" >> $1.files
	else
		echo "Error generation $1 files list!"
		echo "$r: no such file or directory!"
		return 1
	fi
}
ifecho_tree() {
	ifecho $1 $2
	for f in `find $RPM_BUILD_ROOT$2 -printf "%%P "`; do
		ifecho $1 $2/$f
	done
}

echo "%defattr(644,root,root,755)" > examples.files
ifecho_tree examples %{_examplesdir}/qt5/quickcontrols

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

%clean
rm -rf $RPM_BUILD_ROOT

%files -n Qt5Quick-controls -f qtquickcontrols.lang
%defattr(644,root,root,755)
%doc README dist/changes-*
%dir %{qt5dir}/qml/QtQuick/Controls
%{qt5dir}/qml/QtQuick/Controls/Private
%{qt5dir}/qml/QtQuick/Controls/Styles
# R: Core Gui Qml Quick Widgets
%attr(755,root,root) %{qt5dir}/qml/QtQuick/Controls/libqtquickcontrolsplugin.so
%{qt5dir}/qml/QtQuick/Controls/*.qml
%{qt5dir}/qml/QtQuick/Controls/*.qmlc
%{qt5dir}/qml/QtQuick/Controls/plugins.qmltypes
%{qt5dir}/qml/QtQuick/Controls/qmldir
%dir %{qt5dir}/qml/QtQuick/Dialogs
%{qt5dir}/qml/QtQuick/Dialogs/Private
# R: Core Gui Qml Quick
%attr(755,root,root) %{qt5dir}/qml/QtQuick/Dialogs/libdialogplugin.so
%{qt5dir}/qml/QtQuick/Dialogs/*.qml
%{qt5dir}/qml/QtQuick/Dialogs/*.qmlc
%{qt5dir}/qml/QtQuick/Dialogs/images
%{qt5dir}/qml/QtQuick/Dialogs/plugins.qmltypes
%{qt5dir}/qml/QtQuick/Dialogs/qml
%{qt5dir}/qml/QtQuick/Dialogs/qmldir
%dir %{qt5dir}/qml/QtQuick/Extras
%{qt5dir}/qml/QtQuick/Extras/designer
# R: Core Gui Qml Quick
%attr(755,root,root) %{qt5dir}/qml/QtQuick/Extras/libqtquickextrasplugin.so
%{qt5dir}/qml/QtQuick/Extras/*.qml
%{qt5dir}/qml/QtQuick/Extras/*.qmlc
%{qt5dir}/qml/QtQuick/Extras/plugins.qmltypes
%{qt5dir}/qml/QtQuick/Extras/qmldir
%{qt5dir}/qml/QtQuick/Extras/Private
%dir %{qt5dir}/qml/QtQuick/PrivateWidgets
# R: Core Gui Qml Quick Widgets
%attr(755,root,root) %{qt5dir}/qml/QtQuick/PrivateWidgets/libwidgetsplugin.so
%{qt5dir}/qml/QtQuick/PrivateWidgets/plugins.qmltypes
%{qt5dir}/qml/QtQuick/PrivateWidgets/qmldir

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtquickcontrols1
%{_docdir}/qt5-doc/qtquickdialogs
%{_docdir}/qt5-doc/qtquickextras

%files doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtquickcontrols1.qch
%{_docdir}/qt5-doc/qtquickdialogs.qch
%{_docdir}/qt5-doc/qtquickextras.qch
%endif

%files examples -f examples.files
%defattr(644,root,root,755)
# XXX: dir shared with qt5-qtbase-examples
%dir %{_examplesdir}/qt5
