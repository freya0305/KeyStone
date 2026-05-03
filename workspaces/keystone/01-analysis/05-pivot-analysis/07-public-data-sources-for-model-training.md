# 新加坡公开数据源：可用于模型训练

**日期**：2026-05-04
**目的**：为JD生成模型提供训练数据

---

## 一、新加坡政府开放数据平台 (data.gov.sg)

### 1.1 核心数据集

| 数据集 | 内容 | 格式 | 可用性 | 训练价值 |
|--------|------|------|--------|---------|
| **职位空缺数据** | 行业/职业分类、需求数量 | CSV, JSON | ✅ 免费注册下载 | ⭐⭐⭐ |
| **劳动力市场数据** | 就业率、薪资中位数、行业分布 | CSV, API | ✅ 免费 | ⭐⭐⭐ |
| **职业分类 (SSOC)** | 新加坡标准职业分类代码 | CSV | ✅ 免费 | ⭐⭐⭐⭐ |
| **技能框架 (SFw)** | 各职位技能要求、能力标准 | CSV, PDF | ✅ 免费 | ⭐⭐⭐⭐⭐ |

### 1.2 SkillsFuture 技能框架 (SFw)

```
包含内容：
- 700+ 职业路径
- 每个职业的：
  - 关键技能
  - 工作任务描述
  - 能力标准
  - 培训路径

训练价值：
- 直接可用于训练"技能要求"理解
- 标准化职业分类
- 新加坡市场特定的技能需求
```

### 1.3 MOM (劳动力部) 数据

| 数据集 | 内容 | 频率 | 训练价值 |
|--------|------|------|---------|
| **Labour Market Outlook** | 年度劳动力需求预测 | 年度 | ⭐⭐⭐ |
| **Employment Statistics** | 按行业/职业分类就业数据 | 季度 | ⭐⭐⭐ |
| **Foreign Worker Data** | 外籍劳动力统计 | 季度 | ⭐⭐ |

---

## 二、招聘平台公开数据

### 2.1 MyCareersFuture.sg

```
情况：
- 政府运营的招聘平台
- 部分数据公开可用

可用数据：
1. 公开职位列表（可爬取，需遵守T&C）
2. 职位描述（经用户同意后公开）
3. 公司信息（公开）

限制：
- 薪资数据部分公开
- 需申请数据访问权限

建议：联系MCF申请研究合作
```

### 2.2 LinkedIn Singapore (公开信息)

```
可收集的公开信息：
1. LinkedIn Salary (新加坡市场数据)
2. LinkedIn Jobs (职位发布数据)
3. 技能趋势报告 (LinkedIn Economic Graph)

来源：
- LinkedIn Singapore官方报告
- LinkedIn Talent Blog

注意：
- 需遵守LinkedIn爬虫政策
- 不可大规模爬取
- 报告可直接引用
```

### 2.3 Indeed Singapore

```
可用：
- 职位描述（公开可见）
- 薪资范围（用户自愿提供）

方式：
- 单独职位页面可访问
- 薪资估算工具可用

限制：大规模数据需付费API
```

---

## 三、猎头公司公开报告

### 3.1 年度薪资指南 (免费PDF)

| 来源 | 覆盖 | 更新频率 | 可用于训练 |
|------|------|---------|-----------|
| **Robert Walters Salary Survey** | Tech, Finance, Sales等 | 年度(Q1) | ✅ 薪资数据 |
| **Michael Page Salary Guide** | 全行业 | 年度 | ✅ 职位需求 |
| **Robert Half Asia Salary Guide** | Tech, Finance | 年度 | ✅ 薪资趋势 |
| **Adecco Singapore** | 全行业 | 年度 | ✅ |
| **Page Personnel** | 专业职能 | 年度 | ✅ |

### 3.2 报告内容（可用于训练）

```
每个报告通常包含：
- 各职位薪资范围（低/中/高）
- 按经验级别分类
- 按行业/公司类型分类
- 市场趋势分析
- 热门技能需求

训练价值：
- 薪资数据 → LLM学习"合理薪资范围"
- JD模式 → 学习JD结构
- 技能描述 → 学习如何描述技能要求
```

---

## 四、国际公开数据集

### 4.1 Kaggle/HuggingFace

| 数据集 | 内容 | 规模 | 新加坡相关 |
|--------|------|------|-----------|
| **Job Posting Dataset** | 全球职位描述 | 百万级 | ⚠️ 少量SG |
| **Resume/CV Dataset** | 简历数据 | 十万级 | ⚠️ |
| **LinkedIn Jobs Dataset** | 全球职位 | 百万级 | ⚠️ |

### 4.2 O*NET (美国职业数据库)

```
可用性：完全免费

内容：
- 1200+ 职业的详细描述
- 技能要求 (KSAO)
- 任务描述
- 工作活动

训练价值：
- 职业分类体系可迁移
- JD结构模式
- 技能词汇标准化

网址：onetcenter.org
```

### 4.3 ESCO (欧洲技能/职业分类)

