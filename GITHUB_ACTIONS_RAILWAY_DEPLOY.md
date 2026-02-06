# 🚀 GitHub Actions 部署到 Railway 详细指南

本指南将详细说明如何使用 GitHub Actions 自动部署到 Railway。

## 📋 前置要求

- ✅ GitHub 仓库已创建（`Hui-Hu-2025/RAG_DEMO`）
- ✅ Railway 账户已注册
- ✅ 代码已推送到 GitHub

## 🔑 第一步：获取 Railway Token

### 1.1 登录 Railway

1. 访问 https://railway.app
2. 使用 GitHub 账户登录

### 1.2 创建 API Token

1. 点击右上角头像 → **"Account Settings"**
2. 在左侧菜单找到 **"Tokens"** 或 **"API Tokens"**
3. 点击 **"New Token"** 或 **"Create Token"**
4. 输入 Token 名称（例如：`github-actions-deploy`）
5. 选择权限：
   - ✅ **Full Access**（推荐，用于部署）
   - 或根据需要选择特定权限
6. 点击 **"Create Token"**
7. **重要**：复制 Token 并保存（只显示一次！）
   - Token 格式类似：`railway_xxxxxxxxxxxxxxxxxxxxx`

## 🔐 第二步：配置 GitHub Secrets

### 2.1 打开 GitHub 仓库设置

1. 访问你的 GitHub 仓库：https://github.com/Hui-Hu-2025/RAG_DEMO
2. 点击 **"Settings"** 标签页
3. 在左侧菜单找到 **"Secrets and variables"** → **"Actions"**

### 2.2 添加 Railway Token

1. 点击 **"New repository secret"**
2. 输入 Secret 名称：`RAILWAY_TOKEN`
3. 输入 Secret 值：粘贴刚才复制的 Railway Token
4. 点击 **"Add secret"**

### 2.3 添加 Railway Project ID（可选，但推荐）

如果需要部署到特定项目：

1. 在 Railway Dashboard，进入你的项目
2. 点击项目 **"Settings"**
3. 找到 **"Project ID"**（格式类似：`xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`）
4. 在 GitHub Secrets 中添加：
   - Name: `RAILWAY_PROJECT_ID`
   - Value: 项目 ID

## 📝 第三步：创建 GitHub Actions Workflow

### 3.1 检查现有 Workflow

检查是否已有 workflow 文件：

```powershell
# 在项目根目录执行
Test-Path .github\workflows\deploy.yml
```

### 3.2 创建或更新 Workflow 文件

如果文件不存在，创建 `.github/workflows/deploy.yml`：

```yaml
name: Deploy to Railway

on:
  push:
    branches:
      - main
      - master
  workflow_dispatch:  # 允许手动触发

env:
  RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}

jobs:
  test:
    name: Run Tests
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install backend dependencies
        run: |
          cd backend
          pip install -r requirements.txt

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json

      - name: Install frontend dependencies
        run: |
          cd frontend
          npm ci

      - name: Build frontend
        run: |
          cd frontend
          npm run build

  deploy-backend:
    name: Deploy Backend to Railway
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main' || github.ref == 'refs/heads/master'
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Install Railway CLI
        run: npm install -g @railway/cli

      - name: Deploy Backend
        run: |
          railway link --service backend || railway service
          railway up --service backend
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
          RAILWAY_PROJECT_ID: ${{ secrets.RAILWAY_PROJECT_ID }}

  deploy-frontend:
    name: Deploy Frontend to Railway
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main' || github.ref == 'refs/heads/master'
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Install Railway CLI
        run: npm install -g @railway/cli

      - name: Deploy Frontend
        run: |
          railway link --service frontend || railway service
          railway up --service frontend
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
          RAILWAY_PROJECT_ID: ${{ secrets.RAILWAY_PROJECT_ID }}
```

### 3.3 使用 Railway GitHub Integration（推荐方式）

实际上，Railway 更推荐使用 GitHub Integration 而不是 CLI。更新 workflow：

```yaml
name: Deploy to Railway

on:
  push:
    branches:
      - main
      - master
  workflow_dispatch:

jobs:
  test:
    name: Run Tests
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install backend dependencies
        run: |
          cd backend
          pip install -r requirements.txt

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json

      - name: Install frontend dependencies
        run: |
          cd frontend
          npm ci

      - name: Build frontend
        run: |
          cd frontend
          npm run build

  # 注意：Railway 的 GitHub Integration 会自动部署
  # 这个 workflow 主要用于测试
  # 实际部署由 Railway 的自动部署功能处理
```

## 🔗 第四步：配置 Railway GitHub Integration

### 4.1 在 Railway 中连接 GitHub

