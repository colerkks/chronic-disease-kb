"""
Sample medical knowledge data for chronic diseases
"""

from models.disease import DiseaseKnowledge, DiseaseCategory
from datetime import datetime

# Sample knowledge documents
DIABETES_TYPE2_KNOWLEDGE = [
    {
        "name": "2型糖尿病",
        "category": DiseaseCategory.ENDOCRINE,
        "overview": """2型糖尿病是一种慢性代谢性疾病，特征是高血糖、胰岛素抵抗和相对胰岛素缺乏。
        它是全球最常见的糖尿病类型，约占所有糖尿病病例的90-95%。""",
        "symptoms": {
            "common": ["多尿（频繁排尿）", "口渴增加", "疲劳", "视力模糊", "伤口愈合缓慢"],
            "early": ["轻度疲劳", "饭后嗜睡", "皮肤感染频繁"],
            "severe": ["极度口渴", "恶心", "呼吸困难", "意识模糊"]
        },
        "causes": ["胰岛素抵抗", "β细胞功能减退", "遗传因素", "肥胖", "缺乏运动"],
        "risk_factors": {
            "modifiable": ["超重/肥胖", "久坐不动的生活方式", "不健康饮食", "吸烟"],
            "non_modifiable": ["年龄（45岁以上风险增加）", "家族史", "种族（某些族群风险更高）"]
        },
        "treatments": {
            "lifestyle": ["健康饮食（地中海饮食、低碳水化合物）", "规律运动（每周150分钟中等强度）", "减重（5-10%可显著改善）", "戒烟限酒"],
            "medications": ["二甲双胍（一线药物）", "GLP-1受体激动剂", "SGLT2抑制剂", "胰岛素（必要时）"],
            "monitoring": ["定期监测血糖", "HbA1c每3-6个月检查", "肾功能监测", "眼底检查"]
        },
        "complications": ["心血管疾病", "肾病", "视网膜病变", "神经病变", "糖尿病足", "中风"],
        "prevention": ["保持健康体重", "规律运动", "健康饮食", "定期体检", "管理血压和血脂"],
        "sources": ["ADA Standards of Care 2024", "WHO Diabetes Guidelines"]
    }
]

HYPERTENSION_KNOWLEDGE = [
    {
        "name": "高血压",
        "category": DiseaseCategory.CARDIOVASCULAR,
        "overview": """高血压是指动脉血压持续升高，收缩压≥140 mmHg或舒张压≥90 mmHg。
        被称为"沉默杀手"，因为通常无明显症状但可导致严重并发症。""",
        "symptoms": {
            "common": ["通常无症状", "头痛（严重高血压时）", "头晕", "鼻出血"],
            "severe": ["胸痛", "呼吸困难", "严重头痛", "视力变化", "血尿"]
        },
        "causes": ["原发性（90-95%，原因不明）", "继发性（肾脏疾病、内分泌疾病、药物等）"],
        "risk_factors": {
            "modifiable": ["高盐饮食", "超重", "缺乏运动", "过量饮酒", "吸烟", "压力"],
            "non_modifiable": ["年龄", "家族史", "种族（非洲裔风险更高）"]
        },
        "treatments": {
            "lifestyle": ["DASH饮食", "限盐（<5g/天）", "减重", "规律运动", "限制饮酒", "戒烟"],
            "medications": ["ACE抑制剂", "ARBs", "钙通道阻滞剂", "利尿剂", "β受体阻滞剂"],
            "targets": ["<140/90 mmHg（一般人群）", "<130/80 mmHg（糖尿病或肾病患者）"]
        },
        "complications": ["心脏病", "中风", "肾衰竭", "视网膜病变", "主动脉瘤"],
        "prevention": ["健康饮食", "规律运动", "维持健康体重", "限制钠摄入", "定期监测血压"],
        "sources": ["ACC/AHA Guidelines 2024", "中国高血压防治指南"]
    }
]

