@echo off
chcp 65001 >nul
title GitHub一键推送插件 v1.0

:: 颜色设置
set "GREEN=[92m"
set "YELLOW=[93m"
set "RED=[91m"
set "BLUE=[94m"
set "RESET=[0m"

echo.
echo %BLUE%============================================================%RESET%
echo %BLUE%  🚀 GitHub一键推送插件 v1.0%RESET%
echo %BLUE%============================================================%RESET%
echo.

:: 检查git
where git >nul 2>nul
if %errorlevel% neq 0 (
    echo %RED%❌ 错误: 未找到Git%RESET%
    echo    请安装Git: https://git-scm.com/download/win
    pause
    exit /b 1
)

:: 检查是否是git仓库
git rev-parse --git-dir >nul 2>nul
if %errorlevel% neq 0 (
    echo %RED%❌ 错误: 当前目录不是Git仓库%RESET%
    echo    请先运行: git init
    pause
    exit /b 1
)

:: 获取信息
for /f "tokens=*" %%a in ('git branch --show-current') do set "BRANCH=%%a"
for /f "tokens=*" %%a in ('git rev-parse --show-toplevel') do set "REPO_PATH=%%a"
for %%i in ("%REPO_PATH%") do set "REPO_NAME=%%~ni"

echo %GREEN%📁 本地仓库信息:%RESET%
echo    分支: %BRANCH%
echo    名称: %REPO_NAME%
echo.

:: 检查远程仓库
git remote -v >nul 2>nul
if %errorlevel% equ 0 (
    for /f "tokens=2" %%a in ('git remote get-url origin 2^>nul') do (
        echo %GREEN%🔗 远程仓库:%RESET% %%a
        goto :HAS_REMOTE
    )
)

:: 配置用户名
echo %YELLOW%⚙️  首次配置%RESET%
echo.

:: 尝试读取保存的配置
if exist "%USERPROFILE%\.github_push_config.txt" (
    echo %GREEN%✓ 发现已保存的配置%RESET%
    for /f "tokens=1,2" %%a in (%USERPROFILE%\.github_push_config.txt) do (
        set "SAVED_USER=%%a"
        set "SAVED_REPO=%%b"
    )
    echo    用户名: %SAVED_USER%
    choice /c YN /n /m "使用已有配置? [Y/n]: "
    if !errorlevel! equ 1 (
        set "GITHUB_USER=%SAVED_USER%"
        goto :CONFIG_DONE
    )
)

set /p "GITHUB_USER=请输入GitHub用户名: "
if "%GITHUB_USER%"=="" (
    echo %RED%❌ 用户名不能为空%RESET%
    pause
    exit /b 1
)

:: 保存配置
echo %GITHUB_USER% %REPO_NAME% > "%USERPROFILE%\.github_push_config.txt"

:CONFIG_DONE
echo.

:: 配置远程仓库
echo %BLUE%🔗 配置远程仓库...%RESET%
git remote add origin https://github.com/%GITHUB_USER%/%REPO_NAME%.git >nul 2>nul
if %errorlevel% equ 0 (
    echo %GREEN%✓ 远程仓库已添加%RESET%
) else (
    echo %YELLOW%ℹ️ 远程仓库已存在%RESET%
)

:: 打开创建页面
echo.
echo %YELLOW%📦 准备推送%RESET%
echo    仓库地址: https://github.com/%GITHUB_USER%/%REPO_NAME%
echo.
echo %BLUE%🌐 正在打开GitHub创建页面...%RESET%
echo.
echo %YELLOW%请确认:%RESET%
echo   1. 仓库名称为: %REPO_NAME%
echo   2. 不要勾选 "Add a README file"
echo   3. 点击 "Create repository"
echo.

start https://github.com/new?name=%REPO_NAME%^&description=AI-powered+project^&visibility=public

:HAS_REMOTE
echo.
echo %BLUE%💾 配置凭证缓存...%RESET%
git config --global credential.helper cache
echo %GREEN%✓ 凭证缓存已配置%RESET%

echo.
echo %GREEN%⬆️  开始推送到GitHub...%RESET%
echo %YELLOW%提示: 如果提示输入密码，请粘贴你的Token%RESET%
echo.

git push -u origin %BRANCH%

if %errorlevel% equ 0 (
    echo.
    echo %GREEN%============================================================%RESET%
    echo %GREEN%✅ 推送成功!%RESET%
    echo %GREEN%============================================================%RESET%
    echo.
    echo %BLUE%🌐 访问你的仓库:%RESET%
    echo    https://github.com/%GITHUB_USER%/%REPO_NAME%
    echo.
    start https://github.com/%GITHUB_USER%/%REPO_NAME%
) else (
    echo.
    echo %RED%============================================================%RESET%
    echo %RED%❌ 推送失败%RESET%
    echo %RED%============================================================%RESET%
    echo.
    echo %YELLOW%可能原因:%RESET%
    echo   1. Token权限不足 ^(需要repo权限^)
    echo   2. 仓库不存在 ^(需先在GitHub创建^)
    echo   3. 网络连接问题
    echo.
    echo %BLUE%解决步骤:%RESET%
    echo   1. 访问 https://github.com/new 创建仓库
    echo   2. 仓库名称必须 exactly 为: %REPO_NAME%
    echo   3. 重新运行此脚本
)

echo.
pause