1. 登录 Railway：https://railway.app
2. 在现有项目中，点击 **"+ New"** → **"GitHub Repo"**
3. 选择仓库：`Hui-Hu-2025/RAG_DEMO`
4. Railway 会自动：
   - 检测代码变更
   - 自动部署到对应服务

### 4.2 配置自动部署

1. 在 Railway 服务页面，点击 **"Settings"**
2. 找到 **"Deploy"** 或 **"Auto Deploy"** 设置
3. 确保以下选项已启用：
   - ✅ **"Auto Deploy"** - 自动部署
   - ✅ **"Deploy on Push"** - 推送时部署
   - 选择分支：`main` 或 `master`

### 4.3 配置服务设置

**后端服务：**
- Root Directory: `backend`
- Build Command: （自动检测）
- Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

**前端服务：**
- Root Directory: `frontend`
- Build Command: `npm install && npm run build`
- Start Command: `npm run preview -- --host 0.0.0.0 --port $PORT`

## 🚀 第五步：触发部署

### 5.1 自动部署（推荐）

1. 推送代码到 `main` 或 `master` 分支：
   ```powershell
   git add .
   git commit -m "Update code"
   git push origin main
   ```

2. Railway 会自动检测并开始部署

3. 在 Railway Dashboard 查看部署状态

### 5.2 手动触发 GitHub Actions

1. 访问 GitHub 仓库
2. 点击 **"Actions"** 标签页
3. 选择 **"Deploy to Railway"** workflow
4. 点击 **"Run workflow"**
5. 选择分支，点击 **"Run workflow"**

## 📊 第六步：监控部署

### 6.1 在 Railway 中查看

1. 登录 Railway Dashboard
2. 进入项目
3. 点击服务查看：
   - **Deploy** 标签页 - 部署历史和状态
   - **Logs** 标签页 - 实时日志
   - **Metrics** 标签页 - 资源使用情况

### 6.2 在 GitHub Actions 中查看

1. 访问 GitHub 仓库
2. 点击 **"Actions"** 标签页
3. 查看 workflow 运行状态
4. 点击运行查看详细日志

## 🔧 故障排除

### 问题 1: Railway Token 无效

**症状**: GitHub Actions 报错 `RAILWAY_TOKEN` 无效

**解决**:
1. 检查 GitHub Secrets 中的 `RAILWAY_TOKEN` 是否正确
2. 在 Railway 中重新生成 Token
3. 更新 GitHub Secrets

### 问题 2: 部署失败

**症状**: Railway 部署失败

**检查**:
1. 查看 Railway 日志（Logs 标签页）
2. 检查环境变量是否正确设置
3. 确认 Root Directory 设置正确
4. 检查构建命令是否正确

### 问题 3: GitHub Actions 测试失败

**症状**: 测试阶段失败

**解决**:
1. 查看 GitHub Actions 日志
2. 检查 `requirements.txt` 和 `package.json` 是否正确
3. 确认 Python 和 Node.js 版本兼容

### 问题 4: 服务无法启动

**症状**: 部署成功但服务无法启动

**检查**:
1. 查看 Railway Logs
2. 检查 Start Command 是否正确
3. 确认环境变量已设置
4. 检查端口配置（Railway 使用 `$PORT`）

## 💡 最佳实践

### 1. 使用分支保护

在 GitHub 仓库设置中：
- 启用分支保护规则
- 要求通过测试后才能合并
- 防止直接推送到 main 分支

### 2. 环境变量管理

- 敏感信息（API Key）只存储在 Railway Variables
- 不要提交 `.env` 文件到 Git
- 使用 GitHub Secrets 存储 Railway Token

### 3. 部署策略

- 使用 `main` 分支自动部署到生产环境
- 使用 `develop` 分支部署到测试环境
- 使用 GitHub Actions 进行测试和验证

### 4. 监控和日志

- 定期查看 Railway Logs
- 设置告警（如果 Railway 支持）
- 监控资源使用情况

## 📚 相关资源

- [Railway 文档](https://docs.railway.app)
- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [Railway CLI 文档](https://docs.railway.app/develop/cli)

## ✅ 检查清单

- [ ] Railway Token 已创建并添加到 GitHub Secrets
- [ ] Railway Project ID 已添加（可选）
- [ ] GitHub Actions workflow 文件已创建
- [ ] Railway 服务已配置（Root Directory、Build Command、Start Command）
- [ ] 环境变量已在 Railway 中设置
- [ ] 自动部署已启用
- [ ] 测试推送代码触发部署
- [ ] 部署成功并验证功能

---

**完成以上步骤后，每次推送代码到 main/master 分支，Railway 会自动部署！** 🎉
