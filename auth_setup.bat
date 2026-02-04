@echo off
echo Setting up authentication for oh-my-opencode...
echo.
echo Please run the following commands manually in your terminal:
echo.
echo 1. First, add OpenCode to PATH:
echo    export PATH=/c/Users/rkkco/.opencode/bin:$PATH
echo.
echo 2. Then authenticate with OpenAI:
echo    opencode auth login
echo    - Select "OpenAI" 
echo    - Choose "ChatGPT Plus/Pro" login method
echo    - Complete browser authentication
echo.
echo 3. Then authenticate with Google:
echo    opencode auth login
echo    - Select "Google"
echo    - Choose "OAuth with Google (Antigravity)"
echo    - Complete browser authentication
echo.
echo After completing both authentications, you can start using:
echo    opencode
echo.
echo Use "ultrawork" or "ulw" in your prompts for the best experience!
pause