# Repackage the official prebuilt binaries; no compilation is required.
%global debug_package %{nil}
# Upstream tags are "v<version>-beta" while RPM versions cannot contain "-".
%global upstream_tag %{version}-beta
# Date suffix used by the upstream release asset names; updated by CI.
%global build_date 20260629

Name:           n-m3u8dl-re
Version:        0.6.0
Release:        1%{?dist}
Summary:        Cross-platform DASH/HLS/MSS downloader with live stream support

License:        MIT
URL:            https://github.com/nilaoda/N_m3u8DL-RE

ExclusiveArch:  aarch64 x86_64

Source0:        %{url}/releases/download/v%{upstream_tag}/N_m3u8DL-RE_v%{upstream_tag}_linux-arm64_%{build_date}.tar.gz
Source1:        %{url}/releases/download/v%{upstream_tag}/N_m3u8DL-RE_v%{upstream_tag}_linux-x64_%{build_date}.tar.gz

%description
N_m3u8DL-RE is a cross-platform downloader for DASH, HLS and MSS streams.
It supports both video-on-demand and live content and provides a command-line
interface for media stream downloads.

%prep
%setup -q -c -T
%ifarch aarch64
tar -xzf %{SOURCE0}
%endif
%ifarch x86_64
tar -xzf %{SOURCE1}
%endif

%build
# Nothing to build: the release tarballs contain static binaries.

%install
install -Dpm 0755 N_m3u8DL-RE %{buildroot}%{_bindir}/N_m3u8DL-RE
ln -s N_m3u8DL-RE %{buildroot}%{_bindir}/n-m3u8dl-re

%files
%{_bindir}/N_m3u8DL-RE
%{_bindir}/n-m3u8dl-re

%check
test -x %{buildroot}%{_bindir}/N_m3u8DL-RE
test -L %{buildroot}%{_bindir}/n-m3u8dl-re

%changelog
* Thu Nov 19 2026 oak443 <160876107+oak443@users.noreply.github.com> - 0.6.0-1
- Update to 0.6.0-beta
- Clean up spec file and make the source URLs updateable by CI

* Tue May 05 2026 Packager <packager@example.com> - 0.5.1-1
- 初始 RPM 打包，支持 aarch64 和 x86_64 架构
- 包含 N_m3u8DL-RE v0.5.1-beta 版本

* Wed Oct 29 2025 Packager <packager@example.com> - 0.5.1-beta
- DASH/HLS/MSS 下载工具初始发布
