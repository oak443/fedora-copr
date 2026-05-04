# Claude Haiku 4.5 生成
Name:           n-m3u8dl-re
Version:        0.5.1
Release:        1%{?dist}
Summary:        跨平台的DASH/HLS/MSS下载工具。支持点播、直播(DASH/HLS)。
License:        MIT
URL:            https://github.com/nilaoda/N_m3u8DL-RE

# 支持这些架构
ExclusiveArch:  aarch64 x86_64

# 源码包：根据架构分别提供 ARM64 和 x86_64 的预构建二进制
Source0:        https://github.com/nilaoda/N_m3u8DL-RE/releases/download/v0.5.1-beta/N_m3u8DL-RE_v0.5.1-beta_linux-arm64_20251029.tar.gz
Source1:        https://github.com/nilaoda/N_m3u8DL-RE/releases/download/v0.5.1-beta/N_m3u8DL-RE_v0.5.1-beta_linux-x64_20251029.tar.gz

# 禁用调试包生成，因为我们只是分发预编译的二进制文件
%define debug_package %{nil}

%description
N_m3u8DL-RE 是一个跨平台的 DASH/HLS/MSS 下载工具。
支持点播和直播内容下载（DASH/HLS 协议）。
这个工具提供了命令行界面用于媒体流下载。

# 准备阶段：解压源码包
%prep
# 仅为当前架构解压相应的源码包
%ifarch aarch64
%setup -q -c -n n-m3u8dl-re
tar -xzf %{SOURCE0}
%endif
%ifarch x86_64
%setup -q -c -n n-m3u8dl-re
tar -xzf %{SOURCE1}
%endif

# 构建阶段：预编译二进制无需构建
%build
# 无需构建步骤，源码包中已包含可执行文件

# 安装阶段：将二进制文件复制到目标位置
%install
# 创建二进制文件的目标目录
mkdir -p %{buildroot}%{_bindir}

# 复制二进制文件到 /usr/bin 目录
cp N_m3u8DL-RE %{buildroot}%{_bindir}/N_m3u8DL-RE

# 确保二进制文件具有正确的可执行权限
chmod +x %{buildroot}%{_bindir}/N_m3u8DL-RE

# 创建小写别名的符号链接，方便用户使用
ln -s N_m3u8DL-RE %{buildroot}%{_bindir}/n-m3u8dl-re

# 文件列表：指定打包进 RPM 的文件
%files
# 命令行工具的可执行文件位于 /usr/bin
%{_bindir}/N_m3u8DL-RE
# 小写名称的符号链接，作为便利的别名
%{_bindir}/n-m3u8dl-re

# 检查阶段：验证安装的文件
%check
# 验证二进制文件存在且可执行
test -x %{buildroot}%{_bindir}/N_m3u8DL-RE
# 验证小写的符号链接存在
test -L %{buildroot}%{_bindir}/n-m3u8dl-re

# 变更日志：记录版本更新历史
%changelog
* Mon May 5 2026 Packager <packager@example.com> - 0.5.1-1
- 初始 RPM 打包，支持 aarch64 和 x86_64 架构
- 包含 N_m3u8DL-RE v0.5.1-beta 版本

* Sat Oct 29 2025 Packager <packager@example.com> - 0.5.1-beta
- DASH/HLS/MSS 下载工具初始发布

