# 🚀 Railway 部署检查清单

## ✅ 部署前准备

- [ ] 代码已推送到 GitHub 仓库
- [ ] 已注册 Railway 账户
- [ ] 已准备好 OpenAI API Key

## 📦 Railway 项目设置

### 后端服务
- [ ] 创建新服务，选择 GitHub 仓库
- [ ] 设置 Root Directory: `backend`
- [ ] 确认 Build Command: `pip install -r requirements.txt`
- [ ] 确认 Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### 前端服务
- [ ] 创建新服务，选择 GitHub 仓库
- [ ] 设置 Root Directory: `frontend`
- [ ] 确认 Build Command: `npm install && npm run build`
- [ ] 确认 Start Command: `npm run preview -- --host 0.0.0.0 --port $PORT`

## 🔐 环境变量配置

### 后端环境变量
- [ ] `LLM_PROVIDER=openai`
- [ ] `OPENAI_API_KEY=你的密钥`
- [ ] `ALLOWED_ORIGINS=https://你的前端域名.railway.app` (部署后更新)
- [ ] `PORT=8000` (Railway 自动设置)

### 前端环境变量
- [ ] `VITE_API_BASE_URL=https://你的后端域名.railway.app/api` (部署后更新)
- [ ] `PORT=3000` (Railway 自动设置)

## 🧪 测试

- [ ] 后端服务成功启动
- [ ] 前端服务成功启动
- [ ] 前端可以访问后端 API
- [ ] CORS 配置正确
- [ ] 调用 `/api/check_and_index` 初始化向量数据库

## 📝 部署后操作

- [ ] 更新 `ALLOWED_ORIGINS` 为实际前端 URL
- [ ] 更新 `VITE_API_BASE_URL` 为实际后端 URL
- [ ] 重新部署前端（因为 Vite 变量需要在构建时设置）
- [ ] 测试完整功能流程

## 🔄 持续集成

- [ ] GitHub Actions 工作流正常运行
- [ ] 代码推送后自动触发部署
- [ ] 测试通过后才部署
