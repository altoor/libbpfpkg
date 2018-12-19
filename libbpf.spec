%global 	kver		4.19
%global		kurl		https://cdn.kernel.org/pub/linux/kernel/v4.x/
%global		bpf_dir		tools/lib/bpf/
%global		bpf_script	libbpf.map

Name:		libbpf
Version:	0.0.1
Release:	2%{?dist}
Summary:	ebpf library

Group:		Development/Libraries
License:	LGPL-2.1
URL:		https://github.com/libbpf/libbpf
Source0:	%{kurl}linux-%{kver}.tar.gz
Source1:	if_vlan.h

BuildRequires: make gcc elfutils-libelf-devel
%if 0%{?fedora} >= 29
BuildRequires: python3-docutils
%else
BuildRequires: python2-docutils
BuildRequires: python3
%endif

%description
helpers library for eBPF program manipulation and interaction from user-space.

%package devel
Summary:	Libraries and header files for the libbpf library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package provides the libraries, include files, and other
resources needed for developing libbpf applications.

%prep
%setup -q -n linux-%{kver}

%build
./scripts/bpf_helpers_doc.py \
	--filename include/uapi/linux/bpf.h > bpf-helpers.rst
rst2man bpf-helpers.rst > bpf-helpers.7
cd %{bpf_dir}
make %{?_smp_mflags} V=1

# HACK: re-link with soname
if [ -f %{bpf_script} ]; then
	gcc --shared libbpf-in.o -Wl,--version-script=%{bpf_script} \
		-Wl,-soname=libbpf.so.%{version} -o libbpf.so.%{version}
else
	gcc --shared  libbpf-in.o -Wl,-soname=libbpf.so.%{version} \
		-o libbpf.so.%{version}
fi
rm -f libbpf.so
ln -s libbpf.so.%{version} libbpf.so

%install
%{__mkdir} -p %{buildroot}%{_libdir} %{buildroot}%{_includedir}/bpf \
	%{buildroot}%{_mandir}/man7/
%{__install} -m 0755 %{bpf_dir}/libbpf.so %{buildroot}%{_libdir}
%{__install} -m 0777 %{bpf_dir}/libbpf.so.%{version} %{buildroot}%{_libdir}
%{__install} -m 644 %{bpf_dir}/libbpf.h %{buildroot}%{_includedir}/bpf/
%{__install} -m 644 %{bpf_dir}/bpf.h %{buildroot}%{_includedir}/bpf/
%{__install} -m 644 tools/testing/selftests/bpf/bpf_helpers.h %{buildroot}%{_includedir}/bpf/
# HACK: kernel uapi headers lack vlan definition add them here
%{__install} -m 644 %{SOURCE1} %{buildroot}%{_includedir}/bpf/
%{__install} -m 644 bpf-helpers.7 %{buildroot}%{_mandir}/man7/

%files
%{_libdir}/libbpf.so.%{version}

%files devel
%{_libdir}/libbpf.so
%{_includedir}/bpf/*.h
%doc %{_mandir}/man7/bpf-helpers.7*

%changelog
* Wed Dec 19 2018 Paolo Abeni <pabeni@redhat.com> - 0.0.1-2
- added vlan header

* Tue Dec 18 2018 Paolo Abeni <pabeni@redhat.com> - 0.0.1-1
- first version
