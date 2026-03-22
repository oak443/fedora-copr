# Gemini 3 生成
Name:           clash-verge-rev
Version:        2.4.7
Release:        1%{?dist}
Summary:        A modern GUI client based on Tauri, continuation of Clash Verge.
Group:          Applications/Internet
License:        GPLv3
URL:            https://github.com/clash-verge-rev/clash-verge-rev

# 直接使用官方构建好的 RPM 作为源码（针对 x86_64 架构）
Source0:        %{url}/releases/download/v%{version}/Clash.Verge-%{version}-1.x86_64.rpm

# 运行所需的依赖（根据 Tauri 应用通用的运行时依赖总结）
Requires:       webkit2gtk4.1
Requires:       libayatana-appindicator-gtk3
Requires:       openssl
Requires:       nss

# 告诉 RPM 构建器：我们只是在分发二进制，不需要生成调试包
%define debug_package %{nil}

%description
Clash Verge Rev is a modern GUI client based on Tauri, 
designed to provide a tailored proxy experience for Linux.

%prep
# 准备阶段：不需要常规的解压，因为我们后面直接处理 RPM
%setup -q -c -T

%build
# 构建阶段：留空，因为已经是二进制了

%install
# 安装阶段：将官方 RPM 的内容解压到构建目录中
mkdir -p %{buildroot}
rpm2cpio %{SOURCE0} | cpio -idmv -D %{buildroot}

# 修正权限（可选，确保二进制文件可执行）
chmod +x %{buildroot}%{_bindir}/clash-verge || :

%files
%{_bindir}/clash-verge*
%{_bindir}/verge-mihomo*
"/usr/lib/Clash Verge"
"/usr/share/applications/Clash Verge.desktop"
%{_datadir}/icons/hicolor/*/apps/clash-verge.png

%changelog
* Sat Mar 21 2026 Gemini - 2.4.7-1
- Update to version 2.4.7