```
可用性：免费API

内容：
- 3000+ 职业
- 14000+ 技能标签
- 多语言版本（含英文）

训练价值：
- 技能标准化
- 跨语言迁移
- JD关键词提取

网址：ec.europa.eu/esco
```

---

## 五、数据收集建议（分阶段）

### Phase 1: Day 1 可用数据

```
优先级排序（立即可收集）：

1. ✅ SkillsFuture 技能框架
   - 来源：wsg.gov.sg / skillsfuture.gov.sg
   - 内容：职业路径 + 技能要求
   - 格式：CSV下载
   - 训练方式：直接用于训练"技能识别"

2. ✅ MOM Labour Market Statistics
   - 来源：mom.gov.sg
   - 内容：行业就业数据
   - 格式：PDF + CSV

3. ✅ SSOC 职业分类
   - 来源：mom.gov.sg
   - 内容：标准职业代码
   - 格式：CSV

4. ✅ Robert Walters Salary Guide 2025/2026
   - 来源：robertwalters.com (免费PDF)
   - 内容：各职位薪资范围
   - 训练方式：LLM提取结构化数据
```

### Phase 2: 1-2个月内收集

```
5. ✅ LinkedIn Singapore 技能报告
   - 来源：linkedin.com/singapore
   - 内容：年度技能趋势

6. ✅ O*NET 职业数据
   - 来源：onetcenter.org
   - 内容：职业描述 + 技能要求
   - 格式：REST API

7. ✅ ESCO 技能分类
   - 来源：ec.europa.eu/esco
   - 格式：API
```

### Phase 3: 3-6个月

```
8. ⚠️ MyCareersFuture 数据合作
   - 联系MCF申请研究数据访问
   - 可能需要：
     - 研究目的说明
     - 数据安全承诺
     - 脱敏处理协议

9. ⚠️ 爬虫收集公开JD
   - 仅限公开可见职位
   - 遵守robots.txt
   - 仅用于研究目的
```

---

## 六、训练数据格式建议

### 6.1 JD训练数据格式

```json
{
  "job_title": "Senior Software Engineer",
  "company_type": "Tech Startup",
  "industry": "Fintech",
  "required_skills": ["Python", "AWS", "Docker"],
  "experience_level": "5+ years",
  "responsibilities": ["...", "..."],
  "requirements": ["...", "..."],
  "benefits": ["...", "..."],
  "salary_range": {
    "low": 10000,
    "high": 15000,
    "currency": "SGD"
  },
  "source": "mycareersfuture/linkedin/company_website",
  "collected_date": "2026-01-15"
}
```

### 6.2 技能-职位映射

```json
{
  "occupation": "Software Engineer",
  "ssoc_code": "2512.1",
  "essential_skills": ["Programming", "Problem Solving", "System Design"],
  "preferred_skills": ["Cloud", "Agile", "CI/CD"],
  "certifications": ["AWS Solutions Architect", "Google Cloud"],
  "experience_years": "3-5"
}
```

---

## 七、法律合规注意事项

```
1. data.gov.sg 数据
   ✅ 政府开放数据，可自由使用
   ✅ 需注明来源

2. 猎头公司报告
   ✅ 公开PDF，可用于分析
   ✅ 不可直接复制原文商业使用

3. 爬虫收集
   ⚠️ 遵守robots.txt
   ⚠️ 仅收集公开可见数据
   ⚠️ 考虑申请正式数据合作

4. MyCareersFuture
   ⚠️ 用户协议限制数据使用
   ✅ 建议正式申请研究合作

5. 个人隐私
   ⚠️ JD中如有个人信息需脱敏
   ⚠️ 不可收集可识别个人的信息
```

---

## 八、数据准备 Pipeline

```
Day 1 数据准备流程：

1. 下载 SkillsFuture SFw 数据
   → 存储为: data/sfw/skills_framework.csv

2. 下载 MOM SSOC 分类
   → 存储为: data/mom/ssoc_classification.csv

3. 下载 MOM Labour Market Statistics
   → 存储为: data/mom/labour_stats.csv

4. 提取 Robert Walters Salary Guide PDF
   → 存储为: data/salary/robert_walters_2026.json

5. 获取 O*NET API 数据
   → 存储为: data/onet/occupations.json

6. 获取 ESCO API 数据
   → 存储为: data/esco/skills.json

预期数据量：
- 技能框架：700+ 职业路径
- 职业分类：5000+ SSOC代码
- 薪资数据：100+ 常见职位
- 技能标签：14000+ ESCO技能
```

---

## 九、结论

### Day 1 可用训练数据

| 数据源 | 数据量 | 难度 | 立即可用 |
|--------|--------|------|---------|
| SkillsFuture SFw | 700+职业 | 低 | ✅ |
| MOM SSOC | 5000+代码 | 低 | ✅ |
| MOM Labour Stats | 行业级 | 低 | ✅ |
| Robert Walters Guide | 100+职位 | 中 | ✅ |
| O*NET | 1200+职业 | 低 | ✅ |
| ESCO | 14000+技能 | 低 | ✅ |

**不需要爬虫或付费数据，Day 1 就可以开始训练！**

---

*数据收集建议完成。Day 1 可从政府开放数据和猎头报告开始。*
