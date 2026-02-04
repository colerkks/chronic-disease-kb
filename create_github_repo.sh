#!/bin/bash
# GitHub Repository Setup Script
# Usage: ./create_github_repo.sh <username> <repo_name>

if [ $# -ne 2 ]; then
    echo "Usage: $0 <github_username> <repository_name>"
    echo "Example: $0 john_doe chronic-disease-kb"
    exit 1
fi

USERNAME=$1
REPO_NAME=$2

echo "Creating GitHub repository: $USERNAME/$REPO_NAME"
echo ""

# Check if git remote already exists
if git remote | grep -q "origin"; then
    echo "Remote 'origin' already exists. Updating..."
    git remote remove origin
fi

# Add GitHub remote
git remote add origin "https://github.com/$USERNAME/$REPO_NAME.git"

echo "Git remote configured:"
git remote -v

echo ""
echo "To complete the setup, you need to:"
echo "1. Create the repository on GitHub: https://github.com/new"
echo "   - Repository name: $REPO_NAME"
echo "   - Description: AI-powered chronic disease management knowledge base with intelligent agents"
echo "   - Make it Public or Private as you prefer"
echo ""
echo "2. After creating the repository, push your code:"
echo "   git push -u origin master"
echo ""
echo "Or if you have GitHub CLI installed:"
echo "   gh repo create $REPO_NAME --public --source=. --push"
echo ""