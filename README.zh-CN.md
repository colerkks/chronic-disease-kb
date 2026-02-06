# 慢病管理知识库（Chronic Disease Management Knowledge Base）

一个面向慢性疾病管理的 AI 知识库系统，提供智能检索、个性化建议与 RESTful API 接入能力。

## 🌟 主要特性

- **全面知识库**：覆盖糖尿病、高血压、冠心病、哮喘、COPD、关节炎等
- **AI 智能体**：理解用户问题、检索知识、生成个性化建议
- **向量检索**：RAG 语义检索与文档检索增强
- **患者管理**：健康指标、治疗方案与趋势分析
- **RESTful API**：完整的外部服务接口

## 🏗️ 项目结构

```
chronic_disease_kb/
├── agents/              # AI智能体
├── api/                 # FastAPI接口
├── core/                # 核心业务逻辑
├── data/                # 数据和示例
├── db/                  # 数据库模型
├── kb/                  # 知识库模块
├── models/              # Pydantic数据模型
├── scripts/             # 实用脚本
├── tests/               # 测试文件
├── config.py            # 配置文件
└── README.md            # 项目说明
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env，填入 API Key 等配置
```

### 3. 初始化知识库

```bash
python scripts/init_kb.py
```

### 4. 启动服务

```bash
python scripts/start_server.py
```

### 5. 访问 API 文档

打开浏览器访问：`http://localhost:8000/docs`

## 📚 API 使用示例

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

### 获取知识库统计

```bash
curl "http://localhost:8000/api/v1/knowledge/stats"
```

### 创建患者

```bash
curl -X POST "http://localhost:8000/api/v1/patients" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "张三",
    "age": 55,
    "gender": "male",
    "chronic_conditions": ["diabetes_type2", "hypertension"]
  }'
```

### 添加健康指标

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

## 🤖 智能体说明

- **QueryAgent**：理解自然语言健康问题并提取关键实体
- **RetrievalAgent**：进行语义检索与知识定位
- **RecommendationAgent**：生成个性化健康建议
- **AgentOrchestrator**：协调多智能体工作流

## 📦 典型疾病覆盖

- **糖尿病**：1型、2型、妊娠糖尿病、前期糖尿病
- **高血压**：原发性、继发性、高血压急症
- **心脏病**：冠心病、心力衰竭、心律失常
- **呼吸系统**：哮喘、COPD
- **肌肉骨骼**：骨关节炎、类风湿关节炎
- **其他**：慢性肾病、血脂异常、脑卒中

## 🛠️ 技术栈

- **Python 3.9+**
- **FastAPI**
- **ChromaDB**
- **SQLAlchemy**
- **Sentence-Transformers**
- **Pydantic**

## ✅ 测试

```bash
pytest -q
```

> 若缺少依赖，请先安装 `requirements.txt` 中的依赖。

## 📄 License

MIT License
