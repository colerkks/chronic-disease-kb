#!/bin/bash
# GitHub一键推送插件 (Linux/Mac版本)
# 用法: ./push-github.sh

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo ""
echo -e "${BLUE}============================================================${NC}"
echo -e "${BLUE}  🚀 GitHub一键推送插件 v1.0${NC}"
echo -e "${BLUE}============================================================${NC}"
echo ""

# 检查git
if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ 错误: 未找到Git${NC}"
    echo "   请安装Git: https://git-scm.com/downloads"
    exit 1
fi

# 检查是否是git仓库
if ! git rev-parse --git-dir &> /dev/null; then
    echo -e "${RED}❌ 错误: 当前目录不是Git仓库${NC}"
    echo "   请先运行: git init"
    exit 1
fi

# 获取信息
BRANCH=$(git branch --show-current)
REPO_PATH=$(git rev-parse --show-toplevel)
REPO_NAME=$(basename "$REPO_PATH")

echo -e "${GREEN}📁 本地仓库信息:${NC}"
echo "   分支: $BRANCH"
echo "   名称: $REPO_NAME"
echo ""

# 检查远程仓库
if git remote -v &> /dev/null; then
    REMOTE_URL=$(git remote get-url origin 2>/dev/null || echo "")
    if [ -n "$REMOTE_URL" ]; then
        echo -e "${GREEN}🔗 远程仓库:${NC} $REMOTE_URL"
    fi
fi

# 配置
echo ""
echo -e "${YELLOW}⚙️  配置${NC}"
echo ""

# 尝试读取保存的配置
CONFIG_FILE="$HOME/.github_push_config"
if [ -f "$CONFIG_FILE" ]; then
    echo -e "${GREEN}✓ 发现已保存的配置${NC}"
    SAVED_USER=$(head -1 "$CONFIG_FILE")
    echo "   用户名: $SAVED_USER"
    read -p "使用已有配置? [Y/n]: " use_saved
    if [[ $use_saved =~ ^[Yy]$ ]] || [ -z "$use_saved" ]; then
        GITHUB_USER="$SAVED_USER"
    else
        read -p "请输入GitHub用户名: " GITHUB_USER
    fi
else
    read -p "请输入GitHub用户名: " GITHUB_USER
fi

if [ -z "$GITHUB_USER" ]; then
    echo -e "${RED}❌ 错误: 用户名不能为空${NC}"
    exit 1
fi

# 保存配置
echo "$GITHUB_USER" > "$CONFIG_FILE"

# 配置远程仓库
echo ""
echo -e "${BLUE}🔗 配置远程仓库...${NC}"
if git remote add origin "https://github.com/$GITHUB_USER/$REPO_NAME.git" 2>/dev/null; then
    echo -e "${GREEN}✓ 远程仓库已添加${NC}"
else
    echo -e "${YELLOW}ℹ️ 远程仓库已存在${NC}"
fi

# 打开创建页面
echo ""
echo -e "${YELLOW}📦 准备推送${NC}"
echo "   仓库地址: https://github.com/$GITHUB_USER/$REPO_NAME"
echo ""
echo -e "${BLUE}🌐 正在打开GitHub创建页面...${NC}"
echo ""
echo -e "${YELLOW}请确认:${NC}"
echo "  1. 仓库名称为: $REPO_NAME"
echo "  2. 不要勾选 'Add a README file'"
echo "  3. 点击 'Create repository'"
echo ""

# 尝试打开浏览器
if command -v open &> /dev/null; then
    open "https://github.com/new?name=$REPO_NAME&description=AI-powered+project&visibility=public"
elif command -v xdg-open &> /dev/null; then
    xdg-open "https://github.com/new?name=$REPO_NAME&description=AI-powered+project&visibility=public"
else
    echo "请手动访问: https://github.com/new"
fi

read -p "按Enter键继续 (创建完成后)..."

# 配置凭证缓存
echo ""
echo -e "${BLUE}💾 配置凭证缓存...${NC}"
git config --global credential.helper cache
echo -e "${GREEN}✓ 凭证缓存已配置${NC}"

# 推送
echo ""
echo -e "${GREEN}⬆️  开始推送到GitHub...${NC}"
echo -e "${YELLOW}提示: 如果提示输入密码，请粘贴你的Token${NC}"
echo ""

if git push -u origin "$BRANCH"; then
    echo ""
    echo -e "${GREEN}============================================================${NC}"
    echo -e "${GREEN}✅ 推送成功!${NC}"
    echo -e "${GREEN}============================================================${NC}"
    echo ""
    echo -e "${BLUE}🌐 访问你的仓库:${NC}"
    echo "   https://github.com/$GITHUB_USER/$REPO_NAME"
    echo ""
else
    echo ""
    echo -e "${RED}============================================================${NC}"
    echo -e "${RED}❌ 推送失败${NC}"
    echo -e "${RED}============================================================${NC}"
    echo ""
    echo -e "${YELLOW}可能原因:${NC}"
    echo "  1. Token权限不足 (需要repo权限)"
    echo "  2. 仓库不存在 (需先在GitHub创建)"
    echo "  3. 网络连接问题"
    exit 1
fi