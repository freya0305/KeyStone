# Analysis 22 — Product Metrics Framework

> Phase 01 Analysis — 2026-04-29
> Question: What are the leading indicators before revenue? How do we define "working"?

---

## 核心结论

在没有足够收入数据的早期，领先指标比滞后指标（MRR）更重要。KeyStone有三类核心指标：(1) 激活质量指标（用户是否真正体验到价值），(2) 数据飞轮指标（数据资产是否在积累），(3) 商业健康指标（产品是否向可持续方向发展）。所有指标必须在MVP Day 1就开始收集。

---

## Part 1：指标框架全图

### 北极星指标（North Star Metric）

**定义**：每月有效激活用户数（Monthly Active Activated Users，MAAU）

**激活的精确定义**：在过去30天内完成至少1次完整工作流——上传简历 + 分析JD + 接受至少1条建议。

**为什么选这个**：
- 比MAU更有质量门槛（阻止"僵尸注册"稀释数据）
- 比MRR更早出现（注册后几天就可以测量）
- 与数据积累直接相关（激活用户=产生了建议信号）
- 与付费转化相关性高（激活用户的付费率是非激活的5-8x）

---

## Part 2：三层指标体系

### 层1：激活质量指标（用户价值层）

**L1.1 首次激活率**
- 定义：注册用户中完成"完整工作流"的比例
- 目标：>35%（Month 1），>45%（Month 6）
- 测量：注册事件 vs 首次suggestion_accept事件的session分析
- 异常阈值：<20%说明激活流程有严重问题

**L1.2 Aha指数**（自创指标）
- 定义：首次会话中接受建议数量的中位数
- 目标：≥2条建议被接受（首次session）
- 为什么：接受≥2条的用户7天留存率比接受0条高4x

**L1.3 建议质量评分**
- 定义：被接受（不修改直接accept）的建议占所有交互建议的比例
- 目标：>40%直接接受；<20%被拒绝；40%被修改
- 为什么：高拒绝率说明建议质量差；高直接接受率可能说明建议太保守

**L1.4 回报率**
- 定义：7日内回来分析第2个JD的用户比例
- 目标：>40%（激活用户）
- 为什么：真正解决问题的工具用户会重复使用

---

### 层2：数据飞轮指标（数据资产层）

**L2.1 信号积累速率**
- 定义：每周新增建议信号数（accept/reject/modify事件）
- 目标：Week 4 = 500+信号；Month 3 = 5,000+信号
- 测量：`suggestion_signals`表的insert rate

**L2.2 申请记录率**（关键）
- 定义：生成简历修改（下载）的用户中，记录申请状态更新的比例
- 基线：3-6%（Teal/LinkedIn基准）
- 目标（有邮件提醒后）：15-22%
- 重要性：直接影响数据飞轮的outcome信号密度

**L2.3 Stage progression记录率**
- 定义：已记录response的申请中，继续记录后续面试轮次的比例
- 目标：>60%（用户既然记录了第一步，应该坚持记录）
- 为什么：多轮面试数据比单一"回复"数据价值高10x

**L2.4 雇主覆盖深度**
- 定义：有≥5个信号的雇主数量
- 目标：Month 6 = 20家雇主；Month 12 = 50家雇主
- 为什么：这是RAG语料库"雇主指纹"的统计基础

---

### 层3：商业健康指标（可持续层）

**L3.1 免费→Pro转化率**
- 定义：注册用户在30天内升级Pro的比例
- 目标：4-6%（Month 3+，有足够的免费用户基数后）
- 基线期（Month 1-2）：不把这个作为主要优化目标（样本量太小）

**L3.2 Pro 30日留存率**
- 定义：付费用户在订阅后30天内至少使用1次的比例
- 目标：>70%
- 为什么：留存率低说明产品价值没有覆盖整个求职周期

**L3.3 Pro 90日留存率**
- 定义：付费用户在订阅后90天内仍然活跃（每月至少1次会话）的比例
- 目标：>45%
- 为什么：求职周期通常8-12周，90日留存=用户整个求职期间都在用

