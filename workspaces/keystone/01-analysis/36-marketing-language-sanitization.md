# Analysis 36 — Marketing Language Sanitization

**Date**: 2026-04-29
**Context**: Redteam H-9 identified "calibrated on SG hiring manager behaviour" as fraudulent at launch. User requested: remove fraudulent language, replace with factual verifiable statements.

---

## 核心结论

以下营销语言必须在发布前修正，否则构成虚假宣传：

| ❌ 不要说 | ✅ 改为 |
|---------|-------|
| "calibrated on SG hiring manager behaviour" | "built on outcome tracking infrastructure" |
| "backed by real SG hiring data" | "designed to collect outcome data from SG users" |
| "learns from which suggestions get callbacks" | "records which suggestions you accept, reject, or modify" |
| "proven to improve callback rates" | "tracks your application outcomes so you can see what works" |
| "SG's most comprehensive resume database" | "built by SG job seekers, for SG job seekers" |
| "AI trained on SG hiring patterns" | "AI suggestions informed by SG market rules" |
| "outcome-calibrated" | "outcome-tracking" |

---

## 问题所在

### 1. "Calibrated on SG hiring manager behaviour"

**为什么是欺诈**: Redteam正确指出，在0个结果数据时就宣传"校准于招聘经理行为"是虚假的。我们没有数据——还没有。我们有的是：SG市场规则、招聘顾问访谈编码的逻辑、以及建立数据收集基础设施的意图。

**事实**: 我们从零开始建立，目标是有一天能校准。

**修正**: "outcome-tracking infrastructure" — 准确描述我们实际在构建的东西。

### 2. "Backed by real SG hiring data"

**为什么是欺诈**: 如果我们在0个结果时就宣传"真实数据"，这是虚假声明。在100个结果时也算不上"数据"。

**事实**: 我们正在积累数据，但不是现在。

**修正**: "designed to collect outcome data" 或 "built by SG job seekers, for SG job seekers"

### 3. "Proven to improve callback rates"

**为什么是欺诈**: "proven"需要统计显著性。在我们有500+logged outcomes前，我们无法声称任何东西是"proven"的。

**事实**: 我们相信outcome tracking会帮助用户改进，但我们还没有证明。

**修正**: "tracks your application outcomes so you can see what works"

---

## 合规的营销语言框架

### Launch Day (0-6个月)

重点：诚实描述产品功能，不夸大数据积累。

**正确的说法**:
- "KeyStone helps you tailor your resume for each job you apply to"
- "Tracks every application from submit to decision"
- "Built with SG-specific resume rules: NS framing, GLC insights, NRIC guidance"
- "Your feedback helps us improve suggestions — you choose whether to share"
- "Designed to learn from SG job seekers' outcomes over time"

**在有100+ outcomes后可以加**:
- "100+ SG job seekers have tracked their applications with KeyStone"

**在有1,000+ outcomes后可以加**:
- "KeyStone users have tracked 1,000+ applications, helping us understand what works in the SG market"

### Month 6-12 (第一批有意义的模式出现)

**正确的说法**:
- "Early patterns show [X]% of KeyStone users who track their outcomes see [specific insight]"
- "Built on feedback from [N] SG job seekers"
- "Our most-accepted suggestion: [specific example]"

### Year 1+ (有统计显著数据后)

**正确的说法**:
- "Users who complete 3+ KeyStone analyses have [X]% higher callback rate than those who don't" (需要p<0.05)
- "Calibrated on [N] verified SG application outcomes"
- "The first outcome-calibrated resume tool for Singapore"

---

## 具体文案修正

### Homepage/Tagline

| 位置 | ❌ 不要用 | ✅ 改为 |
|------|---------|-------|
| 主标题 | "The AI built for SG hiring managers" | "Per-job resume tailoring, calibrated on your outcomes" |
| 副标题 | "Backed by real SG hiring data" | "Tracks every application so you know what works" |
| Feature 1 | "Learns from callbacks" | "Records which suggestions lead to interviews" |
| Feature 2 | "SG's most accurate matching" | "SG-specific: NS framing, GLC analysis, NRIC masking" |
| Social proof | "Trusted by X SG job seekers" | "[X] job seekers tracking their applications" |

### B2B Pitch Deck

| 场景 | ❌ 不要说 | ✅ 改为 |
|------|---------|-------|
| 痛点 | "We calibrate on real hiring outcomes" | "We track outcomes so you can see what actually works" |
| 差异化 | "Our AI learns from your students' outcomes" | "Students track their own outcomes — anonymised data shows patterns" |
| 数据主张 | "Proven: students with higher KeyStone scores get more callbacks" | "Early signal: students who complete 3+ analyses have [X]% higher callback rate" (only if statistically valid) |
| 差异化vs VMock | "We're calibrated on real outcomes, VMock isn't" | "We track outcomes; VMock tracks ATS pass rates — different metrics" |

### App内提示文案

| 场景 | ❌ 不要说 | ✅ 改为 |
|------|---------|-------|
| 接受建议时 | "This suggestion is popular with similar users" | "You accepted this suggestion" |
| Dashboard | "You're in the top 20% of KeyStone users" | "You've tracked [N] applications this month" |
| Paywall | "Unlock with Pro: calibrated suggestions" | "Unlock with Pro: unlimited analyses and application tracking" |

---

## 执行检查清单

在launch前必须完成：

- [ ] 所有营销文案通过"我们能证明吗？"测试
- [ ] Legal review of any claim containing "proven", "calibrated", "backed by data"
- [ ] Home page A/B test备选文案准备好
- [ ] B2B pitch deck更新
- [ ] App内提示文案更新
- [ ] 禁用任何包含具体数字的统计声明（除非有p<0.05支持）

---

## 为什么这很重要

在B2B销售中，大学 career director 或招聘机构负责人会问："你怎么知道这有效？"

如果我们说"calibrated on SG hiring manager behaviour"，他们问："你们有多少数据？用什么方法校准的？"

如果我们的答案是"0数据"，我们会失去信任。但如果我们现在说"outcome-tracking infrastructure"，我们说的是事实——我们正在建立收集数据的系统。这是可验证的、诚实的，并且在有数据时会变得强大。

**诚实是最好的策略**: 当我们有数据时，我们可以用数据。当我们还没有数据时，我们诚实地描述我们在建立什么。