ASTHMA_KNOWLEDGE = [
    {
        "name": "哮喘",
        "category": DiseaseCategory.RESPIRATORY,
        "overview": """哮喘是一种慢性气道炎症性疾病，特征是可逆性气流受限和气道高反应性。
        症状包括喘息、气短、胸闷和咳嗽，常在夜间或清晨加重。""",
        "symptoms": {
            "common": ["喘息", "气短", "胸闷", "咳嗽（尤其夜间）"],
            "triggers": ["运动诱发", "过敏原暴露", "冷空气", "呼吸道感染"],
            "severe": ["严重呼吸困难", "无法完整说话", "嘴唇发紫", "意识改变"]
        },
        "causes": ["遗传因素", "环境过敏原", "呼吸道感染", "职业暴露"],
        "risk_factors": {
            "modifiable": ["吸烟", "职业暴露", "过敏原接触"],
            "non_modifiable": ["家族史", "特应性体质", "性别（儿童期男性多见，青春期后女性多见）"]
        },
        "treatments": {
            "controller": ["吸入性糖皮质激素（ICS）", "长效β2受体激动剂（LABA）", "白三烯调节剂"],
            "reliever": ["短效β2受体激动剂（SABA）", "抗胆碱能药物"],
            "biologics": ["抗IgE（奥马珠单抗）", "抗IL-5", "抗IL-4/13"],
            "action_plan": ["识别早期症状", "正确使用吸入器", "知道何时就医"]
        },
        "complications": ["哮喘持续状态", "呼吸衰竭", "气胸", "药物副作用"],
        "prevention": ["避免触发因素", "规律用药", "定期随访", "流感疫苗接种", "戒烟"],
        "sources": ["GINA Guidelines 2024", "中国哮喘防治指南"]
    }
]

HEART_DISEASE_KNOWLEDGE = [
    {
        "name": "冠心病",
        "category": DiseaseCategory.CARDIOVASCULAR,
        "overview": """冠心病（冠状动脉粥样硬化性心脏病）是由于冠状动脉粥样硬化导致血管狭窄或阻塞，
        引起心肌缺血、缺氧或坏死的心脏病。""",
        "symptoms": {
            "angina": ["胸痛或胸闷", "压迫感", "可放射至左肩、左臂、颈部或下颌", "持续数分钟"],
            "MI": ["剧烈胸痛", "持续>15分钟", "出汗", "恶心", "呼吸困难"],
            "atypical": ["上腹部不适", "背部疼痛", "极度疲劳（尤其女性）"]
        },
        "causes": ["动脉粥样硬化", "血栓形成", "血管痉挛"],
        "risk_factors": {
            "major": ["高血压", "高血脂", "糖尿病", "吸烟", "肥胖", "缺乏运动"],
            "other": ["年龄（男性>45，女性>55）", "家族史", "压力", "不健康饮食"]
        },
        "treatments": {
            "lifestyle": ["心脏康复", "戒烟", "健康饮食", "规律运动", "压力管理"],
            "medications": ["抗血小板药物（阿司匹林）", "他汀类药物", "β受体阻滞剂", "ACE抑制剂", "硝酸酯类"],
            "procedures": ["经皮冠状动脉介入治疗（PCI）", "冠状动脉旁路移植术（CABG）"]
        },
        "complications": ["心肌梗死", "心力衰竭", "心律失常", "心源性猝死"],
        "prevention": ["控制血压", "控制血脂", "管理糖尿病", "戒烟", "健康饮食", "规律运动"],
        "sources": ["AHA/ACC Guidelines", "中国心血管病预防指南"]
    }
]

