#!/usr/bin/env python3
"""
GitHub一键推送插件
智能检测、自动配置、一键推送
"""

import os
import sys
import subprocess
import json
import urllib.request
import urllib.error
import webbrowser
from pathlib import Path

class GitHubPushPlugin:
    def __init__(self):
        self.username = None
        self.repo_name = None
        self.token = None
        self.config_file = Path.home() / ".github_push_config.json"
        
    def load_config(self):
        """加载保存的配置"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.username = config.get('username')
                    self.token = config.get('token')
                    return True
            except:
                pass
        return False
    
    def save_config(self):
        """保存配置"""
        config = {
            'username': self.username,
            'token': self.token[:10] + '...' if self.token else None  # 只保存部分token用于识别
        }
        with open(self.config_file, 'w') as f:
            json.dump(config, f)
    
    def run_command(self, cmd, capture=True):
        """执行shell命令"""
        try:
            if capture:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                return result.returncode == 0, result.stdout, result.stderr
            else:
                return subprocess.run(cmd, shell=True).returncode == 0, "", ""
        except Exception as e:
            return False, "", str(e)
    
    def check_git_repo(self):
        """检查是否是git仓库"""
        success, stdout, _ = self.run_command("git rev-parse --git-dir")
        return success
    
    def get_git_info(self):
        """获取git信息"""
        # 获取当前分支
        success, branch, _ = self.run_command("git branch --show-current")
        branch = branch.strip() if success else "master"
        
        # 获取远程信息
        success, remotes, _ = self.run_command("git remote -v")
        has_origin = "origin" in remotes if success else False
        
        # 获取仓库名（从目录名）
        success, repo_path, _ = self.run_command("git rev-parse --show-toplevel")
        repo_name = Path(repo_path.strip()).name if success else "my-project"
        
        return branch, has_origin, repo_name
    
    def check_github_repo_exists(self, username, repo_name):
        """检查GitHub仓库是否存在"""
        try:
            url = f"https://api.github.com/repos/{username}/{repo_name}"
            req = urllib.request.Request(url)
            if self.token:
                req.add_header("Authorization", f"token {self.token}")
            
            with urllib.request.urlopen(req, timeout=5) as response:
                return response.status == 200
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return False
            return None  # 无法确定
        except:
            return None
    
    def setup_credentials(self):
        """设置凭证"""
        print("🔐 配置GitHub凭证")
        print("-" * 50)
        
        # 尝试加载已有配置
        if self.load_config():
            print(f"✓ 发现已保存的配置")
            print(f"  用户名: {self.username}")
            use_existing = input("  使用已有配置? [Y/n]: ").strip().lower()
            if use_existing in ['', 'y', 'yes']:
                return True
        
        # 输入用户名
        default_username = self.username or ""
        prompt = f"  GitHub用户名 [{default_username}]: " if default_username else "  GitHub用户名: "
        username = input(prompt).strip()
        self.username = username if username else default_username
        
        if not self.username:
            print("❌ 错误: 必须提供GitHub用户名")
            return False
        
        # 输入Token
        print("\n  需要GitHub Personal Access Token")
        print("  获取方式: https://github.com/settings/tokens")
        print("  权限要求: 勾选 'repo' 权限")
        
        has_token = input("  是否已准备好Token? [y/N]: ").strip().lower()
        if has_token in ['y', 'yes']:
            print("  (输入时不会显示)")
            import getpass
            self.token = getpass.getpass("  粘贴你的Token: ").strip()
        
        # 保存配置
        self.save_config()
        return True
    
    def create_repo_guide(self, repo_name):
        """引导创建仓库"""
        repo_url = f"https://github.com/new?name={repo_name}&description=AI-powered+project&visibility=public"
        
        print("\n" + "="*60)
        print("📦 需要在GitHub创建仓库")
        print("="*60)
        print(f"\n仓库名: {repo_name}")
        print(f"用户名: {self.username}")
        print(f"\n🔗 正在打开创建页面...")
        
        # 打开浏览器
        try:
            webbrowser.open(repo_url)
            print("✓ 浏览器已打开")
        except:
            print(f"\n请手动访问:")
            print(f"  {repo_url}")
        
        print("\n📋 创建步骤:")
        print("  1. 确认仓库名正确")
        print("  2. 不要勾选 'Add a README file'")
        print("  3. 不要勾选 'Add .gitignore'")
        print("  4. 点击 'Create repository'")
        
        input("\n按Enter键继续 (创建完成后)...")
        return True
    
    def push_to_github(self):
        """推送到GitHub"""
        print("\n" + "="*60)
        print("🚀 开始推送到GitHub")
        print("="*60)
        
        # 获取git信息
        branch, has_origin, repo_name = self.get_git_info()
        
        print(f"\n📁 本地信息:")
        print(f"  分支: {branch}")
        print(f"  仓库名: {repo_name}")
        
        # 检查远程配置
        if not has_origin:
            print(f"\n🔗 配置远程仓库...")
            remote_url = f"https://github.com/{self.username}/{repo_name}.git"
            success, _, error = self.run_command(f"git remote add origin {remote_url}")
            if not success:
                print(f"⚠️  添加远程仓库失败: {error}")
                return False
            print(f"✓ 远程仓库已配置")
        else:
            print(f"✓ 远程仓库已存在")
        
        # 检查GitHub仓库是否存在
        print(f"\n🔍 检查GitHub仓库...")
        exists = self.check_github_repo_exists(self.username, repo_name)
        
        if exists is False:
            print(f"  仓库不存在，需要创建")
            self.create_repo_guide(repo_name)
        elif exists is True:
            print(f"✓ GitHub仓库已存在")
        else:
            print(f"⚠️  无法确认仓库状态，将继续尝试推送")
        
        # 配置凭证缓存
        print(f"\n💾 配置凭证缓存...")
        self.run_command("git config --global credential.helper cache")
        
        # 推送
        print(f"\n⬆️  推送到GitHub...")
        print(f"  命令: git push -u origin {branch}")
        print(f"\n  如果提示输入密码，请粘贴你的Token\n")
        
        success = self.run_command(f"git push -u origin {branch}", capture=False)
        
        if success:
            print(f"\n✅ 推送成功!")
            print(f"\n🌐 访问你的仓库:")
            print(f"  https://github.com/{self.username}/{repo_name}")
            return True
        else:
            print(f"\n❌ 推送失败")
            print(f"\n常见原因:")
            print(f"  1. Token权限不足 (需要repo权限)")
            print(f"  2. 仓库不存在 (需先在GitHub创建)")
            print(f"  3. 网络连接问题")
            return False
    
    def run(self):
        """运行插件"""
        print("\n" + "="*60)
        print("🚀 GitHub一键推送插件 v1.0")
        print("="*60)
        
        # 检查git仓库
        if not self.check_git_repo():
            print("❌ 错误: 当前目录不是Git仓库")
            print("  请先运行: git init")
            return 1
        
        # 设置凭证
        if not self.setup_credentials():
            return 1
        
        # 推送
        if self.push_to_github():
            return 0
        else:
            return 1

if __name__ == "__main__":
    plugin = GitHubPushPlugin()
    sys.exit(plugin.run())
