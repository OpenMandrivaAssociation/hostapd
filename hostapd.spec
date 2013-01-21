%define name	hostapd
%define version	2.0
%define release 1

Name:		%{name}
Version:	%{version}
Release:	%{release}
URL:		http://hostap.epitest.fi/hostapd/
Group:		System/Servers
Source0:	http://hostap.epitest.fi/releases/%{name}-%version.tar.gz
Source1:	%{name}.init
Source2:	%{name}-config-build
Source3:        %{name}.service
Patch0:		%{name}-config.patch
Patch2:		hostapd-1.0-tls_length_fix.patch
Summary:	Optional user space component for Host AP driver
License:	GPL
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(libnl-3.0)
Requires(post):  rpm-helper
Requires(preun): rpm-helper
BuildRequires:    systemd-units
Requires(post):   sysvinit
Requires(preun):  sysvinit
Requires(postun): sysvinit

%description
Hostapd is an optional user space component for Host AP driver. It adds 
more features to the basic IEEE 802.11 management included in the kernel 
driver: using external RADIUS authentication server for MAC address 
based access control, IEEE 802.1X Authenticator and dynamic WEP keying, 
RADIUS accounting. 

%prep
%setup -q -n %{name}-%{version}
%patch0 -p0 -b .mdkconf
%patch2 -p1 -b .tls
pushd %{name}
cp %{SOURCE2} .config
popd

%build
pushd %{name}
%{__perl} -pi -e 's/CFLAGS =.*/CFLAGS = -MMD %{optflags}/' Makefile
%{__make} CC="%{__cc}" #CFLAGS="-MMD %{optflags}"
popd

%install
pushd %{name}
install -d -m 755 %{buildroot}%{_sbindir}
install -d -m 755 %{buildroot}%{_sysconfdir}/%{name}
install -d -m 755 %{buildroot}%{_initrddir}
install -d -m 755 %{buildroot}/%{_unitdir}
install -m 755 %{name}        %{buildroot}%{_sbindir}
install -m 755 %{name}_cli    %{buildroot}%{_sbindir}
install -m 600 %{name}.conf   %{buildroot}%{_sysconfdir}/%{name}
install -m 644 %{name}.accept %{buildroot}%{_sysconfdir}/%{name}
install -m 644 %{name}.deny   %{buildroot}%{_sysconfdir}/%{name}
install -pm 0755 %{SOURCE1}   %{buildroot}%{_initrddir}/%{name}
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
%config(noreplace) %{_initrddir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.accept
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.deny
%config(noreplace) %{_unitdir}/%{name}.service
