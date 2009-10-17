#
# Conditional build:
%bcond_without	javadoc		# don't build javadoc
%bcond_without	tests		# don't build and run tests

%include	/usr/lib/rpm/macros.java
Summary:	Error-finding tool based on static analysis
Summary(pl.UTF-8):	Narzędzie do znajdowania błędów na podstawie statycznej analizy kodu.
Name:		stanse
Version:	1.0.0
Release:	0.1
License:	GPL v2
Group:		Development/Languages/Java
Source0:	http://stanse.fi.muni.cz/download/%{name}-%{version}.tar.bz2
Source1:	%{name}.sh
# Source0-md5:	e281d21df3fe162cd525df7002a36c8a
URL:		http://stanse.fi.muni.cz/
BuildRequires:	ant
BuildRequires:	ant-antlr3
BuildRequires:	ant-cpptasks
BuildRequires:	java-sun
BuildRequires:	jpackage-utils
BuildRequires:	rpm >= 4.4.9-56
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	gcc
Requires:	make
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Stanse is an error-finding tool based on static analysis. The aim of
this project is to research, evaluate and implement modern approaches
to automatic bug finding for programs written in procedural languages
related to C (C/C++/C#/Java). Currently this software tool is able to
automatically discover some types of bugs in real-life sized projects
(e.g. the Linux kernel).

Its main features are:

 - Target language is C (ANSI C99), but extensible to C#/C++/Java.
 - Full ANSI C99 support, including most GNU C extensions.
 - Modular structure, easy extensibility, fast development.
 - Easy to use interface and error path inspection.
 - Makefile support and batch execution.

It is able to detect following kinds of errors:

 - Memory allocation errors (null pointers, memory leaks, dangling
   pointers)
 - Bad locking discipline (double locks/unlocks, locks not released
   etc.)
 - Interrupt handling (cli/sti-style).
 - And all the errors which can be described by state automata.

%description -l pl.UTF-8
Stanse jest narzędziem do znajdowania błędów w oprogramowaniu na
podstawie statycznej analizy kodu. Celem projektu jest rozwijanie,
ocena i implementacja nowoczesnych metod automatycznego znajdowania
błędów w programach napisanych w językach proceduralnych pokrewnych C
(C/C++/C#/Java). Narzędzie to jest w stanie automatycznie odkryć pewne
rodzaje błędów w dużych projektach takich jak jądro systemu Linux.

Główna cechy stanse, to:

 - obsługa języka C (ANSI C99), rozszerzalna do C#/C++/Java
 - pełne wsparcie ANSII C99, włączając większość rozszerzeń GNU C
 - rozszerzalna, modularna struktura
 - łatwy w użyciu interfejs
 - wsparcie dla Makefile
 - możliwość pracy nie interaktywnej

Stanse jest w stanie wykryć następujące typy błędów:

 - Błędy alokacji pamięci
 - Błędy związane z blokadami
 - Błędy obsługi przerwań
 - Wszelkie błędy, które można opisać przy użyciu automatów skończonych

%package javadoc
Summary:	Online manual for %{name}
Summary(pl.UTF-8):	Dokumentacja online do %{name}
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Documentation for %{name}.

%description javadoc -l pl.UTF-8
Dokumentacja do %{name}.

%description javadoc -l fr.UTF-8
Javadoc pour %{name}.

%prep
%setup -q

%build
export JAVA_HOME="%{java_home}"

required_jars="antlr3 ant/ant ant/ant-antlr3 ant/ant-cpptasks"
CLASSPATH=$(build-classpath $required_jars)
export CLASSPATH

export LC_ALL=en_US # source code not US-ASCII

%ant jar %{?with_javadoc:javadoc}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_javadir},%{_bindir},%{_datadir}/stanse}

# jars
cp -a dist/%{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

# files
cp -a dist/bin $RPM_BUILD_ROOT%{_datadir}/stanse/bin
cp -a dist/data $RPM_BUILD_ROOT%{_datadir}/stanse/data
cp -a dist/lib $RPM_BUILD_ROOT%{_datadir}/stanse/lib
cp dist/properties.xml $RPM_BUILD_ROOT%{_datadir}/stanse/properties.xml
cp %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/stanse

# javadoc
%if %{with javadoc}
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -a dist/javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{name}-%{version} %{_javadocdir}/%{name}

%files
%defattr(644,root,root,755)
%doc README SUCCESS_STORIES TODO.txt WISH.txt
%{_javadir}/*.jar
%dir %{_datadir}/%{name}
%attr(755,root,root) %{_datadir}/%{name}/bin
%{_datadir}/%{name}/lib
%{_datadir}/%{name}/data
%{_datadir}/%{name}/properties.xml
%attr(755,root,root) %{_bindir}/stanse

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}
%ghost %{_javadocdir}/%{name}
%endif
