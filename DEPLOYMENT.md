# 部署指南 - GitHub Actions → Railway

本指南将帮助你使用 GitHub Actions 和 Railway 部署这个 RAG 应用。

## 📋 前置要求

1. **GitHub 账户** - 用于代码仓库和 GitHub Actions
2. **Railway 账户** - 注册地址：https://railway.app
3. **OpenAI API Key** - 用于 LLM 服务

## 🚀 部署步骤

### 步骤 1: 准备代码仓库

1. **在项目根目录**（`rag_demo` 目录）中执行以下命令，将代码推送到 GitHub 仓库：
   
   ```bash
   # 确保你在项目根目录
   cd C:\Users\huihu\Desktop\SDM2020\wk2_RAG-feature-test\wk2_RAG-feature-test\rag_demo
   
   # 如果还没有初始化 Git 仓库，执行：
   git init
   
   # 添加所有文件
   git add .
   
   # 提交代码
   git commit -m "Initial commit"
   
   # 添加远程仓库（替换为你的 GitHub 仓库地址）
   git remote add origin https://github.com/yourusername/your-repo.git
   
   # 推送到 GitHub
   git push -u origin main
   ```
   
   **注意**: 
   - 如果仓库已经存在，可以跳过 `git init`
   - 如果远程仓库已存在，使用 `git remote set-url origin https://github.com/yourusername/your-repo.git` 更新地址
   - 如果分支是 `master` 而不是 `main`，将 `main` 替换为 `master`

### 步骤 2: 在 Railway 创建项目

