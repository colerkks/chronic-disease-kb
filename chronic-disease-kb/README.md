# Chronic Disease KB (临床应用导向)

> 这是一个以**临床应用为核心**、以**全球权威指南训练**为底座的慢病知识库系统。
>
> 当前代码已具备 `RAG 检索 + 多 Agent 编排 + 患者档案/指标/建议 API` 基础能力；本 README 将知识库结构升级为可持续的临床级治理框架。

## 1. 项目定位

- 目标不是“通用医学问答”，而是面向慢病管理的**临床决策支持型知识库**。
- 核心约束：
  - 训练内容优先来自国际/国家权威指南与共识；
  - 每条知识都可追溯来源、版本、更新时间；
  - 输出对临床流程有用（评估 -> 干预 -> 随访 -> 预警）。

## 2. 当前系统能力（已实现）

- 多 Agent 流程：`QueryAgent -> RetrievalAgent -> RecommendationAgent -> Orchestrator`（`agents/orchestrator.py`）
- 知识库管理：文档切块、向量检索、元数据过滤（`kb/knowledge_base.py`, `kb/vector_store.py`）
- 临床接口：
  - 患者档案与健康指标：`api/routes/patients.py`
  - 知识检索：`api/routes/knowledge.py`
  - 智能问答：`api/routes/query.py`
  - 个性化建议：`api/routes/recommendations.py`
- 数据模型基础：`models/` 下 patient / metric / disease / query 等
- 治理校验（已生效）：
  - 入库必填元数据：`source_id` / `document_version` / `evidence_level`
  - `source_id` 必须在 `data/sources/source_registry.yaml` 注册
  - `evidence_level` 受枚举约束，非法值返回 400（`/api/v1/knowledge/add`）

## 3. 知识库核心结构（v1.1 已落地，持续完善）

在现有结构基础上，建议将 `data/` 与 `kb/` 的知识内容组织为以下分层（文档与数据治理层）：

```text
kb/
  knowledge_base.py
  vector_store.py

data/
  sample_knowledge.py
  sources/                      # 新增：权威来源登记
    source_registry.yaml        # 来源主数据（机构、文档、版本、URL、许可）
  guidelines/                   # 新增：按疾病和指南版本沉淀结构化知识
    diabetes/
      ada-2026/
        overview.md
        diagnosis.md
        treatment.md
        monitoring.md
        citations.json
    hypertension/
      nice-ng136/
      esc-esh/
  evidence/                     # 新增：证据分级映射
    grade_mapping.yaml
  governance/                   # 新增：治理策略
    review_policy.md
    update_calendar.yaml
    changelog.md
```

说明：
- 当前仓库已具备代码执行链路；上述结构用于补齐“权威训练 + 临床可追溯”的治理能力。
- 当前已落地：`data/sources/source_registry.yaml` 与写入链路治理校验（见 `kb/knowledge_base.py`）。

## 4. 全球权威来源分层（训练白名单）

### A 级：国际权威指南/战略（优先）

- WHO（慢病整体策略与基层管理）
  - WHO PEN: https://www.who.int/publications/i/item/9789240009226
- ADA（糖尿病金标准）
  - Standards of Care 2026: https://diabetes.org/newsroom/press-releases/american-diabetes-association-releases-standards-care-diabetes-2026
  - Diabetes Care 专刊索引: https://diabetesjournals.org/care/article/49/Supplement_1/S6/163930
- KDIGO（CKD）
  - 2024 CKD Guideline: https://kdigo.org/guidelines/ckd-evaluation-and-management/
- GOLD（COPD）
  - 2026 Report: https://goldcopd.org/2026-gold-report-and-pocket-guide/
- GINA（哮喘）
  - 2025 Strategy: https://ginasthma.org/2025-gina-strategy-report/
- NICE（英国临床指南，含更新状态）
  - Cardiometabolic guideline hub: https://www.nice.org.uk/hub/indevelopment/gid-hub10002

### B 级：国家级指南/学会共识（本地化必须）

- 各国家/地区卫健委、学会指南（例如中国高血压、糖尿病、COPD 指南）
- 用于补充 A 级在本地用药可及性、医保路径和随访制度差异。

### C 级：高质量综述/系统评价

