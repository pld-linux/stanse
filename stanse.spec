#
# Conditional build:
%bcond_without	javadoc		# don't build javadoc
%bcond_without	tests		# don't build and run tests

%if "%{pld_release}" == "ti"
%bcond_without	java_sun	# build with gcj
%else
%bcond_with	java_sun	# build with java-sun
%endif
#
%include	/usr/lib/rpm/macros.java

Summary:	stanse
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
%{!?with_java_sun:BuildRequires:	java-gcj-compat-devel}
%{?with_java_sun:BuildRequires:	java-sun}
BuildRequires:	jpackage-utils
BuildRequires:	rpm >= 4.4.9-56
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
stanse

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
install -d $RPM_BUILD_ROOT{%{_javadir},%{_bindir}}

# jars
cp -a dist/%{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar
cp -a dist/lib $RPM_BUILD_ROOT%{_javadir}/%{name}

# scripts
cp dist/bin/* $RPM_BUILD_ROOT%{_bindir}
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
%{_javadir}/*.jar
%{_javadir}/%{name}
%attr(755,root,root) %{_bindir}/*

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}
%ghost %{_javadocdir}/%{name}
%endif
