# Analysis 20 — RAG Corpus Content Plan

> Phase 01 Analysis — 2026-04-29
> Question: What goes in the proprietary RAG corpus? What format? How to build it pre-launch?

---

## 核心结论

RAG语料库不是一个"数据集"，而是一个**三层知识结构**：(1) 雇主指纹库（各公司的招聘偏好），(2) SG市场规则库（行业/职能特定规范），(3) 用户信号库（从用户行为中提取的回写模式）。每一层的来源、格式和构建顺序不同。Pre-launch可以完成第一二层的核心部分；第三层在上线后3-6个月积累。

---

## Part 1：RAG的技术架构（简要）

### 为什么RAG优于fine-tuning（已决定）

- Fine-tuning需要80K+信号才有统计意义（Year 3-4）
- RAG在任何数据量下都有效
- RAG内容更新不需要重新训练（随时更新）
- 新版Claude/GPT基础模型自动受益（不需要重新fine-tune）

### 技术实现

```
Query（用户的简历 + JD）
    ↓
Embedding（向量化查询）
    ↓
Vector Store检索（Pinecone / pgvector）
    ↓
相关语料块（Top-K results）
    ↓
LLM生成（Claude Sonnet + 检索到的SG上下文）
    ↓
建议输出
```

---

## Part 2：语料库三层结构

### 层1：雇主指纹库（Employer Fingerprints）

**内容**：各主要SG雇主的招聘偏好、语言偏好、文化关键词

**格式示例**：
```yaml
employer: DBS Bank
employer_type: GLC
size: large
industries: [banking, fintech]

hiring_preferences:
  language_style: formal, quantified results expected
  cultural_keywords: [innovation, customer obsession, transformation, resilience]
  avoid: [responsible for, managed, helped with]
  prefer: [led, delivered, drove, achieved]

resume_conventions:
  photo: not required for corporate roles
  format: reverse chronological, 2 pages max for PMET
  
role_specific_intel:
  technology: emphasis on cloud, data; AWS/Azure > GCP in their stack
  risk_compliance: mention MAS framework awareness
  operations: Six Sigma, process improvement language valued
  
interview_intel:  [populated later from user outcomes]
  typical_rounds: 3
  assessment_centre: used for analyst/associate level
```

**pre-launch建设方法**：
1. **招聘顾问访谈**（模型B from Analysis 15）：5-10名在DBS/GovTech/Accenture等主要雇主有placement经验的SG猎头，各付SGD 100-200访谈费，系统性提取他们对每家公司的招聘偏好认知
2. **公开信息分析**：每家公司最近发布的50-100个JD的语言模式分析（关键词频率、技能要求变化）
3. **Glassdoor/LinkedIn面试评论**（公开内容）：主要雇主面试问题类型汇总

**目标雇主清单（初期50家）**：

| 类别 | 目标雇主 |
|-----|---------|
| 银行 | DBS、OCBC、UOB、Standard Chartered、Citi |
| 政府 | GovTech、MOF、MAS、CPF、HDB |
| GLC | Singtel、CapitaLand、Sembcorp、SMRT、ST Engineering |
| 科技MNC | Google、Meta、Grab、Sea Group、Shopee |
| 咨询 | McKinsey、BCG、Deloitte、EY、Accenture |
| 金融科技 | Stripe、Wise、Revolut（SG）|

---

### 层2：SG市场规则库（Market Intelligence Rules）

**内容**：不依赖特定雇主的SG市场规范、行业规则、文化解码

**格式示例**：
```yaml
rule_id: SG-NS-001
category: national_service
applies_to: [male_graduates, male_PMET]

rule: NS vocation descriptions must be translated to civilian-equivalent competencies
bad_example: "Served as Signal Officer in 3rd Signal Battalion"
good_example: "Led 12-person communications team managing critical infrastructure for 2,000-person organization"

rationale: Hiring managers outside NS context don't understand military vocations

rule_id: SG-PHOTO-GLC-001
category: photo_guidance
applies_to: [all_candidates, GLC_applications]

rule: Professional headshot recommended for GLC and statutory board applications
evidence: GLC HR practice; face recognition in HRIS systems
exception: Applications via MCF platform (system may not support photos)

rule_id: SG-PMET-AGE-001
category: age_neutral_language
applies_to: [PMET, 10+years_experience]

rule: Remove implicit age signals — graduation years, "early career" job descriptions
example_to_flag: "2001 Graduate, NUS Business" → "NUS Business (Hons)"
example_to_flag: "Junior Analyst" → "Analyst"
rationale: SG Fair Consideration Framework; implicit age discrimination common
```

**pre-launch建设方法**：
1. **招聘顾问访谈**（同上）：系统性提取SG市场特有规则（目标：200条规则）
2. **MOM Fair Consideration Framework文档**：政府发布，公开可用
3. **新闻/HR行业报告**：HR In Asia、Singapore Management Review中的HR insights
4. **NUS/NTU Career Centre指南**：公开发布的简历/面试指导（SG学生受众）
5. **NTUC/e2i公开资源**：政府委托的职业指导内容

