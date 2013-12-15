#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	parsec
Summary:	Monadic parser combinators
Summary(pl.UTF-8):	Monadowe kombinatory analizatorów
Name:		ghc-%{pkgname}
Version:	3.1.4
Release:	1
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/parsec
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	22fe2b1ebaad74ae3d00d066c3046314
URL:		http://hackage.haskell.org/package/parsec
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-base >= 3.0.3
BuildRequires:	ghc-base < 5
BuildRequires:	ghc-bytestring
BuildRequires:	ghc-mtl
BuildRequires:	ghc-text >= 0.2
BuildRequires:	ghc-text < 1.1
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-base-prof >= 3.0.3
BuildRequires:	ghc-base-prof < 5
BuildRequires:	ghc-bytestring-prof
BuildRequires:	ghc-mtl-prof
BuildRequires:	ghc-text-prof >= 0.2
BuildRequires:	ghc-text-prof < 1.1
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Requires:	ghc-base >= 3.0.3
Requires:	ghc-base < 5
Requires:	ghc-bytestring
Requires:	ghc-mtl
Requires:	ghc-text >= 0.2
Requires:	ghc-text < 1.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
Parsec is designed from scratch as an industrial-strength parser
library. It is simple, safe, well documented (on the package
homepage), has extensive libraries and good error messages, and is
also fast. It is defined as a monad transformer that can be stacked on
arbitrary monads, and it is also parametric in the input stream type.

%description -l pl.UTF-8
Parsec został zaprojektowany od początku jako biblioteka analizatorów
o przemysłowych możliwościach. Jest prosta, bezpieczna, dobrze
udokumentowana (na stronie domowej pakietu), ma obszerne biblioteki i
dobre komunikaty błędów, a także jest szybka. Analizator jest
zdefiniowany jako transformator monad, który można stosować na
dowolnych monadach; jest także parametryzowany typem strumienia
wejściowego.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-base-prof >= 3.0.3
Requires:	ghc-base-prof < 5
Requires:	ghc-bytestring-prof
Requires:	ghc-mtl-prof
Requires:	ghc-text-prof >= 0.2
Requires:	ghc-text-prof < 1.1

%description prof
Profiling %{pkgname} library for GHC. Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%package doc
Summary:	HTML documentation for ghc %{pkgname} package
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}
Group:		Documentation

%description doc
HTML documentation for ghc %{pkgname} package.

%description doc -l pl.UTF-8
Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/html %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc CHANGES LICENSE
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/HSparsec-%{version}.o
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSparsec-%{version}.a
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Parsec.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Parsec
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Parsec/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Parsec/ByteString
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Parsec/ByteString/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Parsec/Text
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Parsec/Text/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/ParserCombinators
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/ParserCombinators/Parsec.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/ParserCombinators/Parsec
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/ParserCombinators/Parsec/*.hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSparsec-%{version}_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Parsec.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Parsec/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Parsec/ByteString/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Parsec/Text/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/ParserCombinators/Parsec.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/ParserCombinators/Parsec/*.p_hi
%endif

%files doc
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
