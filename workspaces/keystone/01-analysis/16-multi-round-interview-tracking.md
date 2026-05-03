# Analysis 16 — Multi-Round Interview Tracking

> Phase 01 Analysis — 2026-04-29
> Question: How should the product model multi-round interviews, and what does this mean for the data model, UX, and LTV?

---

## 核心结论

SG专业岗位普遍2-4轮面试。当前spec把"interview scheduled"当成单一终态事件是错误的。正确模型是：每一轮面试是一个独立的**stage transition event**，每次转变都有：日期、轮次、结果（通过/未通过/待定）。这一变化有三层影响：数据模型、面试准备模块触发逻辑、LTV估算。

---

## Part 1：SG市场面试轮次现状

### 各类雇主典型面试轮次

| 雇主类型 | 典型轮次 | 形式 |
|---------|---------|-----|
| 科技公司（初创）| 2-3轮 | HR筛选 → 技术 → Culture fit |
| 科技公司（大型MNC）| 3-5轮 | HR → 技术电话 → On-site → 高管 |
| GLC / 法定机构 | 3-4轮 | 笔试/评估中心 → 面板 → 高管 |
| 银行/金融 | 3-4轮 | HR → 业务 → 技术 → 高管 |
| 咨询公司 | 3-5轮 | 案例面试 × 2-3 → Partner面试 |
| SME | 1-2轮 | 老板直接面试 |
| 政府部门 | 2-3轮 | 结构化面板 × 2 |

**关键洞察**：SG目标用户中，约70%的professional岗位需要3轮以上。当前spec把整个面试过程压缩成一个事件，丢失了大量结构化信息。

---

## Part 2：修正后的申请漏斗模型

### 完整漏斗（7个阶段）

```
Level 0: Applied
    ↓
Level 1: Response received (any response — email/LinkedIn/phone call)
    ↓
Level 2: Phone / video screen (recruiter or HR, 15-30 min)
    ↓
Level 3: Interview Round 1 (technical / competency)
    ↓
Level 4: Interview Round N (可重复，最多记录到Round 5)
    ↓
Level 5: Final round / Assessment centre
    ↓
Level 6: Decision — Offer / Rejection / Withdrawn
```

### 数据模型要求

每个 `application_record` 应包含一个 `interview_stages` 数组：

```
application_record {
    id
    job_id (linked to JD)
    resume_version_id
    applied_date
    status: applied | responded | screening | interviewing | decided | withdrawn
    
    stages: [
        {
            stage_type: response | screening | interview | final | offer | rejection | withdrawal
            round_number: null | 1 | 2 | 3 | 4 | 5
            date
            format: phone | video | in-person | assessment_centre | panel | technical | case
            outcome: passed | failed | pending | withdrawn
            notes: (optional, free text)
        }
    ]
    
    final_outcome: no_response | rejected | offer_received | withdrawn
    offer_details: { salary_range, start_date } (optional, for market intelligence)
}
```

### 为什么不是简单的status枚举

当前spec用status枚举（No response / Callback received / Phone screen / Interview scheduled / Offer / Rejected / Withdrawn）。问题：
1. "Interview scheduled"无法区分Round 1还是Round 3
2. 无法计算per-stage通过率（Round 1→Round 2的通过率比整体回复率更有预测价值）
3. 无法分析"在哪个阶段最容易被淘汰"（对用户最有价值的洞察）

---

## Part 3：对面试准备模块的影响

### 当前spec的错误假设

> "Entry point: Triggered when user marks a job as 'callback received'"

这把所有准备工作放在第一次回复后。正确逻辑：

**每次进入新的面试轮次时，都应触发准备提示。**

### 修正后的触发逻辑

```
Stage transition → Interview Prep Prompt:

Response received → "准备好接下来的筛选电话了吗？[查看电话筛选指南]"
Phone screen → passed → "恭喜通过！Round 1 面试准备：[开始]"
Round 1 → passed → "进入Round 2！针对这家公司的深度准备：[开始]"
Final round → "最终面试准备 — 针对高管轮次：[开始]"
```

