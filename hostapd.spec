%define name	hostapd
%define version	0.7.3
%define subrel	1
%define release %mkrel 2

Name:		%{name}
Version:	%{version}
Release:	%{release}
URL:		http://hostap.epitest.fi/hostapd/
Group:		System/Servers
Source0:	%{name}-%version.tar.gz
Source1:	%{name}.init
Source2:	%{name}-config-build
Patch0:		%{name}-config.patch
Summary:	Optional user space component for Host AP driver
License:	GPL
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
BuildRequires:	libopenssl-devel
BuildRequires:	madwifi-source libnl-devel
Requires(post):	rpm-helper
Requires(preun): rpm-helper
Requires(postun): rpm-helper
Requires:	hostap-utils

%description
Hostapd is an optional user space component for Host AP driver. It adds 
more features to the basic IEEE 802.11 management included in the kernel 
driver: using external RADIUS authentication server for MAC address 
based access control, IEEE 802.1X Authenticator and dynamic WEP keying, 
RADIUS accounting. 

%prep
%setup -q -n %{name}-%{version}
%patch0 -p0 -b .mdkconf 
pushd %{name}
cp %{SOURCE2} .config
popd

%build
pushd %{name}
%{__perl} -pi -e 's/CFLAGS =.*/CFLAGS = -MMD %{optflags}/' Makefile
%{__make} CC="%{__cc}" #CFLAGS="-MMD % {optflags}"
popd

%install
pushd %{name}
install -d -m 755 %{buildroot}%{_sbindir}
install -d -m 755 %{buildroot}%{_sysconfdir}/%{name}
install -d -m 755 %{buildroot}%{_initrddir}
install -m 755 %{name} %{buildroot}%{_sbindir}
install -m 755 %{name}_cli %{buildroot}%{_sbindir}
install -m 644 %{name}.conf %{buildroot}%{_sysconfdir}/%{name}
install -m 644 %{name}.accept %{buildroot}%{_sysconfdir}/%{name}
install -m 644 %{name}.deny %{buildroot}%{_sysconfdir}/%{name}
install -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}
popd

%clean
rm -rf %{buildroot}

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%postun
%_postun_userdel %{name}

%files
%defattr(-,root,root)
%doc %{name}/ChangeLog %{name}/README %{name}/README-WPS
%{_sbindir}/%{name}
%{_sbindir}/%{name}_cli
%config(noreplace) %{_initrddir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.accept
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.deny


