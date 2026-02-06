# 空头报告反驳助手 (Short Report Rebuttal Assistant)

一个基于RAG（检索增强生成）的MVP系统，用于分析空头报告并生成反驳分析。

## 项目结构

```
rag_demo/
├── backend/              # FastAPI 后端
│   ├── app/             # 应用模块
│   ├── main.py          # FastAPI 主应用
│   ├── requirements.txt # Python 依赖
│   └── .env.example     # 环境变量示例
├── frontend/            # React 前端
│   ├── src/             # React 源代码
│   ├── package.json     # Node.js 依赖
│   └── vite.config.js   # Vite 配置
├── company/             # 内部文档目录
│   └── EDU/
├── storage/             # 数据存储
│   ├── chroma/         # ChromaDB 向量数据库
│   └── reports/        # 生成的报告
└── run.sh              # 启动脚本（Linux/Mac）
```

## 快速开始

### 1. 安装后端依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 安装前端依赖

```bash
cd frontend
npm install
```

### 3. 配置环境变量

创建 `backend/.env` 文件：

```bash
cd backend
cp .env.example .env
```

编辑 `.env` 文件，设置以下变量：

```env
# OpenAI 配置（必需）
OPENAI_API_KEY=sk-your-openai-api-key-here

# 可选配置
LLM_MODEL=gpt-4o-mini                    # LLM 模型
EMBED_MODEL=text-embedding-3-large        # 嵌入模型
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173  # CORS 允许的源
```

### 4. 索引内部文档

在首次使用前，需要索引内部文档到向量数据库：

```bash
cd backend
python -m app.index_internal
```

### 5. 启动服务

**方式一：使用启动脚本（Linux/Mac）**

```bash
# 在项目根目录
./run.sh
```

**方式二：分别启动**

**后端:**
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**前端:**
```bash
cd frontend
npm run dev
```

**Windows 用户:**

可以使用 `start.bat` 脚本（如果存在），或手动启动：

```powershell
# 后端
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 前端（新终端）
cd frontend
npm run dev
```

## 访问地址

- **前端**: http://localhost:3000
- **后端API**: http://localhost:8000
- **API文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/health

## 技术栈

### 后端
- **FastAPI** - 现代 Python Web 框架
- **ChromaDB** - 向量数据库，用于存储和检索文档嵌入
- **OpenAI API** - LLM 和嵌入模型
  - LLM: `gpt-4o-mini` (默认)
  - Embedding: `text-embedding-3-large` (默认，3072维)

### 前端
- **React 18** - UI 框架
- **Vite** - 构建工具和开发服务器
- **Axios** - HTTP 客户端

## 功能特性

- 📄 **PDF处理**: 自动提取空头报告前3页内容
- 🔍 **论点提取**: 使用 OpenAI LLM 识别独立、可测试的论点
- 📚 **证据检索**: 从本地向量数据库检索相关内部证据
- ⚖️ **智能判断**: 评估每个论点的覆盖情况（完全/部分/未解决）
- 📊 **报告生成**: 生成分析师风格的分析报告（Markdown/JSON/PDF格式）

## 部署

### Railway 部署

项目已配置支持 Railway 部署，详细步骤请参考：

- [GitHub Actions + Railway 部署指南](GITHUB_ACTIONS_RAILWAY_DEPLOY.md)
- [Railway 设置指南](RAILWAY_SETUP.md)
- [Railway 故障排除](RAILWAY_TROUBLESHOOTING.md)

**快速部署步骤：**

1. 在 Railway 创建两个服务（前端和后端）
2. 配置环境变量（见下方）
3. 设置 Root Directory、Build Command 和 Start Command
4. 连接 GitHub 仓库，自动部署

**Railway 环境变量配置：**

**后端服务：**
```
OPENAI_API_KEY=sk-your-key-here
ALLOWED_ORIGINS=https://your-frontend-domain.railway.app
INTERNAL_DATA_DIR=company/EDU
```

**前端服务：**
```
VITE_API_BASE_URL=https://your-backend-domain.railway.app/api
```

## 开发

### 后端开发

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 前端开发

```bash
cd frontend
npm run dev
```

## 构建生产版本

### 前端

```bash
cd frontend
npm run build
```

构建产物在 `frontend/dist/` 目录

### 后端

后端使用 FastAPI，生产环境建议使用：

```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

或使用 Gunicorn：

```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 故障排除

### OpenAI API 连接失败

1. **检查 API 密钥**: 确保 `OPENAI_API_KEY` 环境变量已正确设置
2. **验证密钥格式**: API 密钥应以 `sk-` 开头
3. **检查网络连接**: 确保可以访问 OpenAI API
4. **查看日志**: 检查后端日志中的错误信息

### 向量数据库问题

如果遇到嵌入维度不匹配错误：

```bash
cd backend
# 删除旧的向量数据库
rm -rf storage/chroma

# 重新索引文档
python -m app.index_internal
```

### 端口被占用

- 后端默认端口: 8000
- 前端默认端口: 3000

可以在启动命令中修改端口：

```bash
# 后端
uvicorn main:app --port 8001

# 前端
npm run dev -- --port 3001
```

### CORS 错误

如果前端无法访问后端 API，检查：

1. 后端 `ALLOWED_ORIGINS` 环境变量是否包含前端地址
2. 前端 `VITE_API_BASE_URL` 是否指向正确的后端地址

## API 文档

详细的 API 文档和使用说明请查看：

- [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - 完整的 API 文档和使用指南

### 主要 API 端点

- `GET /` - API 信息
- `GET /health` - 健康检查
- `POST /api/check_and_index` - 检查并索引内部文档
- `POST /api/upload_report` - 上传空头报告
- `POST /api/extract_claims` - 提取论点
- `POST /api/analyze` - 分析论点并生成报告
- `GET /api/download_report/{report_id}` - 下载报告（支持 md/json/pdf 格式）

## 环境变量说明

### 后端环境变量

| 变量名 | 必需 | 默认值 | 说明 |
|--------|------|--------|------|
| `OPENAI_API_KEY` | ✅ | - | OpenAI API 密钥 |
| `LLM_MODEL` | ❌ | `gpt-4o-mini` | LLM 模型名称 |
| `EMBED_MODEL` | ❌ | `text-embedding-3-large` | 嵌入模型名称 |
| `ALLOWED_ORIGINS` | ❌ | `http://localhost:3000,...` | CORS 允许的源（逗号分隔） |
| `INTERNAL_DATA_DIR` | ❌ | `company/EDU` | 内部文档目录 |
| `CHROMA_DIR` | ❌ | `storage/chroma` | ChromaDB 存储目录 |
| `REPORTS_DIR` | ❌ | `storage/reports` | 报告存储目录 |

### 前端环境变量

| 变量名 | 必需 | 默认值 | 说明 |
|--------|------|--------|------|
| `VITE_API_BASE_URL` | ❌ | `http://localhost:8000/api` | 后端 API 地址 |

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 更新日志

### v1.0.0
- ✅ 移除 Ollama 支持，仅使用 OpenAI
- ✅ 简化配置，只需设置 `OPENAI_API_KEY`
- ✅ 优化代码结构，减少约 185 行代码
- ✅ 支持 Railway 部署
- ✅ 完整的 API 文档
