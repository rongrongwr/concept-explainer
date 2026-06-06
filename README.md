# concept-explainer

**概念解释 Skill** — 快速准确理解任何概念，输出结构化、易读的总结。

## 简介

当用户需要"搞懂"一个概念/知识点时使用。适用于医学知识、技术概念、科学原理、文化现象、专业术语等各种场景。

核心原则：**准确优先、清晰易懂、篇幅恰当、结构化输出**。

最终产出一份**排版精美的 PDF 报告**。

## 触发词

- 帮我了解XX、XX是什么、解释一下XX、搞懂XX
- XX是怎么回事、XX的原理、通俗易懂地解释XX
- 即使用户说"研究一下XX"，如果上下文显示只是想理解概念而非深度调研，也应触发

## 不适用场景

- 需要横纵分析的深度研究 → 用 [hv-analysis](https://github.com/KKKKhazix/khazix-skills/tree/main/hv-analysis)
- 公众号写作 → 用 [khazix-writer](https://github.com/KKKKhazix/khazix-skills/tree/main/khazix-writer)
- 简单的一句名词解释 → 直接回答即可

## 安装

在 Claude Code、Codex、OpenCode、OpenClaw 等支持 Skill 的 Agent 里，直接说：

```
帮我安装这个 skill：https://github.com/<your-username>/concept-explainer
```

## 跨平台兼容

本 Skill 遵循 [Agent Skills](https://agentskills.io) 开放标准，支持：

- Claude Code
- Codex
- OpenCode
- OpenClaw
- 其他支持 Agent Skills 标准的平台

## 目录结构

```
concept-explainer/
├── SKILL.md          # Skill 主文件
├── scripts/          # PDF 转换脚本
│   └── md_to_pdf.py
└── README.md         # 本文件
```

## 许可证

MIT License