COPD_KNOWLEDGE = [
    {
        "name": "慢性阻塞性肺疾病（COPD）",
        "category": DiseaseCategory.RESPIRATORY,
        "overview": """COPD是一种以持续气流受限为特征的常见、可预防和治疗的疾病。
        气流受限呈进行性发展，与气道和肺组织对有害颗粒或气体的慢性炎症反应增强有关。""",
        "symptoms": {
            "common": ["慢性咳嗽", "咳痰", "气短（呼吸困难）", "喘息", "胸闷"],
            "severe": ["严重呼吸困难", "发绀", "意识混乱", "下肢水肿"]
        },
        "causes": ["吸烟（主要原因）", "职业粉尘和化学物质", "室内外空气污染", "遗传因素（α1-抗胰蛋白酶缺乏）"],
        "risk_factors": {
            "major": ["吸烟史", "长期暴露于烟雾或化学物质", "家族史"],
            "other": ["年龄", "儿童期呼吸道感染", "社会经济地位低"]
        },
        "treatments": {
            "lifestyle": ["戒烟（最重要）", "避免刺激物", "营养支持", "肺康复训练"],
            "medications": ["支气管扩张剂（SABA, LABA, LAMA）", "吸入性糖皮质激素", "磷酸二酯酶-4抑制剂"],
            "oxygen": ["长期家庭氧疗（严重低氧血症）"],
            "surgery": ["肺减容术", "肺移植（终末期）"]
        },
        "complications": ["呼吸衰竭", "肺心病", "骨质疏松", "抑郁和焦虑", "肺癌"],
        "prevention": ["戒烟", "避免二手烟", "减少职业暴露", "预防呼吸道感染（疫苗接种）"],
        "sources": ["GOLD Guidelines 2024", "中国COPD诊治指南"]
    }
]

ARTHRITIS_KNOWLEDGE = [
    {
        "name": "骨关节炎",
        "category": DiseaseCategory.MUSCULOSKELETAL,
        "overview": """骨关节炎是最常见的关节炎类型，以关节软骨退行性变和继发性骨质增生为特征。
        主要影响膝关节、髋关节、脊柱和手的小关节。""",
        "symptoms": {
            "common": ["关节疼痛", "晨僵（<30分钟）", "关节活动受限", "关节摩擦感", "关节肿胀"],
            "progressive": ["持续性疼痛", "夜间疼痛", "功能障碍", "关节畸形"]
        },
        "causes": ["年龄（主要因素）", "关节损伤", "肥胖", "遗传因素", "关节过度使用"],
        "risk_factors": {
            "modifiable": ["肥胖", "关节损伤", "职业因素"],
            "non_modifiable": ["年龄", "女性", "遗传因素", "先天性关节异常"]
        },
        "treatments": {
            "non_pharmacological": ["减重", "运动（低冲击运动）", "物理治疗", "辅助器具", "热敷/冷敷"],
            "medications": ["对乙酰氨基酚", "非甾体抗炎药（NSAIDs）", "局部用药", "关节腔注射"],
            "surgical": ["关节镜手术", "截骨术", "关节置换术"]
        },
        "complications": ["关节功能丧失", "慢性疼痛", "抑郁", "睡眠障碍"],
        "prevention": ["保持健康体重", "适度运动", "避免关节损伤", "正确姿势"],
        "sources": ["ACR Guidelines", "中国骨关节炎诊治指南"]
    },
    {
        "name": "类风湿关节炎",
        "category": DiseaseCategory.MUSCULOSKELETAL,
        "overview": """类风湿关节炎（RA）是一种以侵蚀性、对称性多关节炎为主要临床表现的慢性、
        全身性自身免疫性疾病。可发生于任何年龄，30-50岁为发病高峰。""",
        "symptoms": {
            "joint": ["关节疼痛", "肿胀", "晨僵（>1小时）", "对称性受累", "活动受限"],
            "systemic": ["疲劳", "低热", "体重减轻", "类风湿结节"],
            "extra_articular": ["肺部受累", "血管炎", "干燥综合征", "心脏受累"]
        },
        "causes": ["自身免疫反应", "遗传易感性", "环境因素"],
        "risk_factors": {
            "modifiable": ["吸烟", "感染", "激素因素"],
            "non_modifiable": ["女性", "家族史", "HLA-DR4基因型"]
        },
        "treatments": {
            "DMARDs": ["甲氨蝶呤（一线药物）", "来氟米特", "羟氯喹", "柳氮磺吡啶"],
            "biologics": ["TNF抑制剂", "IL-6受体拮抗剂", "CTLA4-Ig", "JAK抑制剂"],
            "symptomatic": ["NSAIDs", "糖皮质激素（桥接治疗）"],
            "adjunctive": ["物理治疗", "职业治疗", "关节保护", "患者教育"]
        },
        "complications": ["关节畸形", "残疾", "心血管疾病", "骨质疏松", "感染风险增加"],
        "prevention": ["早期诊断和治疗", "戒烟", "定期监测", "规范用药"],
        "sources": ["ACR/EULAR Guidelines", "中国类风湿关节炎诊治指南"]
    }
]