- 仅用于解释性补充，不覆盖 A/B 级主推荐。

## 5. 证据分级与元数据标准（必须在知识条目中体现）

当前代码已有基础字段（如 `sources`, `last_updated`, `confidence`），建议升级为标准化元数据：

```json
{
  "source_id": "ada-2026-soc",
  "organization": "American Diabetes Association",
  "document_title": "Standards of Care in Diabetes—2026",
  "document_version": "2026.1",
  "publication_date": "2025-12-08",
  "access_date": "2026-02-13",
  "url": "https://diabetesjournals.org/...",
  "evidence_level": "GRADE_HIGH",
  "recommendation_strength": "STRONG",
  "applicability": "adult_type2_diabetes_primary_care",
  "review_status": "medical_reviewed",
  "reviewed_by": "endocrinology_md",
  "review_due_date": "2026-12-31"
}
```

最小要求（MVP）：
- 每个知识片段至少包含：`organization / title / version / publication_date / url / evidence_level / review_due_date`
- 若缺少上述字段，知识不得进入生产检索集合。

当前实现中的硬约束（已生效）：
- 必填：`source_id`、`document_version`、`evidence_level`
- `source_id`：小写 slug 格式，且必须存在于 `data/sources/source_registry.yaml`
- `document_version`：仅允许字母数字及 `.` `_` `-`
- `evidence_level` 允许值：`GRADE_HIGH` / `GRADE_MODERATE` / `GRADE_LOW` / `GUIDELINE_CONSENSUS` / `EXPERT_OPINION`
- 任一规则不满足时，`POST /api/v1/knowledge/add` 返回 400

## 6. 临床应用优先的内容组织方式

每个慢病应按临床路径建模，而不是仅按百科字段堆叠：

1. 评估与分层（诊断标准、风险分层）
2. 干预策略（生活方式、药物、联合治疗）
3. 监测与目标（指标阈值、复查频次、达标定义）
4. 危险信号与转诊（红旗症状、急诊指征）
5. 随访计划（门诊/远程随访节点）

与现有 API 对齐：
- `POST /api/v1/patients`：患者基础画像与慢病组合
- `POST /api/v1/patients/{patient_id}/metrics`：持续指标采集
- `POST /api/v1/query`：临床问题检索与解释
- `POST /api/v1/recommendations`：个性化建议生成

## 7. 更新治理机制（防过期、防漂移）

- 更新周期建议：
  - A 级来源：每月扫描更新公告，季度强制复核
  - B 级来源：季度复核
  - C 级来源：半年复核
- 变更流程：
  1. 发现新版本指南
  2. 生成差异清单（新增/删除/阈值变化）
  3. 医学审核
  4. 更新知识条目版本与 `changelog`
  5. 回归测试（检索、回答、推荐）

## 8. 安全边界与免责声明

- 系统输出用于临床支持，不替代执业医师诊疗决策。
- 对以下场景强制提示急诊/线下就医：持续胸痛、严重呼吸困难、意识障碍、卒中疑似症状等。
- 药物调整类建议必须包含“需医生确认”警示。

## 9. 快速启动

```bash
pip install -r requirements.txt
cp .env.example .env
python scripts/init_kb.py
python scripts/start_server.py
```

访问：
- API 文档：`http://localhost:8000/docs`
- 健康检查：`http://localhost:8000/health`

## 10. 下一步实施优先级（建议）

已完成：
1. 在 `data/sources/` 落地 `source_registry.yaml`（覆盖糖尿病/高血压/COPD/哮喘）
2. 在知识写入链路补齐 `source_id` / `evidence_level` / `document_version` 校验
3. 增加治理测试（缺失来源元数据、未知 source_id、非法 evidence_level）

下一步：
1. 使用 `source_registry.yaml` 的 `disease_source_priority` 驱动映射，替代代码硬编码
2. 增加治理正向测试（合法元数据可成功入库）并接入 CI
3. 新增 `governance/changelog.md`，实现指南更新审计闭环

---

## 医疗声明

- 本系统提供内容仅供医学教育与辅助决策参考。
- 不能替代医生面诊、处方和个体化治疗。
- 紧急情况请立即联系急救系统或前往急诊。
