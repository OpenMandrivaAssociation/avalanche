%define		_filter_GLIBC_PRIVATE		1
%define		_disable_ld_no_undefined	1

Name:		avalanche
Version:	0.6.0
Release:	2
Summary:	Dynamic defect detection tool
License:	Apache and GPLv2 and MIT
Group:		Development/Other
URL:		http://code.google.com/p/avalanche/
Source0:	http://avalanche.googlecode.com/files/avalanche-0.6.tar.gz
Source1:	http://avalanche.googlecode.com/files/avalanche.pdf
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gdb
BuildRequires:	glibc-static-devel
BuildRequires:	libgomp-devel
BuildRequires:	libstdc++-static-devel
BuildRequires:	openmpi-devel

Patch0:		avalanche-0.6-pic.patch
# http://www.google.com/url?sa=D&q=http://code.google.com/p/avalanche/downloads/detail%3Fname%3DSTP_PL_patch&usg=AFQjCNEVUq9C1_2Azei4LlVN1372RpOCbQ
Patch1:		avalanche-0.6-byacc.patch
Patch2:		avalanche-0.6-glibc.patch
Patch3:		avalanche-0.6-gcc47.patch

%description
Avalanche is a dynamic defect detection tool that generates
"inputs of death" - input data reproducing critical bugs and
vulnerabilities in the analysed program.

Avalanche overview
+ Automatically finds critical software errors
+ Generates "input of death" for each detected error
+ Tracks the flow of "tainted" data in the program
+ Iteratively generates a sequence of inputs to increase the
  coverage and find new errors
+ Implements dynamic analysis based on open-source Valgrind framework,
  and STP (Simple Theorem Prover)
+ Runs on x86/Linux and x86_64/Linux

#-----------------------------------------------------------------------
%prep
%setup -q
%patch0 -p1
%patch1 -p0
%patch2 -p1
%patch3 -p1

#-----------------------------------------------------------------------
%build
%configure	--prefix=%{_libexecdir}/%{name}			\
		--exec-prefix=%{_libexecdir}/%{name}		\
		--bindir=%{_libexecdir}/%{name}/bin		\
		--libdir=%{_libexecdir}/%{name}			\
		--libexecdir=%{_libexecdir}/%{name}
perl -pi -e 's/^(INCLUDES = .*)/$1 \$\(DEFAULT_INCLUDES\)/'	\
    stp-ver-0.1-11-18-2008/parser/Makefile
make

#-----------------------------------------------------------------------
%install
export EXCLUDE_FROM_STRIP=%{_libexecdir}/%{name}/valgrind/*.so
%makeinstall_std
rm -fr %{buildroot}%{_datadir}
rm -fr %{buildroot}%{_includedir}
rm -fr %{buildroot}%{_libexecdir}/%{name}/pkgconfig

mkdir -p %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/%{name} << EOF
#!/bin/sh

export PATH=%{_libexecdir}/%{name}/bin:\$PATH
%{name} "\$@"
EOF
chmod +x %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_docdir}/%{name}
install -m644 README %{SOURCE1} %{buildroot}%{_docdir}/%{name}

#-----------------------------------------------------------------------
%files
%defattr(-,root,root,-)
%{_libexecdir}/%{name}
%{_bindir}/*
%doc %{_docdir}/%{name}
