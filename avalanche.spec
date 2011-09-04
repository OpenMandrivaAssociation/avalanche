%define		_filter_GLIBC_PRIVATE		1
%define		_disable_ld_no_undefined	1

Name:		avalanche
Version:	0.4
Release:	1
Summary:	Dynamic defect detection tool
License:	GPLv2
Group:		Development/Other
URL:		http://code.google.com/p/avalanche/
Source0:	http://avalanche.googlecode.com/files/avalanche-0.4.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gdb
BuildRequires:	glibc-static-devel
BuildRequires:	libgomp-devel
BuildRequires:	openmpi-devel

# mostly valgrind patches
Patch0:		avalanche-0.4.patch

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

#-----------------------------------------------------------------------
%files
%defattr(-,root,root,-)
%{_libexecdir}/%{name}
%{_bindir}/*