**目标规则数量（pre-launch）**：
- 国家服务（NS）规则：20条
- 照片指导（按雇主类型）：10条
- 年龄中性语言规则：30条
- 行业特定词汇规则（金融/科技/法律/政府）：80条
- GLC/政府组织文化规则：40条
- PMET职业转换框架：20条

**总计目标：200条经验证的SG市场规则**

---

### 层3：用户信号库（User Preference Signals）

**内容**：从实际用户的Accept/Reject/Modify行为中提取的偏好模式

**这是上线后积累的内容，pre-launch无法构建**

**格式**（会随产品使用自动生成）：
```yaml
signal_pattern:
  context: {company_type: GLC, role_level: mid, industry: banking}
  suggestion_type: quantification
  original: "Responsible for managing team"
  suggested: "Led 8-person cross-functional team, improving report turnaround by 30%"
  outcome: accepted (88% acceptance rate in this context)
  
signal_pattern:
  context: {company_type: startup, role_level: senior, industry: fintech}
  suggestion_type: leadership_framing
  original: "Managed 3 direct reports"  
  suggested: "Grew and mentored 3-person engineering team"
  outcome: modified (users changed "Grew" to "Built" in 60% of cases)
  → Learning: "Built" beats "Grew" for startup senior roles
```

**Month 6时的预计信号量**：
- 5,000活跃用户 × 5个JD × 平均8条建议 × 50%会有交互 = 100,000个信号
- 按照3-6%的outcome记录率，关联outcome的信号约3,000-6,000条
- 这已经是有意义的SG偏好数据集起点

---

## Part 3：Pre-Launch建设工作流

### 阶段1：基础建设（产品开发期间）

**Week 1-4**：雇主指纹和市场规则的骨架

工作：
1. 设计YAML schema（雇主指纹格式、规则格式）
2. 识别目标50家雇主
3. 分析每家公司最近50个JD（自动化：Python脚本批量解析）
4. 提取关键词频率、技能要求、语言模式

输出：50家雇主的基础指纹草稿（需要招聘顾问验证）

**Week 5-8**：招聘顾问访谈

工作：
1. 招募5-10名有SG大型雇主placement经验的招聘顾问（Design Partner模型B）
2. 结构化访谈（每次1.5小时，SGD 100-200补偿）
3. 问题清单：
   - "DBS的简历什么样的最容易通过初筛？"
   - "哪些GLC会看照片，哪些不看？"
   - "MAS审计岗面试官最看重什么？"
   - "什么样的NS描述方式最受欢迎？"
4. 将访谈笔记编码成规则和指纹

输出：
- 验证/修正雇主指纹（50家）
- 200条SG市场规则（按类别结构化）
- 识别5-10家适合Design Partner Cohort的机构

---

### 阶段2：Design Partner数据（上线前1-2个月）

**目标**：50-100名有完整同意授权的真实用户，产生高质量信号

工作：
1. 通过招聘机构渠道和校友网络招募50名积极求职者
2. 每人获得：
   - 免费Pro账号（6个月）
   - 1对1简历反馈（创始人亲自）
   - 结果跟踪激励（callback率对比）
3. 用户产生：
   - 上传简历 + 分析至少5个JD
   - 记录申请结果（由于是design partner，记录率预计30-40%）

预期产出（50个用户 × 5个JD × 8条建议 × 80%交互率）：
- 1,600个建议信号
- 与outcome关联：50 × 5 × 35% = 87个结果记录

这是产品上线时的基础数据层。

---

### 阶段3：上线后的持续积累

**Month 1-3**：
- 建议信号每月积累约10,000-20,000条（100个活跃Pro用户）
- Outcome记录约150-400条/月（15-22%记录率目标）
- 每月一次语料库更新（自动化pipeline）

**Month 6**：首次回顾
- 信号量约100,000条
- 识别最高价值的雇主（信号密度最高的前10家）
- 开始构建这10家的深度指纹

---

## Part 4：语料库维护和更新

### 内容时效性

| 内容类型 | 更新频率 | 触发更新的事件 |
|---------|---------|--------------|
| 雇主指纹 | 季度 | 大裁员/扩招、C-suite更换、战略调整 |
| 市场规则 | 年度 | MOM政策变化、Fair Consideration Framework更新 |
| 用户信号 | 持续 | 自动Pipeline（每次用户交互） |

### 自动化程度

- 用户信号：100%自动（产品功能的一部分）
- 雇主指纹更新：半自动（新JD自动解析；解读仍需人工确认）
- 市场规则：手动（需要领域专家判断）

---

## 诚实评估

| 维度 | 评估 |
|-----|-----|
| Pre-launch语料库质量 | 有价值但有限——50家雇主指纹 + 200条规则是好的起点，不是壁垒 |
| 壁垒形成时间 | Month 18-30（100,000+信号 + 5,000+outcomes）|
| 最大风险 | 招聘顾问访谈质量参差不齐——5-10次访谈的结论需要交叉验证 |
| 自动化可行性 | 信号收集完全自动化；指纹维护需要半自动 |
| 与竞品的时间差 | 竞品可以在60-90天内复制静态规则；无法复制累积的用户信号 |

