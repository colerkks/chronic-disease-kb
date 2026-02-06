# 🏥 Agent慢病管理知识库系统

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **AI驱动的慢病管理知识库系统** - 基于多智能体架构的医疗知识问答平台

## 🌟 系统特性

### 🤖 智能多Agent架构
- **QueryAgent** - 自然语言查询理解与意图识别
- **RetrievalAgent** - RAG检索增强生成，智能知识检索
- **RecommendationAgent** - 基于患者画像的个性化健康建议
- **Orchestrator** - 多智能体协调与任务编排

### 📚 医疗知识覆盖
支持7种常见慢性疾病：
- 🩸 **糖尿病** - 1型、2型、妊娠糖尿病管理
- ❤️ **高血压** - 分级诊疗与用药指导  
- 💔 **心脏病** - 冠心病、心力衰竭防治
- 🫁 **呼吸系统** - 哮喘、COPD管理
- 🦴 **风湿免疫** - 骨关节炎、类风湿关节炎

### 🔧 核心技术
- **RAG检索** - ChromaDB向量数据库 + 语义搜索
- **FastAPI** - 高性能异步API框架
- **Pydantic** - 严格数据验证与序列化
- **Sentence-Transformers** - 医疗文本语义嵌入

---

## 🚀 快速开始

### 1️⃣ 环境准备

```bash
# 克隆项目
cd chronic-disease-kb

# 安装依赖
pip install -r requirements.txt
```

### 2️⃣ 配置环境

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，添加你的API密钥
# OPENAI_API_KEY=your_key_here
```

### 3️⃣ 启动系统

```bash
# 初始化知识库
python scripts/init_kb.py

# 启动API服务器
python scripts/start_server.py

# 或使用uvicorn直接启动
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### 4️⃣ 访问文档

- 📖 **API文档**: http://localhost:8000/docs
- 🔍 **健康检查**: http://localhost:8000/health

---

## 📡 API使用示例

### 查询知识库

```bash
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "2型糖尿病的早期症状是什么？",
    "patient_id": "patient_123",
    "max_results": 5
  }'
```

**响应示例：**
```json
{
  "query_id": "query_20240204_001",
  "query": "2型糖尿病的早期症状是什么？",
  "answer": "2型糖尿病的早期症状包括多尿、口渴增加、疲劳、视力模糊...",
  "confidence": 0.92,
  "sources": ["medical_knowledge_base"],
  "recommendations": ["建议定期监测血糖", "保持健康饮食"]
}
```

### 创建患者档案

```bash
curl -X POST "http://localhost:8000/api/v1/patients" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "张三",
    "age": 55,
    "gender": "male",
    "chronic_conditions": ["diabetes_type2", "hypertension"],
    "allergies": ["penicillin"]
  }'
```

### 记录健康指标

```bash
curl -X POST "http://localhost:8000/api/v1/patients/patient_123/metrics" \
  -H "Content-Type: application/json" \
  -d '{
    "metric_type": "blood_pressure",
    "value": {"systolic": 120, "diastolic": 80},
    "unit": "mmHg",
    "timestamp": "2026-02-04T10:00:00"
  }'
```

### 获取个性化建议

```bash
curl -X POST "http://localhost:8000/api/v1/recommendations" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "patient_123",
    "recommendation_type": "diet",
    "context": "newly_diagnosed_type2_diabetes"
  }'
```

---

## 🏗️ 项目结构

```
chronic-disease-kb/
├── 📁 agents/                 # AI智能体模块
│   ├── __init__.py
│   └── orchestrator.py        # Agent协调器
│
├── 📁 api/                    # FastAPI接口层
│   ├── __init__.py
│   ├── main.py                # 应用入口
│   └── routes/                # API路由
│       ├── health.py          # 健康检查
│       ├── knowledge.py       # 知识库管理
│       ├── patients.py        # 患者管理
│       ├── query.py           # 智能查询
│       └── recommendations.py # 个性化建议
│
├── 📁 kb/                     # 知识库模块
│   ├── __init__.py
│   ├── vector_store.py        # 向量数据库(ChromaDB)
│   └── knowledge_base.py      # 知识库管理
│
├── 📁 models/                 # Pydantic数据模型
│   ├── __init__.py
│   ├── patient.py             # 患者模型
│   ├── disease.py             # 疾病模型
│   ├── treatment.py           # 治疗模型
│   ├── metric.py              # 健康指标模型
│   └── query.py               # 查询模型
│
├── 📁 data/                   # 数据文件
│   └── sample_knowledge.py    # 示例医疗知识
│
├── 📁 scripts/                # 实用脚本
│   ├── init_kb.py             # 初始化知识库
│   └── start_server.py        # 启动服务器
│
├── 📁 tests/                  # 测试套件
│   ├── test_models.py         # 模型测试
│   └── test_kb.py             # 知识库测试
│
├── 📄 config.py               # 配置文件
├── 📄 requirements.txt        # Python依赖
├── 📄 .env.example            # 环境变量模板
└── 📄 pytest.ini             # 测试配置
```

---

## ⚙️ 配置说明

编辑 `.env` 文件配置API密钥：

```env
# OpenAI (用于Agent的智能回复)
OPENAI_API_KEY=sk-your_openai_key_here

# Anthropic Claude (备选)
ANTHROPIC_API_KEY=your_anthropic_key_here

# Google Gemini (备选)
GOOGLE_API_KEY=your_google_key_here

# 默认配置
DEFAULT_LLM_PROVIDER=openai
DEFAULT_MODEL=gpt-3.5-turbo
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# 数据库
DATABASE_URL=sqlite:///./data/chronic_disease.db
VECTOR_DB_PATH=./data/vector_db
```

---

## 🧪 测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_models.py
pytest tests/test_kb.py

# 带覆盖率报告
pytest --cov=.
```

---

## 🛠️ 技术栈

| 技术 | 用途 | 版本 |
|------|------|------|
| **Python** | 编程语言 | 3.9+ |
| **FastAPI** | Web框架 | 0.104+ |
| **Uvicorn** | ASGI服务器 | 0.24+ |
| **ChromaDB** | 向量数据库 | 0.4+ |
| **SQLAlchemy** | ORM | 2.0+ |
| **Pydantic** | 数据验证 | 2.5+ |
| **Sentence-Transformers** | 文本嵌入 | 2.2+ |
| **Pytest** | 测试框架 | 7.4+ |

---

## ⚠️ 重要声明

**医疗免责声明：**
- 本系统提供的医疗信息**仅供参考**
- **不能替代**专业医疗诊断和治疗建议
- 如有严重症状，请**立即就医**
- 用药调整必须**咨询医生**

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## ©️ 版权归属

Copyright (c) 2026 colerkks. All rights reserved.

项目代码、文档与相关内容的著作权归 `colerkks` 所有。

---

## 📞 支持与反馈

如有问题或建议，欢迎提交 Issue 或 Pull Request！

---

**版本**: 1.0.0  
**创建时间**: 2026-02-04  
**作者**: colerkks  
**状态**: ✅ 生产就绪

🎉 **系统已就绪，可以立即开始使用！**