CKD_KNOWLEDGE = [
    {
        "name": "慢性肾病（CKD）",
        "category": DiseaseCategory.OTHER,
        "overview": """慢性肾病是指肾脏结构或功能异常持续超过3个月，
        表现为肾小球滤过率下降、蛋白尿或影像学异常。CKD可进展至终末期肾病。""",
        "symptoms": {
            "early": ["疲劳", "食欲减退", "夜尿增多", "轻度浮肿"],
            "progressive": ["水肿加重", "恶心呕吐", "皮肤瘙痒", "呼吸困难"],
            "advanced": ["严重贫血", "少尿或无尿", "意识改变", "心律失常"]
        },
        "causes": ["糖尿病肾病", "高血压肾损害", "肾小球肾炎", "多囊肾", "长期药物损伤"],
        "risk_factors": {
            "modifiable": ["血糖控制不佳", "血压控制不佳", "高盐饮食", "吸烟"],
            "non_modifiable": ["年龄增长", "家族史", "既往肾损伤"]
        },
        "diagnosis": {
            "labs": ["eGFR<60 ml/min/1.73m²持续≥3个月", "尿蛋白/尿白蛋白升高", "肌酐升高"],
            "imaging": ["肾脏超声提示肾脏萎缩或结构异常"],
            "staging": ["KDIGO分期：G1-G5结合A1-A3蛋白尿分级"]
        },
        "treatments": {
            "lifestyle": ["限盐饮食", "蛋白摄入适度控制", "戒烟", "规律运动"],
            "medications": ["ACE抑制剂/ARB", "SGLT2抑制剂（合并糖尿病）", "纠正贫血与电解质紊乱"],
            "renal_replacement": ["血液透析", "腹膜透析", "肾移植"]
        },
        "complications": ["贫血", "矿物质骨病", "心血管事件", "电解质紊乱"],
        "prevention": ["控制血糖和血压", "避免肾毒性药物", "定期筛查尿蛋白与肾功能"],
        "prognosis": "早期干预可延缓进展，晚期需肾替代治疗。",
        "sources": ["KDIGO Guidelines 2024", "中国慢性肾病管理指南"]
    }
]

DYSLIPIDEMIA_KNOWLEDGE = [
    {
        "name": "血脂异常",
        "category": DiseaseCategory.CARDIOVASCULAR,
        "overview": """血脂异常是指血浆胆固醇或甘油三酯水平异常升高，
        或高密度脂蛋白胆固醇降低，是动脉粥样硬化的重要危险因素。""",
        "symptoms": {
            "common": ["多数无症状"],
            "severe": ["黄色瘤", "脂血症性胰腺炎（极高甘油三酯）"]
        },
        "causes": ["遗传性高脂血症", "高脂饮食", "肥胖", "糖尿病", "甲状腺功能减退"],
        "risk_factors": {
            "modifiable": ["高脂饮食", "缺乏运动", "超重/肥胖", "吸烟"],
            "non_modifiable": ["家族史", "年龄增长"]
        },
        "diagnosis": {
            "labs": ["空腹血脂谱（TC, LDL-C, HDL-C, TG）"],
            "criteria": ["LDL-C升高或HDL-C降低", "TG升高≥1.7 mmol/L"],
            "risk": ["ASCVD风险评估决定治疗强度"]
        },
        "treatments": {
            "lifestyle": ["低饱和脂肪饮食", "增加膳食纤维", "规律有氧运动", "减重"],
            "medications": ["他汀类药物", "依折麦布", "PCSK9抑制剂", "贝特类（高TG）"]
        },
        "complications": ["动脉粥样硬化", "心肌梗死", "中风", "胰腺炎"],
        "prevention": ["健康饮食", "规律运动", "控制体重", "定期血脂检查"],
        "prognosis": "长期坚持生活方式干预与降脂治疗可显著降低心血管风险。",
        "sources": ["ESC/EAS Dyslipidemia Guidelines 2023", "中国血脂管理指南"]
    }
]