**L3.4 NPS（净推荐值）**
- 定义：标准NPS问题（0-10分，推荐给朋友的可能性）
- 目标：>40（好）；>60（优秀）
- 测量时机：用户完成第一个JD分析后30分钟 + 订阅满30天

**L3.5 B2B Pipeline健康度**（非产品指标，但同样重要）
- 定义：与大学/机构的对话处于各阶段的数量
- 目标：Month 3 = 3个大学对话；Month 6 = 1个试点合同意向

---

## Part 3：早期阶段指标仪表板

### 每日需要查看（创始人仪表板）

```
Today:
  New signups: __
  Activated users (completed workflow): __ (__% of signups)
  Suggestions shown / accepted / rejected / modified: __ / __ / __ / __
  Pro upgrades: __
  
This week:
  New signals in suggestion_signals table: __
  Applications tracked with email reminders sent: __
  Stage updates recorded: __
```

### 每周需要查看

```
Weekly Cohort:
  Cohort [week X]: N users
  7-day activation rate: __%
  7-day return rate (2nd JD analysis): __%
  
Data Flywheel:
  Total signals: __
  Employers with 5+ signals: __ / target 20 by Month 6
  Outcome records this week: __
  
Health:
  Pro conversion (rolling 30-day): __%
  Email open rate (reminder emails): __%
  Email deep-link click rate: __%
```

---

## Part 4：警告阈值（需要立即行动）

| 指标 | 警告阈值 | 可能原因 |
|-----|---------|---------|
| 首次激活率 | <20% | 流程太长/建议质量差/上传失败 |
| 建议拒绝率 | >35% | 建议不够SG化/太generic |
| 7日回访率 | <25% | 没有解决真正问题/产品bug |
| Pro转化率 | <2% (Month 3+) | 免费tier给太多/定价错误/价值不清晰 |
| 邮件打开率 | <20% | 邮件进垃圾箱/主题行差 |
| 申请记录率 | <8% (有邮件提醒后) | 邮件提醒没效果/deep link坏了 |

---

## Part 5：指标收集技术要求（MVP Day 1）

### 必须从Day 1收集的事件

```javascript
// 激活漏斗
analytics.track('resume_uploaded', {user_id, file_type, size_kb})
analytics.track('jd_submitted', {user_id, source: 'url'|'text', company_type, role_level})
analytics.track('analysis_completed', {user_id, processing_time_ms, match_levels: {strong, transferable, addressable, fundamental}})
analytics.track('suggestion_interacted', {user_id, suggestion_id, action: 'accepted'|'rejected'|'modified', company_type, role_level, industry})

// 数据飞轮
analytics.track('application_created', {user_id, job_id, source: 'resume_download'|'manual'})
analytics.track('stage_updated', {user_id, application_id, stage_type, round_number, outcome})
analytics.track('email_reminder_sent', {application_id, day: 3|10|21})
analytics.track('email_reminder_clicked', {application_id, update_completed: true|false})

// 商业
analytics.track('pro_upgrade', {user_id, plan: 'monthly'|'annual', trigger_point})
analytics.track('nps_survey_submitted', {user_id, score, context: 'post_first_jd'|'day_30_pro'})
```

### 推荐工具（低成本）

- **PostHog**（开源，self-hosted可以）：事件分析、漏斗分析、会话录制 — 免费tier适合早期
- **Mixpanel**（付费但成熟）：用户行为分析，适合Month 3后
- 简单替代：Supabase + 自建分析dashboard（最低成本）

---

## Part 6：指标和决策的连接

| 如果指标显示... | 决定... |
|--------------|--------|
| 建议拒绝率>35% | 暂停增长，专注提升建议质量 |
| 7日回访率<25% | 优先修复，延迟B2B销售 |
| 申请记录率<8%(有提醒后) | 检查邮件deliverability + deep link |
| Pro转化率>8% | 考虑提高定价或减少免费tier |
| B2B大学对话0个（Month 3后）| 改变B2B获客策略 |
| NPS>60 | 可以开始投入更多B2C获客 |

