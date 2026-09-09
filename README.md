# Frontend Design Skills

前端设计技能集合，统一分类为 **design**，存放在 [`skills/design/`](skills/design/)。从各上游原样同步完整技能目录，保留配套文档、脚本及执行权限。

共 15 项：Taste 11 项、Emil Kowalski 2 项、Impeccable 1 项、Vercel 1 项。不包含 UI UX Pro Max 的 `brand`；保留 Taste 的 `brandkit`。

## 安装

先查看可用技能，再按需要安装（需要 Node.js / npx）：

```sh
npx skills add Yevanchen/frontend-design-skills --list
npx skills add Yevanchen/frontend-design-skills --skill web-design-guidelines --agent codex
```

安装全部到当前项目：

```sh
npx skills add Yevanchen/frontend-design-skills --skill '*' --agent codex -y
```

Claude Code 用户将 `--agent codex` 换成 `--agent claude-code`。安装全部不等于同时启用全部规则；按当前任务选技能。

## 技能目录

| 技能 | 用途 | 上游 |
| --- | --- | --- |
| [design-taste-frontend](skills/design/design-taste-frontend/SKILL.md) | 前端视觉方向与反模板化设计 | Taste |
| [design-taste-frontend-v1](skills/design/design-taste-frontend-v1/SKILL.md) | 上游保留的 v1 风格版本 | Taste |
| [gpt-taste](skills/design/gpt-taste/SKILL.md) | GPT 设计与动效指导 | Taste |
| [high-end-visual-design](skills/design/high-end-visual-design/SKILL.md) | 高端视觉风格预设 | Taste |
| [minimalist-ui](skills/design/minimalist-ui/SKILL.md) | 极简编辑式风格预设 | Taste |
| [redesign-existing-projects](skills/design/redesign-existing-projects/SKILL.md) | 现有界面改版 | Taste |
| [brandkit](skills/design/brandkit/SKILL.md) | 品牌视觉板与标志系统 | Taste |
| [image-to-code](skills/design/image-to-code/SKILL.md) | 图片驱动的界面实现 | Taste |
| [imagegen-frontend-web](skills/design/imagegen-frontend-web/SKILL.md) | Web 界面设计图生成 | Taste |
| [imagegen-frontend-mobile](skills/design/imagegen-frontend-mobile/SKILL.md) | 移动端界面设计图生成 | Taste |
| [full-output-enforcement](skills/design/full-output-enforcement/SKILL.md) | 完整输出约束 | Taste |
| [emil-design-eng](skills/design/emil-design-eng/SKILL.md) | 设计工程与克制的动效 | Emil |
| [find-animation-opportunities](skills/design/find-animation-opportunities/SKILL.md) | 识别值得添加动效的位置 | Emil |
| [impeccable](skills/design/impeccable/SKILL.md) | 设计、审查、打磨与可视化迭代 | Impeccable |
| [web-design-guidelines](skills/design/web-design-guidelines/SKILL.md) | Web 界面与可访问性代码审查 | Vercel |

风格预设可能冲突，例如嵌套卡片、圆角和胶囊按钮的要求。每个页面选定一种视觉方向，以用户需求和项目设计规范为准。

## 更新与验证

最新版指 [`sources.lock.json`](sources.lock.json) 中 `syncedAt` 时核对的上游默认分支 HEAD，不表示自动持续更新。`design-taste-frontend-v1` 是上游刻意保留的独立技能，仍同步该路径的最新内容。

```sh
# 需要 Python 3 和 Git；完整同步四个上游，替换受管技能目录及来源快照
python3 scripts/sync.py
# 离线验证文件内容、目录清单和执行权限
python3 scripts/sync.py --check
# 额外联网确认上游 HEAD 没有更新
python3 scripts/sync.py --check-upstream
# 检查安装工具可以识别这些技能
npx skills add . --list
```

更新后检查 `git diff` 再提交。回滚可使用 `git revert <同步提交>`；来源锁记录了每项的上游 commit、路径和逐文件 SHA-256。

Vercel 技能会在每次审查时获取它指定的最新 Web Interface Guidelines。Impeccable 上游的 launcher 首次使用可能下载其固定版本的运行程序。图像生成技能仍需要使用环境提供对应工具；安装本集合不会配置这些外部能力。

## 来源与许可

| 上游 | 许可 / 声明 |
| --- | --- |
| [leonxlnx/taste-skill](https://github.com/leonxlnx/taste-skill) | [MIT](third-party/leonxlnx--taste-skill/LICENSE) |
| [emilkowalski/skills](https://github.com/emilkowalski/skills) | [MIT](third-party/emilkowalski--skills/LICENSE) |
| [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | [Apache-2.0](third-party/pbakaus--impeccable/LICENSE) 与 [第三方声明](third-party/pbakaus--impeccable/NOTICE.md) |
| [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | 上游 [README 的 MIT 声明](third-party/vercel-labs--agent-skills/README.md#license) |

各技能归原作者所有，本仓库仅做分类、同步与分发。具体来源路径见 [`sources.json`](sources.json)。
