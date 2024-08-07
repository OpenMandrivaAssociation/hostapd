%define _disable_lto 1

Summary:	Optional user space component for Host AP driver
Name:		hostapd
Version:	2.11
Release:	1
License:	GPLv2
Group:		System/Servers
Url:		https://hostap.epitest.fi/hostapd/
Source0:	https://w1.fi/releases/%{name}-%{version}.tar.gz
Source2:	%{name}-config-build
Source3:	%{name}.service
Patch0:		%{name}-config.patch
Patch2:		hostapd-1.0-tls_length_fix.patch

BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	pkgconfig(libnl-3.0)
BuildRequires:	pkgconfig(openssl)
Requires(post,preun):	rpm-helper
Requires(post,preun,postun):	sysvinit

%description
Hostapd is an optional user space component for Host AP driver. It adds
more features to the basic IEEE 802.11 management included in the kernel
driver: using external RADIUS authentication server for MAC address
based access control, IEEE 802.1X Authenticator and dynamic WEP keying,
RADIUS accounting.

%prep
%setup -q
%autopatch -p1
pushd %{name}
cp %{SOURCE2} .config
echo "CC = %{__cc}" >> .config
popd

%build
%set_build_flags
pushd %{name}
sed -i -e 's/CFLAGS =.*/CFLAGS = -MMD %{optflags}/' Makefile
%make CC="%{__cc}" #CFLAGS="-MMD %{optflags}"
popd

%install
pushd %{name}
install -d -m 755 %{buildroot}%{_sbindir}
install -d -m 755 %{buildroot}%{_sysconfdir}/%{name}
install -d -m 755 %{buildroot}/%{_unitdir}
install -m 755 %{name}        %{buildroot}%{_sbindir}
install -m 755 %{name}_cli    %{buildroot}%{_sbindir}
install -m 600 %{name}.conf   %{buildroot}%{_sysconfdir}/%{name}
install -m 644 %{name}.accept %{buildroot}%{_sysconfdir}/%{name}
install -m 644 %{name}.deny   %{buildroot}%{_sysconfdir}/%{name}

install -pm 644 %{SOURCE3}   %{buildroot}/%{_unitdir}/%{name}.service

popd

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%postun
%_postun_userdel %{name}

%files
%doc %{name}/ChangeLog %{name}/README
%{_sbindir}/%{name}
%{_sbindir}/%{name}_cli
%config(noreplace) %{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.accept
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.deny