STROKE_KNOWLEDGE = [
    {
        "name": "脑卒中",
        "category": DiseaseCategory.NEUROLOGICAL,
        "overview": """脑卒中是由于脑血管阻塞或破裂导致局灶性神经功能缺损。
        包括缺血性脑卒中和出血性脑卒中，是成人致残和死亡的主要原因之一。""",
        "symptoms": {
            "common": ["突发偏侧无力或麻木", "言语不清", "口角歪斜", "视物模糊"],
            "severe": ["意识障碍", "剧烈头痛（出血性）", "吞咽困难"]
        },
        "causes": ["动脉粥样硬化", "心源性栓塞", "小血管病变", "高血压脑出血"],
        "risk_factors": {
            "modifiable": ["高血压", "糖尿病", "血脂异常", "吸烟", "房颤"],
            "non_modifiable": ["年龄增长", "家族史", "既往卒中史"]
        },
        "diagnosis": {
            "imaging": ["头颅CT/MRI确诊出血或缺血", "血管成像评估狭窄/闭塞"],
            "clinical": ["FAST评估", "NIHSS评分"]
        },
        "treatments": {
            "acute": ["静脉溶栓（时间窗内）", "取栓治疗", "控制血压和血糖"],
            "secondary": ["抗血小板/抗凝治疗", "他汀类药物", "危险因素管理"],
            "rehabilitation": ["早期康复训练", "吞咽与语言训练"]
        },
        "complications": ["偏瘫", "失语", "认知障碍", "抑郁", "肺部感染"],
        "prevention": ["控制血压血脂", "戒烟限酒", "规律运动", "抗凝或抗血小板治疗"],
        "prognosis": "早期识别与治疗可改善预后，长期康复有助于功能恢复。",
        "sources": ["AHA/ASA Stroke Guidelines 2024", "中国脑卒中防治指南"]
    }
]

ALL_KNOWLEDGE = (
    DIABETES_TYPE2_KNOWLEDGE + 
    HYPERTENSION_KNOWLEDGE + 
    ASTHMA_KNOWLEDGE + 
    HEART_DISEASE_KNOWLEDGE + 
    COPD_KNOWLEDGE + 
    ARTHRITIS_KNOWLEDGE +
    CKD_KNOWLEDGE +
    DYSLIPIDEMIA_KNOWLEDGE +
    STROKE_KNOWLEDGE
)

def get_sample_knowledge():
    """Get all sample knowledge documents"""
    return ALL_KNOWLEDGE

def create_disease_knowledge_objects():
    """Create DiseaseKnowledge objects from sample data"""
    knowledge_objects = []
    
    for data in ALL_KNOWLEDGE:
        from datetime import datetime
        import uuid
        
        knowledge = DiseaseKnowledge(
            disease_id=f"disease_{uuid.uuid4().hex[:8]}",
            name=data["name"],
            category=data["category"],
            overview=data["overview"],
            symptoms=data.get("symptoms", {}),
            causes=data.get("causes", []),
            risk_factors=data.get("risk_factors", {}),
            diagnosis=data.get("diagnosis", {}),
            treatments=data.get("treatments", {}),
            complications=data.get("complications", []),
            prevention=data.get("prevention", []),
            prognosis=data.get("prognosis"),
            sources=data.get("sources", []),
            last_updated=datetime.now()
        )
        knowledge_objects.append(knowledge)
    
    return knowledge_objects
