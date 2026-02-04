# GitHub一键推送插件使用说明

## 🚀 快速开始

### 方法1: Python脚本 (跨平台，推荐)

```bash
# Windows/Linux/Mac 通用
python tools/github-push.py
```

**功能：**
- ✅ 自动检测Git仓库
- ✅ 智能配置管理（保存用户名）
- ✅ 自动打开GitHub创建页面
- ✅ 一键完成推送

---

### 方法2: Windows批处理

```bash
# 双击运行
tools\push-github.bat
```

或命令行：
```cmd
tools\push-github.bat
```

**功能：**
- ✅ 图形化界面提示
- ✅ 自动保存配置
- ✅ 颜色输出，清晰易读

---

### 方法3: Linux/Mac Bash脚本

```bash
# 添加执行权限
chmod +x tools/push-github.sh

# 运行
./tools/push-github.sh
```

---

### 方法4: Git别名 (最快捷)

```bash
# 配置别名
./tools/setup-git-alias.sh

# 以后直接运行
git push-github
# 或简写
git push-gh
```

---

## 📋 首次使用步骤

### 1. 准备GitHub Token

1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 勾选 `repo` 权限
4. 生成并复制Token

### 2. 运行插件

选择上面任意一种方法运行，按提示操作：

```
🚀 GitHub一键推送插件 v1.0
============================================================

📁 本地仓库信息:
   分支: master
   名称: my-project

⚙️  首次配置
请输入GitHub用户名: colerkks

🔗 配置远程仓库...
✓ 远程仓库已添加

📦 准备推送
   仓库地址: https://github.com/colerkks/my-project

🌐 正在打开GitHub创建页面...

[浏览器自动打开，创建仓库后按Enter]

⬆️  开始推送到GitHub...
提示: 如果提示输入密码，请粘贴你的Token

[输入Token后自动推送]

✅ 推送成功!
🌐 访问你的仓库:
   https://github.com/colerkks/my-project
```

---

## 🔧 添加到系统PATH（可选）

### Windows

1. 将 `tools` 目录添加到系统PATH
2. 以后可以在任意位置运行：
   ```cmd
   push-github.bat
   ```

### Linux/Mac

1. 创建符号链接：
   ```bash
   sudo ln -s $(pwd)/tools/push-github.sh /usr/local/bin/push-github
   ```
2. 以后可以直接运行：
   ```bash
   push-github
   ```

---

## 📝 配置文件

插件会自动保存配置到：

- **Windows**: `%USERPROFILE%\.github_push_config.txt`
- **Linux/Mac**: `~/.github_push_config`

包含：GitHub用户名、仓库名

---

## 🎯 使用场景

| 场景 | 推荐方法 | 命令 |
|------|---------|------|
| 第一次推送 | Python脚本 | `python tools/github-push.py` |
| 日常推送 | Git别名 | `git push-github` |
| Windows用户 | 批处理 | `push-github.bat` |
| Linux/Mac用户 | Bash脚本 | `./push-github.sh` |

---

## ❗ 常见问题

### Q: 提示 "Repository not found"
**A:** 需要先在GitHub创建仓库。插件会自动打开创建页面，你只需要点击创建即可。

### Q: 提示 "Permission denied"
**A:** Token权限不足，需要勾选 `repo` 权限重新生成Token。

### Q: 不想每次都输入Token
**A:** 使用 `git config --global credential.helper cache` 缓存凭证（默认15分钟）。

### Q: 如何修改已保存的用户名？
**A:** 删除配置文件后重新运行：
- Windows: `del %USERPROFILE%\.github_push_config.txt`
- Linux/Mac: `rm ~/.github_push_config`

---

## 🎉 一键推送，就是这么简单！

选择你喜欢的方法，以后推送到GitHub只需要一个命令！🚀