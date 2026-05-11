<#
.SYNOPSIS
    Token Usage Tracker - 推送到 GitHub 脚本
.DESCRIPTION
    自动创建 GitHub 仓库并推送代码
.NOTES
    需要先安装 gh CLI 并登录: gh auth login
#>

$ErrorActionPreference = "Stop"

$repoName = "token-usage-tracker"
$description = "AI平台余额追踪器 (AI Platform Balance Tracker)"
$projectDir = Split-Path -Parent $PSScriptRoot

Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host " Token Usage Tracker - Pushing to GitHub" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan

# 切换到项目目录
Set-Location $projectDir

# 检查 gh 是否已登录
try {
    $ghStatus = gh auth status 2>&1
    Write-Host "[OK] GitHub CLI is authenticated" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] GitHub CLI is not authenticated. Run 'gh auth login' first." -ForegroundColor Red
    exit 1
}

# 检查是否已有 Git 仓库
if (-not (Test-Path ".git")) {
    Write-Host "[INFO] Initializing Git repository..." -ForegroundColor Yellow
    git init
    git add .
    git commit -m "Initial commit: Token Usage Tracker"
}

# 检查是否已有远程仓库
$remoteExists = git remote -v 2>&1 | Select-String "origin"
if (-not $remoteExists) {
    Write-Host "[INFO] Creating GitHub repository..." -ForegroundColor Yellow
    gh repo create "tobiglevent001/$repoName" --public --description $description --push --source .
} else {
    Write-Host "[INFO] Remote exists, pushing changes..." -ForegroundColor Yellow
    git push -u origin master
}

Write-Host ""
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host " Done! Repository: https://github.com/tobiglevent001/$repoName" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Cyan
