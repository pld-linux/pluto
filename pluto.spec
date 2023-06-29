Summary:	PLUTO automatic parallelizer
Summary(pl.UTF-8):	PLUTO - automatyczny zrównoleglacz
Name:		pluto
Version:	0.11.4
Release:	7
License:	LGPL v2.1+ (library), GPL v3+ (tools)
Group:		Libraries
# monitor also https://github.com/bondhugula/pluto/releases
Source0:	http://downloads.sourceforge.net/pluto-compiler/%{name}-%{version}.tar.gz
# Source0-md5:	2ad2e3305ea480b1c2aefd2cc90f38a1
Patch0:		%{name}-system-libs.patch
Patch1:		%{name}-updates.patch
Patch2:		%{name}-include.patch
Patch3:		%{name}-link.patch
URL:		http://pluto-compiler.sourceforge.net/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	candl-devel >= 0.6.2-1.20120728
BuildRequires:	clan-devel >= 0.8.0
BuildRequires:	cloog-isl-devel >= 0.19.0
BuildRequires:	gcc >= 6:4.2
BuildRequires:	isl-devel >= 0.13
BuildRequires:	libgomp-devel
BuildRequires:	libtool
BuildRequires:	osl-devel >= 0.9.0
BuildRequires:	piplib-devel >= 1.4.0
BuildRequires:	polylib-devel >= 5.22.5
Requires:	candl >= 0.6.2-1.20120728
Requires:	clan >= 0.8.0
Requires:	cloog-isl-libs >= 0.19.0
Requires:	isl >= 0.13
Requires:	osl >= 0.9.0
Requires:	piplib >= 1.4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PLUTO is an automatic source-to-source transformer that can optimize
nested loop sequences for coarse-grained parallelism and cache
locality simultaneously. OpenMP parallel code for multicores can be
generated from regular C program sections.

%description -l pl.UTF-8
PLUTO to automatyczne narzędzie operujące na kodzie źródłowy,
potrafiące optymalizować sekwencje zagnieżdżonych pętli pod kątem
zrównoleglenia i lokalizacji pamięci podręcznej. Można generować kod
równoległy OpenMP ze zwykłych sekcji programu w C.

%package devel
Summary:	Header files for Pluto library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Pluto
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	candl-devel >= 0.6.2-1.20120728
Requires:	clan-devel >= 0.8.0
Requires:	cloog-isl-devel >= 0.19.0
Requires:	isl-devel >= 0.13
Requires:	libgomp-devel
Requires:	osl-devel >= 0.9.0
Requires:	piplib-devel >= 1.4.0

%description devel
Header files for Pluto library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Pluto.

%package static
Summary:	Static Pluto library
Summary(pl.UTF-8):	Statyczna biblioteka Pluto
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Pluto library.

%description static -l pl.UTF-8
Statyczna biblioteka Pluto.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules
%{__make} \
	OPT_FLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# installed by mistake
%{__rm} $RPM_BUILD_ROOT%{_bindir}/getversion.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ACKS AUTHORS ChangeLog README
%attr(755,root,root) %{_bindir}/ploog
%attr(755,root,root) %{_bindir}/plorc
%attr(755,root,root) %{_bindir}/pluto
%attr(755,root,root) %{_bindir}/plutune
%attr(755,root,root) %{_bindir}/polycc
%attr(755,root,root) %{_bindir}/vloog
%attr(755,root,root) %{_libdir}/libpluto.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpluto.so.0

%files devel
%defattr(644,root,root,755)
%doc doc/{DOC.txt,pluto.bib}
%attr(755,root,root) %{_libdir}/libpluto.so
%{_libdir}/libpluto.la
%{_includedir}/pluto

%files static
%defattr(644,root,root,755)
%{_libdir}/libpluto.a
