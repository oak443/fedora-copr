# Repackage the official upstream RPM; no compilation is required.
%global debug_package %{nil}

Name:           clash-verge-rev
Version:        2.5.10
Release:        1%{?dist}
Summary:        Modern Tauri-based GUI client for Clash/Mihomo

License:        GPL-3.0-only
URL:            https://github.com/clash-verge-rev/clash-verge-rev

ExclusiveArch:  aarch64 x86_64

# Official prebuilt RPMs, one per supported architecture.
Source0:        %{url}/releases/download/v%{version}/Clash.Verge-%{version}-1.aarch64.rpm
Source1:        %{url}/releases/download/v%{version}/Clash.Verge-%{version}-1.x86_64.rpm

Requires:       webkit2gtk4.1
Requires:       libayatana-appindicator-gtk3
Requires:       gtk3
Requires:       openssl
Requires:       nss

BuildRequires:  cpio

%description
Clash Verge Rev is a modern GUI client based on Tauri, designed to provide
a tailored proxy experience for Linux. This package repackages the official
upstream RPM without modification.

%prep
%setup -q -c -T

%build
# Nothing to build: the upstream RPM already contains the binaries.

%install
mkdir -p %{buildroot}
%ifarch aarch64
rpm2cpio %{SOURCE0} | cpio -idm -D %{buildroot}
%endif
%ifarch x86_64
rpm2cpio %{SOURCE1} | cpio -idm -D %{buildroot}
%endif

chmod 0755 %{buildroot}%{_bindir}/clash-verge

%files
%{_bindir}/clash-verge*
%{_bindir}/verge-mihomo*
# Build-time helper shipped by some upstream releases; not needed at runtime.
%exclude %{_bindir}/frontend-contract
# Upstream installs the application bundle into /usr/lib on every architecture.
"/usr/lib/Clash Verge"
"/usr/share/applications/Clash Verge.desktop"
%{_datadir}/icons/hicolor/*/apps/clash-verge.png

%check
test -x %{buildroot}%{_bindir}/clash-verge
test -d "%{buildroot}/usr/lib/Clash Verge"

%changelog
* Thu Nov 19 2026 oak443 <160876107+oak443@users.noreply.github.com> - 2.5.10-1
- Update to 2.5.10
- Clean up spec file and declare missing runtime/build dependencies

* Fri Apr 24 2026 Gemini - 2.4.7-2
- 添加 aarch64 架构支持

* Sat Mar 21 2026 Gemini - 2.4.7-1
- Update to version 2.4.7
