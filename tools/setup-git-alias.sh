#!/bin/bash
# Git别名一键推送配置
# 运行此脚本设置git别名: ./setup-git-alias.sh

echo "🔧 配置Git别名..."

# 添加别名到git配置
git config --global alias.push-github '!bash -c '"'"'
REPO_NAME=$(basename "$(git rev-parse --show-toplevel)")
BRANCH=$(git branch --show-current)
echo "🚀 推送到GitHub..."
echo "   仓库: $REPO_NAME"
echo "   分支: $BRANCH"
git push -u origin "$BRANCH"
'"'"''

git config --global alias.push-gh '!git push-github'

echo "✅ 配置完成!"
echo ""
echo "使用方法:"
echo "  git push-github    # 完整命令"
echo "  git push-gh        # 简写命令"
echo ""
echo "这些别名会推送当前分支到origin"