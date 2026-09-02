# 许可与来源说明

本压缩包是多个独立来源的集合，不以一个许可证覆盖全部内容。

- 每个条目的仓库、固定提交、源路径、许可证和 payload 哈希见 `MANIFEST.json`；
- 上游根许可证/通知复制到 `licenses/<source-id>/`，安装时复制到对应包的 `UPSTREAM_NOTICES/`；
- Academic Research Skills 与其 Codex 适配器为 CC BY-NC 4.0，只能按许可证用于非商业场景；
- MIT、Apache-2.0 和各官方 Skill 的本地许可证仍分别适用；
- `NOASSERTION` 或只有 README 声称、缺少明确许可证文件的来源仅做 metadata-only 索引，不打包其 payload；
- 本仓库自有路由、模板和文档没有用第三方许可证重新授权上游内容；使用者仍需检查自己的用途、组织政策和司法辖区。

压缩包包含 Skill 指令和必要附件，不代表替用户安装第三方软件、获得 API 权限、数据库订阅、模型权重、数据许可或伦理批准。

来源固定信息来自仓库 `catalog/sources.lock.json`；构建时会核对实际 submodule HEAD。若固定提交不匹配，构建失败而不是静默领取最新版本。
