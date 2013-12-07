Summary:	Optional user space component for Host AP driver
Name:		hostapd
Version:	2.0
Release:	6
License:	GPLv2
Group:		System/Servers
Url:		http://hostap.epitest.fi/hostapd/
Source0:	http://hostap.epitest.fi/releases/%{name}-%{version}.tar.gz
Source1:	%{name}.init
Source2:	%{name}-config-build
Source3:	%{name}.service
Patch0:		%{name}-config.patch
Patch2:		hostapd-1.0-tls_length_fix.patch

BuildRequires:	systemd-units
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
%apply_patches
pushd %{name}
cp %{SOURCE2} .config
popd

%build
pushd %{name}
sed -i -e 's/CFLAGS =.*/CFLAGS = -MMD %{optflags}/' Makefile
%make CC="%{__cc}" #CFLAGS="-MMD %{optflags}"
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

%if %mdvver < 201200
install -pm 0755 %{SOURCE1}   %{buildroot}%{_initrddir}/%{name}
%else
install -pm 644 %{SOURCE3}   %{buildroot}/%{_unitdir}/%{name}.service
%endif

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
%if %mdvver < 201200
%config(noreplace) %{_initrddir}/%{name}
%else
%config(noreplace) %{_unitdir}/%{name}.service
%endif
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.accept
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.deny

