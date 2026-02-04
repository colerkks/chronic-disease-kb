# 项目结构说明

## 目录组织

本项目采用分离式结构，将项目代码与系统插件分开管理。

### 1. 项目目录
**路径**: `C:\Users\rkkco\Desktop\配置\chronic-disease-kb\`

包含所有项目相关的代码、文档和配置文件：

```
chronic-disease-kb/
├── agents/          # 代理模块
├── api/             # API接口
├── core/            # 核心功能
├── data/            # 数据文件
├── db/              # 数据库相关
├── kb/              # 知识库
├── models/          # 数据模型
├── scripts/         # 脚本文件
├── tests/           # 测试文件
├── docs/            # 项目文档
├── config.py        # 配置文件
├── requirements.txt # 依赖列表
├── .env.example     # 环境变量示例
└── README.md        # 项目说明
```

### 2. 系统插件
**路径**: `C:\Users\rkkco\.opencode\plugins\github-push\`

包含 GitHub 推送插件（已安装到系统目录）：

```
github-push/
├── github-push.py   # 主插件脚本
├── github-push.bat  # Windows 批处理
├── plugin.json      # 插件配置
├── install.sh       # Linux/Mac 安装脚本
├── install.bat      # Windows 安装脚本
└── README.md        # 插件说明
```

## 迁移说明

- 原项目中的 `tools/` 目录已移除，相关内容已迁移到系统插件目录
- GitHub 推送功能通过系统插件 `github-push` 提供
- 使用方式：`opencode github-push` 或 `opencode ghp`

## 使用建议

1. **开发时**: 在 `chronic-disease-kb/` 目录下进行项目开发
2. **推送代码**: 使用系统插件命令 `opencode github-push`
3. **保持同步**: 定期从系统插件目录更新工具

---
创建时间: 2025-02-04
