# Analysis 19 — Legal Risk Analysis (SG)

> Phase 01 Analysis — 2026-04-29
> Question: What are the material legal risks? Employment Agencies Act? JD copyright?

---

## 核心结论

KeyStone面临**3个值得认真对待的法律风险**：(1) Employment Agencies Act申请是否构成"职业介绍"，(2) JD内容版权问题，(3) PDPA数据使用同意结构。其中只有PDPA风险需要在MVP前解决；EAA风险概率很低但需要律师意见确认；JD版权风险通过合理使用框架可以管理。

---

## Part 1：Employment Agencies Act (EAA) — 核心风险评估

### 什么是EAA

新加坡就业中介法（Employment Agencies Act, Cap. 92A）规定：任何从事"就业中介服务"的实体必须持有MOM颁发的就业中介牌照（Employment Agency Licence）。

**就业中介服务的法律定义**：
> "negotiating, procuring, or promising employment for or providing employment information to job seekers for a fee"

### KeyStone的行为是否落入此定义？

| 行为 | 分析 | 结论 |
|-----|-----|-----|
| 提供简历改写建议 | 工具服务，非中介行为 | ✅ 不在EAA范围 |
| 分析JD匹配度 | 分析工具，非介绍职位 | ✅ 不在EAA范围 |
| 提供面试准备 | 培训类服务，非中介 | ✅ 不在EAA范围 |
| 追踪申请结果 | 用户自用工具 | ✅ 不在EAA范围 |
| 向用户推荐"你应该申请这家公司"（未来功能）| 主动推荐可能被视为信息中介 | ⚠️ 需律师意见 |
| 向企业推荐候选人 | 明确是中介行为 | ❌ 需要牌照 |

### 关键区分

EAA针对的是**撮合雇主和求职者的中介行为**，而非：
- 求职工具/软件（如Word、LinkedIn Builder）
- 职业培训/辅导服务
- 自助式简历优化平台

**最相近的类比**：Jobscan（美国公司）在SG运营多年，提供JD匹配分析，无就业中介牌照。LinkedIn简历优化建议功能在SG运营无牌照。

### 风险概率评估

**低风险（P<10%）**：MOM对KeyStone这类AI写作辅助工具进行EAA执法。

**需要律师意见的触发条件**：
1. 产品加入主动职位推荐功能（"你应该申请这家公司"）
2. 产品向企业端销售候选人匹配服务
3. 产品代表用户代投简历

**建议**：在MVP前获取一份律师意见函（约SGD 500-1,500），确认当前产品形态不需要EAA牌照。这是一次性成本，提供保障和投资人信心。

---

## Part 2：JD内容版权 — 实际风险评估

### 版权归属问题

SG版权法（Copyright Act 2021）对原创文学作品提供保护。JD是否构成受保护作品？

**分析**：
- 标准化的技术要求列表（"5+ years experience in Java"）— 不构成原创作品，版权保护弱
- 精心撰写的公司文化描述、独特的角色说明 — 可能受版权保护
- 实践中：Jobscan、LinkedIn、Indeed多年来都在解析/展示JD，无版权诉讼记录

### KeyStone的行为

KeyStone对JD的使用：
1. 用户粘贴或提交JD URL（用户主动行为）
2. 系统解析JD用于分析
3. 不公开存储或展示JD原文给第三方
4. 仅用于为该用户生成个性化建议

### Fair Dealing框架（SG版权法第39-49条）

以下使用通常构成fair dealing：
- 研究或私人学习目的
- 评论或批评目的
- 报道当前事件

KeyStone的使用最接近"私人学习"目的（帮助个人用户理解JD要求）。实质上是用户的工具，而非内容再分发平台。

### 实际风险

**极低风险（P<2%）**：版权持有人（雇主/招聘平台）因JD解析起诉KeyStone。

原因：
1. 解析JD用于求职者个人使用是公认做法（所有主流工具都这么做）
2. 雇主发布JD的目的就是让求职者阅读和分析
3. 没有规模性公开再发布行为
4. 全球无此类案例记录

**需要法律关注的情况**：
- 如果KeyStone建立JD内容数据库并向第三方商业授权 — 不在当前计划中

**建议**：在ToS中加入标准的DMCA/版权条款。不需要专门的版权法律意见。

---

## Part 3：PDPA — 必须在MVP前解决

### 三个核心PDPA问题

**问题1：训练同意 vs 服务同意**

必须区分两个同意：
- **服务同意**：处理用户数据以提供KeyStone服务（必须）
- **训练同意**：使用用户信号（Accept/Reject）训练AI模型（单独opt-in）

当前spec已有此分离。**MVP前必须**：
- ToS和隐私政策明确写清楚两种同意的区别
- 注册流程有独立的训练同意checkbox
- B2B（大学）合同中写明"学生数据仅用于聚合dashboard，不用于AI训练"

**问题2：数据跨境传输**

LLM API调用会将用户简历内容传输到美国（Anthropic/OpenAI服务器）。PDPA对此的要求：

- 数据传输到SG认可的"comparable protection"国家/地区
- 或与数据接收方签订数据传输协议（Data Transfer Agreement）

**实际影响**：大多数SG SaaS都这样做。关键是ToS/隐私政策中披露"我们使用AI提供商（Anthropic、OpenAI），您的数据可能在SG以外处理"。

**问题3：简历中的个人数据**

简历包含高度个人化数据（NRIC、地址、出生年份等）。PDPA要求：
- 数据最小化（只收集必要数据）
- NRIC数据：系统建议用户删除NRIC，本身不存储NRIC值
- 保留期限：用户删除账号后X天内清除数据（ToS中定义）

---

## Part 4：其他需关注的法律问题

### 消费者保护（Fair Trading）法

关键要求：不能有误导性宣传。

**直接影响**：
- 不能宣称"提高X%回复率"（直到数据支撑前）
- 不能说"calibrated on SG hiring manager behaviour"（红队已标记）
- 可以说"built for the Singapore job market"、"SG-specific intelligence"

### 数据泄露通知要求

PDPA 2021年修订后引入数据泄露通知义务：
- 严重泄露：24小时内通知PDPC（电话/系统提醒）
- 轻微泄露：30天内书面通知PDPC

**MVP要求**：
- 基础事件日志（谁访问了什么数据）
- 备案联系人信息（DPO — 初期创始人自任）

---

## Part 5：建议行动清单

### MVP前必须（M0）

| 行动 | 成本 | 优先级 |
|-----|-----|------|
| 起草隐私政策（含PDPA合规条款、跨境传输披露）| SGD 800-2,000（律师）或使用模板 | P0 |
| ToS中区分服务同意 vs 训练同意 | 含在隐私政策中 | P0 |
| B2B合同模板中写明"学生数据不用于AI训练" | SGD 500（律师审阅）| P0 |
| 获取EAA不适用的律师意见函 | SGD 500-1,500 | P1 |

### Phase 2前（M3-6）

| 行动 | 成本 | 说明 |
|-----|-----|-----|
| PDPC"Research Purpose"豁免申请（如果需要匿名化研究）| 行政时间 | 仅在需要时 |
| 邮件解析功能的PDPA评估（如果推进Phase 3功能）| SGD 1,000 | 仅在需要时 |

### 总结

**真正的法律风险只有一个**：PDPA合规，且主要是文件和流程问题，不是结构性障碍。EAA和版权风险被市场实践和产品形态证明为低风险。一次性律师费用SGD 2,000-4,000可覆盖所有主要风险。