1. 登录 Railway (https://railway.app)
2. 点击 "New Project"
3. 选择 "Deploy from GitHub repo"
4. 选择你的仓库
5. Railway 会自动检测项目结构

### 步骤 3: 配置 Railway 服务

由于这是一个前后端分离的项目，你需要在 Railway 中创建两个服务：

#### 3.1 创建后端服务

1. 在 Railway 项目中，点击 "New Service"
2. 选择 "GitHub Repo" 并选择你的仓库
3. 在服务设置中：
   - **Root Directory**: 设置为 `backend`
   - **Build Command**: Railway 会自动检测（使用 Nixpacks）
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

#### 3.2 创建前端服务

1. 再次点击 "New Service"
2. 选择 "GitHub Repo" 并选择你的仓库
3. 在服务设置中：
   - **Root Directory**: 设置为 `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Start Command**: `npm run preview -- --host 0.0.0.0 --port $PORT`

### 步骤 4: 配置环境变量

#### 后端环境变量

在后端服务的 "Variables" 标签页中添加：

```
LLM_PROVIDER=openai
OPENAI_API_KEY=你的OpenAI_API密钥
ALLOWED_ORIGINS=https://你的前端域名.railway.app
PORT=8000
```

**重要**: 
- 将 `ALLOWED_ORIGINS` 设置为你的前端 Railway URL（部署后会获得）
- 如果使用自定义域名，也要添加到 `ALLOWED_ORIGINS` 中

#### 前端环境变量

在前端服务的 "Variables" 标签页中添加：

```
VITE_API_BASE_URL=https://你的后端域名.railway.app/api
PORT=3000
```

**注意**: 
- `VITE_API_BASE_URL` 需要在构建时设置，所以部署前需要先部署后端获取 URL
- 或者使用 Railway 的引用变量功能：`${{Backend.RAILWAY_PUBLIC_DOMAIN}}`

### 步骤 5: 配置 GitHub Actions

1. 在 GitHub 仓库中，进入 "Settings" → "Secrets and variables" → "Actions"
2. 添加以下 Secret：
   - `RAILWAY_TOKEN`: 从 Railway Dashboard → Account Settings → Tokens 获取

### 步骤 6: 部署流程

#### 方式一：使用 Railway 自动部署（推荐）

1. Railway 会自动检测到代码推送并开始部署
2. 等待构建完成
3. Railway 会为每个服务生成一个公共 URL

#### 方式二：使用 GitHub Actions

1. 推送代码到 `main` 分支
2. GitHub Actions 会自动运行测试
3. 测试通过后自动部署到 Railway

### 步骤 7: 配置域名（可选）

1. 在 Railway 服务设置中，点击 "Settings" → "Networking"
2. 为前端和后端服务分别配置自定义域名
3. 更新环境变量中的 `ALLOWED_ORIGINS` 和 `VITE_API_BASE_URL`

### 步骤 8: 初始化向量数据库

首次部署后，需要初始化向量数据库：

1. 访问后端 API 文档：`https://你的后端域名.railway.app/docs`
2. 调用 `/api/check_and_index` 端点来索引内部文档
3. 或者通过前端界面的 "Index Documents" 功能

## 🔧 配置文件说明

### `.github/workflows/deploy.yml`
GitHub Actions 工作流文件，用于：
- 运行测试
- 自动部署到 Railway

### `railway.json`
Railway 配置文件，定义构建和部署设置

### `backend/Procfile`
后端启动命令配置

### `frontend/Procfile`
前端启动命令配置

## 📝 环境变量参考

### 后端环境变量

| 变量名 | 说明 | 必需 | 默认值 |
|--------|------|------|--------|
| `LLM_PROVIDER` | LLM 提供者 | 是 | `openai` |
| `OPENAI_API_KEY` | OpenAI API 密钥 | 是 | - |
| `LLM_MODEL` | LLM 模型 | 否 | `gpt-4o-mini` |
| `EMBED_MODEL` | 嵌入模型 | 否 | `text-embedding-3-large` |
| `ALLOWED_ORIGINS` | 允许的 CORS 源 | 是 | `http://localhost:3000,...` |
| `PORT` | 服务端口 | 否 | Railway 自动设置 |
| `CHROMA_DIR` | 向量数据库目录 | 否 | `storage/chroma` |
| `INTERNAL_DATA_DIR` | 内部文档目录 | 否 | `company/EDU` |
| `REPORTS_DIR` | 报告存储目录 | 否 | `storage/reports` |

### 前端环境变量

| 变量名 | 说明 | 必需 | 默认值 |
|--------|------|------|--------|
| `VITE_API_BASE_URL` | 后端 API 地址 | 是 | `http://localhost:8000/api` |
| `PORT` | 服务端口 | 否 | Railway 自动设置 |

## 🐛 故障排除

### 问题 1: CORS 错误

**症状**: 前端无法连接到后端 API

**解决方案**:
1. 检查后端 `ALLOWED_ORIGINS` 环境变量是否包含前端 URL
2. 确保 URL 格式正确（包含协议 `https://`）
3. 多个域名用逗号分隔，不要有空格

### 问题 2: 前端无法找到后端 API

**症状**: 前端显示 API 连接错误

**解决方案**:
1. 检查 `VITE_API_BASE_URL` 环境变量是否正确
2. **重要**: Vite 环境变量需要在构建时设置，修改后需要重新构建
3. 确保后端服务已成功部署并运行

### 问题 3: 向量数据库未初始化

**症状**: 检索功能不工作

**解决方案**:
1. 访问后端 API 文档
2. 调用 `/api/check_and_index` 端点
3. 等待索引完成（可能需要几分钟）

### 问题 4: 构建失败

**症状**: Railway 构建错误

**解决方案**:
1. 检查 `requirements.txt` 和 `package.json` 是否正确
2. 查看 Railway 构建日志
3. 确保 Python 和 Node.js 版本兼容

## 🔄 更新部署

每次推送代码到 `main` 分支时：
1. GitHub Actions 会自动运行测试
2. Railway 会自动检测更改并重新部署
3. 或者手动在 Railway Dashboard 中触发部署

## 📚 相关资源

- [Railway 文档](https://docs.railway.app)
- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [FastAPI 部署指南](https://fastapi.tiangolo.com/deployment/)
- [Vite 部署指南](https://vitejs.dev/guide/static-deploy.html)

## 💡 最佳实践

1. **环境变量管理**: 使用 Railway 的环境变量功能，不要将敏感信息提交到代码仓库
2. **监控**: 使用 Railway 的监控功能跟踪服务状态
3. **日志**: 定期查看 Railway 的日志以排查问题
4. **备份**: 定期备份向量数据库和重要数据
5. **测试**: 在本地充分测试后再部署到生产环境
