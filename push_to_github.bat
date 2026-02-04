@echo off
chcp 65001 >nul
echo ========================================
echo   GitHub仓库上传助手
echo ========================================
echo.

:: 检查Git是否安装
git --version >nul 2>&1
if errorlevel 1 (
    echo [错误] Git未安装，请先安装Git: https://git-scm.com/download/win
    exit /b 1
)

:: 获取GitHub用户名
set /p GITHUB_USERNAME=请输入你的GitHub用户名: 

:: 获取仓库名（默认）
set REPO_NAME=chronic-disease-kb
echo.
echo 将创建仓库: %GITHUB_USERNAME%/%REPO_NAME%
echo.

:: 检查远程仓库是否已配置
git remote -v >nul 2>&1
if %errorlevel% == 0 (
    echo [信息] 远程仓库已配置，跳过添加...
) else (
    echo [步骤1/2] 添加远程仓库...
    git remote add origin https://github.com/%GITHUB_USERNAME%/%REPO_NAME%.git
    if errorlevel 1 (
        echo [警告] 添加远程仓库失败，可能已存在
    ) else (
        echo [成功] 远程仓库已添加
    )
)

echo.
echo [步骤2/2] 推送到GitHub...
echo 提示: 推送时会要求输入GitHub用户名和密码/令牌
echo.

:: 检查分支名
for /f "tokens=*" %%a in ('git branch --show-current') do set CURRENT_BRANCH=%%a
echo 当前分支: %CURRENT_BRANCH%

:: 推送
git push -u origin %CURRENT_BRANCH%
if errorlevel 1 (
    echo.
    echo [错误] 推送失败。可能的原因:
    echo 1. GitHub仓库不存在 - 请先在 https://github.com/new 创建仓库
    echo 2. 身份验证失败 - 请检查用户名和令牌
    echo 3. 网络连接问题
    echo.
    echo 请手动执行以下命令:
    echo git remote add origin https://github.com/%GITHUB_USERNAME%/%REPO_NAME%.git
    echo git push -u origin %CURRENT_BRANCH%
    exit /b 1
)

echo.
echo ========================================
echo [成功] 代码已推送到GitHub!
echo ========================================
echo.
echo 访问地址: https://github.com/%GITHUB_USERNAME%/%REPO_NAME%
echo.
pause