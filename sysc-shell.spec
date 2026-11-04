%global debug_package %{nil}

Name:		sysc-shell
Version:	0.2.6
Release:	1
Summary:	Desktop shell for Niri, written in Go
License:	BSD-3-Clause
Group:		Window Manager/Bar
URL:		https://github.com/Nomadcxx/sysc-shell
Source0:	https://github.com/Nomadcxx/sysc-shell/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:	%{name}-%{version}-vendor.tar.xz
Source2:  config.example.json
Source3:  first-run.md
Source4:  niri-bindings.kdl

BuildRequires:	golang

Requires:	sysc-clipboard
Requires:	sysc-notify
Requires:	sysc-tray

Recommends:	sysc-lock
Recommends:	gslapper
Recommends:	wl-clipboard
Recommends:	wireplumber
Recommends:	networkmanager
Recommends:	bluez
Recommends:	matugen

%description
A desktop shell for Niri, written in Go. Bars, panels and OSDs, 
with separate daemons for notifications, clipboard history and the system tray.

%prep
%autosetup -p1
tar -xf %{S:1}

%build
go build -o %{name} ./cmd/%{name}/

%install
install -Dm755 %{name} %{buildroot}/usr/bin/%{name}
install -Dm644 packaging/systemd/sysc-shell.service %{buildroot}%{_userunitdir}/sysc-shell.service
sed -i 's|%h/.local/bin/|/usr/bin/|g' %{buildroot}%{_userunitdir}/sysc-shell.service
sed -i '/After=graphical-session.target/a Wants=sysc-notify.service sysc-tray.service sysc-clipboard.service sysc-lock-session.service\nAfter=sysc-notify.service sysc-tray.service sysc-clipboard.service sysc-lock-session.service' %{buildroot}%{_userunitdir}/sysc-shell.service
  # Seed only a missing user config; systemd runs these commands as the session user.
sed -i '/Type=simple/a ExecStartPre=/usr/bin/mkdir -p %E/sysc-shell\nExecStartPre=/usr/bin/cp --update=none /usr/share/doc/sysc-shell/config.example.json %E/sysc-shell/config.json' %{buildroot}%{_userunitdir}/sysc-shell.service

install -Dm644 README.md %{buildroot}%{_docdir}/%{name}/README.md
install -Dm644 LICENSE %{buildroot}%{_datadir}/licenses/%{name}/LICENSE

install -Dm644 %{_topdir}/config.example.json %{buildroot}%{_docdir}/%{name}/config.example.json
install -Dm644 %{_topdir}/first-run.md %{buildroot}%{_docdir}/%{name}/first-run.md
install -Dm644 %{_topdir}/niri-bindings.kdl %{buildroot}%{_docdir}/%{name}/niri-bindings.kdl

%post
%systemd_user_post sysc-shell.service

%preun
%systemd_user_preun sysc-shell.service

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_userunitdir}/%{name}.service
%{_docdir}/%{name}/config.example.json
%{_docdir}/%{name}/first-run.md
%{_docdir}/%{name}/niri-bindings.kdl