### 对Interview Prep模块内容的影响

不同轮次需要不同类型的准备：

| 轮次 | 典型内容 | KeyStone准备重点 |
|-----|---------|----------------|
| 电话筛选 | 背景介绍、基本资质确认 | 30秒电梯演讲、薪资期望准备 |
| Round 1 | 技术能力、行为问题 | STAR故事库、技术基础 |
| Round 2 | 深度技术/案例 | 案例框架、扩展STAR故事 |
| Final | 高管文化匹配、战略视角 | 公司战略理解、"为什么是你"叙事 |
| Assessment centre | 多种形式混合 | 分组练习、In-tray练习提示 |

---

## Part 4：LTV影响重估

### 旧估算（单次面试触发）

```
用户收到回复 → 触发1次面试准备 → 1-3个月额外使用
LTV延长：50-67%（对收到回复的用户）
```

### 新估算（多轮触发）

对收到最终offer的用户（经历4轮面试）：
- 触发面试准备：4次（每轮一次）
- 每次触发约1-2周的高频使用
- 总额外使用期：4-8周
- 相当于多1-2个月订阅期

**关键变化**：不是每个用户都经历4轮，但：
- 经历Round 2+的用户已经通过了公司的初步筛选，是高价值潜在雇员
- 这些用户的求职动机和工具使用率远高于"刚开始投简历"阶段
- 每次stage transition是一个自然的re-engagement时机

### 修正后的LTV估算

```
用户类型 | 平均面试轮次 | 额外订阅月数
Fresh grad | 1.5轮 | 0.8个月
PMET | 2.8轮 | 1.6个月
High-demand专业（金融/咨询）| 3.5轮 | 2.3个月

加权平均额外LTV延长：75-90%（vs 50-67%的旧估算）
```

---

## Part 5：Per-Stage通过率 — 比整体"回复率"更有价值的指标

### 用户视角

"我的回复率是8%"没有指导性。

"你的简历在初始回复率（8%）处于平均水平，但你在Round 1→Round 2的通过率（33%）显著低于拿到offer的用户（67%）——这说明你的简历能吸引面试，但面试表现需要提升"

这是用户愿意为之付费的洞察。

### 平台视角（数据价值）

Per-stage通过率数据是真正的差异化数据资产：
- 某公司Round 2通过率的基准数据
- 某行业/岗位层级在不同阶段的通过率分布
- 哪些简历改写策略与更高的Round 1通过率相关

这些数据没有竞争对手在SG市场积累。这就是数据壁垒的具体形态。

---

## Part 6：UX变化要求

### Stage Recording UI

不再是简单的下拉"改状态"，而是：

**快速记录模式**（主流）：
```
[申请的公司] 有新进展？
○ 收到回复  ○ 通过筛选  ○ 进入面试  ○ 拿到Offer  ○ 被拒绝
```

**详细记录模式**（可选展开）：
```
这是第几轮面试？ [1] [2] [3] [4+]
面试形式？ [电话] [视频] [现场] [评估中心]
结果如何？ [通过] [等待中] [未通过]
面试日期：[___]
```

### Dashboard变化

用户可见指标升级：

```
旧：回复率 8%（22次申请中2次回复）

新：
申请漏斗:
  投递 → 回复     8%  (2/22)   ↑ 市场平均5%
  回复 → 面试     100% (2/2)   ↑ 良好
  面试Round 1 → Round 2  50%   ≈ 市场平均
  Round 2 → Final       0%    ↓ 需改进
```

---

## 诚实评估

| 问题 | 评估 |
|-----|-----|
| 数据模型复杂度 | 中度增加——stages数组比单状态复杂，但不是技术障碍 |
| 用户填写意愿 | 风险——多轮填写要求更高摩擦；解决方案：每轮独立推送，不强制一次填完 |
| 数据积累速度 | 每个用户产生更多事件记录，数据质量提升 |
| Interview prep复杂度 | 需要per-round内容，工程量增加约30% |
| MVP必须包含 | Stage-aware tracking必须在MVP中（不能后加）；per-round prep可以在Phase 2实现 |

