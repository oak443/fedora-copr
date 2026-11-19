# fedora-copr

[![Validate Specs](https://github.com/oak443/fedora-copr/actions/workflows/validate.yml/badge.svg)](https://github.com/oak443/fedora-copr/actions/workflows/validate.yml)

个人维护的 [Fedora COPR](https://copr.fedorainfracloud.org/coprs/oak443/) 打包仓库。仓库中的 spec 文件直接重新打包上游发布的预编译产物，不在 COPR 中编译源码。

## 软件包

| 软件包 | 上游项目 | 说明 |
| --- | --- | --- |
| [clash-verge-rev](clash-verge-rev/clash-verge-rev.spec) | [clash-verge-rev/clash-verge-rev](https://github.com/clash-verge-rev/clash-verge-rev) | 基于 Tauri 的 Clash/Mihomo GUI 客户端 |
| [n-m3u8dl-re](n-m3u8dl-re/n-m3u8dl-re.spec) | [nilaoda/N_m3u8DL-RE](https://github.com/nilaoda/N_m3u8DL-RE) | DASH/HLS/MSS 流媒体下载工具 |

两个包均只支持 `x86_64` 和 `aarch64`。

## 安装

```bash
# Clash Verge Rev
sudo dnf copr enable oak443/clash-verge-rev
sudo dnf install clash-verge-rev

# N_m3u8DL-RE
sudo dnf copr enable oak443/n-m3u8dl-re
sudo dnf install n-m3u8dl-re
```

## 仓库结构

```text
.
├── .github/
│   ├── scripts/
│   │   └── update_spec.py       # 根据上游 release 更新 spec
│   └── workflows/
│       ├── auto_update.yml      # 每日检查上游新版本
│       └── validate.yml         # push / PR 时校验 spec
├── clash-verge-rev/
│   └── clash-verge-rev.spec
└── n-m3u8dl-re/
    └── n-m3u8dl-re.spec
```

COPR 中的两个项目都配置为从本仓库的 SCM 构建，子目录分别为 `clash-verge-rev` 和 `n-m3u8dl-re`。

- `clash-verge-rev` 已在 GitHub 仓库中配置 webhook，推送该子目录下的变更会自动触发构建。
- `n-m3u8dl-re` 还需要在 COPR 项目页面的 **Settings → Integrations** 中复制 GitHub webhook URL，然后添加到本仓库的 **Settings → Webhooks**（Content type 选 `application/json`，事件选 push）。配置完成前，请在 COPR 页面手动触发构建。

webhook 只会对该子目录内文件发生变更的 push 触发重建，修改 README 等仓库根目录文件不会触发。

## 自动更新

[`auto_update.yml`](.github/workflows/auto_update.yml) 每天 12:00 UTC 运行一次，也可以从 Actions 页面手动触发：

1. 通过 `gh api`（使用 `GITHUB_TOKEN`）获取上游最新 release，避免匿名 API 限流；
2. 更新 spec 中的 `Version`、`Release`、上游 tag / 构建日期宏（如需要）；
3. 在 `%changelog` 顶部插入对应版本的记录；
4. 有变动时自动提交并推送；若对应的 COPR 项目已配置 webhook，COPR 会继续触发重建。

更新逻辑集中在 [`update_spec.py`](.github/scripts/update_spec.py)，新增软件包时只需在 workflow 中增加一次调用。

## 本地校验

需要 `rpm-build`：

```bash
sudo dnf install rpm-build

for spec in */*.spec; do
    rpmspec -P "$spec" > /dev/null && echo "OK: $spec"
done
```

## 说明

- 这些是个人维护的非官方软件包，与 Fedora 项目及上游开发者无关。
- 打包内容来自上游发布的 RPM 或静态二进制，许可证遵循各自上游项目（GPL-3.0-only / MIT）。
- 上游更新后，版本号和下载地址由 CI 自动维护；如遇上游产物命名变化，CI 会保留旧版本并等待手动修正。
