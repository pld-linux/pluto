#
# Conditional build:
%bcond_without	javadoc		# don't build javadoc
%bcond_with	tests		# run tests (takes long time)
%bcond_with	java_sun	# build using java-sun

%include	/usr/lib/rpm/macros.java

Summary:	pluto
Summary(pl.UTF-8):	pluto
Name:		pluto
Version:	1.0.1
Release:	0.1
License:	Apache v2.0
Group:		Development/Languages/Java
Source0:	pluto-%{version}.tar.bz2
# Source0-md5:	d6355e173ebda88b4a2da4f7df688875
URL:		http://portals.apache.org/pluto/
BuildRequires:	ant
BuildRequires:	jdk
Requires:	jpackage-utils
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description

%description -l pl.UTF-8

%package javadoc
Summary:	Online manual for pluto
Summary(pl.UTF-8):	Dokumentacja online do pluto
Group:		Documentation
Requires:	jpackage-utils
Obsoletes:	jakarta-commons-io-javadoc

%description javadoc
Documentation for pluto.

%description javadoc -l pl.UTF-8
Dokumentacja do pluto.

%description javadoc -l fr.UTF-8
Javadoc pour pluto.

%prep
%setup -q

%build
%ant %{!?with_java_sun:-Dbuild.compiler=extJavac} all

%if %{with tests}
JUNITJAR=$(find-jar junit)
%ant -Djunit.jar=$JUNITJAR test
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}

cp -a %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}
ln -sf %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

# javadoc
%if %{with javadoc}
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -a target/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{name}-%{version} %{_javadocdir}/%{name}

%files
%defattr(644,root,root,755)
%{_javadir}/*.jar

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}
%ghost %{_javadocdir}/%{name}
%endif
