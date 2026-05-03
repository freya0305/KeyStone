# Analysis 18 — MVP Scope Definition (v1.0)

> Phase 01 Analysis — 2026-04-29
> Question: What is explicitly in and out of MVP v1.0? What are the "done" criteria?

---

## 核心结论

MVP的最大风险不是功能太少，而是**功能太多导致发布延迟**。当前spec包含了太多"应该有"功能。明确的v1.0范围需要一个核心问题：**6周内能上线的最小功能集，足以让一个SG求职者为之付费？**

答案是：**3个功能 + 2个架构要求**。

---

## Part 1：v1.0必须包含（不发布则没有产品）

### 功能1：Resume Upload + SG Analysis（5分钟内可用）

**必须**：
- PDF/DOCX/文本上传
- 基础SG flags（NRIC检测、NS section识别、照片建议）
- 主要强项/弱点输出（2-4条）
- 缓存（content hash），同一简历不重复分析
- PMET特有分析（职业转换叙事、年龄中性语言）

**可以没有**：
- ATS分数（不是SG雇主首要考量）
- 简历"排版优化"建议

---

### 功能2：JD输入 + 四级匹配评估

**必须**：
- URL解析（MCF、JobStreet、LinkedIn、公司官网）+ 文本粘贴fallback
- 雇主类型识别（GLC/MNC/SME/初创/政府）
- 四级分类（Strong/Transferable/Addressable/Fundamental）
- 每项分类附一句理由

**可以没有**：
- Batch mode（5个JD同时分析）— Phase 2
- 历史JD库

---

### 功能3：逐行修改建议（这就是产品）

**必须**：
- Transferable和Addressable gap的具体改写建议
- 每条建议：原文 → 建议改写 → 理由（引用JD要求和雇主类型）
- Accept / Reject / 手动修改交互
- 接受建议后可导出PDF/DOCX
- 免费限制：第一个JD无限建议；后续JD仅显示3条，其余需Pro
- **手机号验证**（SG mobile，防多账号）

**可以没有**：
- 内联diff view（可用简单的before/after展示）
- 多语言支持

---

### 架构要求1：建议信号记录（Day 1必须，不可后加）

**每次Accept/Reject/Modify都必须记录**：
```
suggestion_id, user_segment, company_type, role_level, 
industry, modification_type, session_id, timestamp
```

没有这个，数据壁垒永远不会形成。这是基础设施，不是功能。

---

### 架构要求2：申请漏斗跟踪（Stage-aware，必须）

**必须**：
- 简历下载时自动创建申请记录（触发记录的最高转化点）
- Stage tracking：Applied → Response → Screen → Interview(R1..RN) → Decision
- 邮件序列（Day 3/10/21提醒，附深链接）
- 最少5条记录后展示个人通过率dashboard

**可以没有**：
- Web Push通知
- 周摘要邮件（Phase 2，但在MVP+尽快加入）
- 邮件解析（Phase 3）

---

## Part 2：明确排除出MVP（不许进）

| 功能 | 排除原因 | 计划阶段 |
|-----|---------|---------|
| 面试准备模块 | 工程量大；先把用户带到面试这一步 | Phase 2 |
| Batch mode（5个JD）| 不是解决核心问题 | Phase 2 |
| LinkedIn Profile优化 | 不同产品 | 不确定 |
| 薪资基准/Offer评估 | 需要单独数据源 | Year 2 |
| 主动职位推荐 | 需要用户画像积累 | Year 2 |
| Cover letter生成 | 低价值（SG市场很少用）| 永不 |
| 移动app | Web-first；app是Phase 3 | Phase 3 |
| 双语UI（中文/马来文）| 英语先行 | Year 2 |
| 两端招聘平台 | 完全不同的商业模式 | 永不 |
| B2B大学dashboard | 需要大学签约；MVP前就开始销售 | 首个大学合同签约后 |
| 语音练习模拟 | 高复杂度 | Phase 3 |

---

## Part 3：MVP"Done"标准

### 功能层面

- [ ] 用户可在5分钟内完成：上传简历 → 粘贴JD → 看到具体改写建议
- [ ] 免费用户可体验完整价值（第一个JD无限制）
- [ ] Pro用户可无限制使用所有功能
- [ ] 手机号验证防多账号滥用
- [ ] 建议信号100%被记录到数据库

### 技术层面

- [ ] 处理时间≤10秒（简历分析）
- [ ] 处理时间≤15秒（JD分析 + 建议生成）
- [ ] 99.5%可用性（单region可以）
- [ ] PDPA合规：明确B2C训练同意 vs 仅服务同意
- [ ] LLM成本上限：≤SGD 5/用户/月（Haiku+Sonnet组合）

### 商业层面

- [ ] Stripe支付接入（SGD月付/年付）
- [ ] 至少1个设计伙伴给出书面推荐语
- [ ] 手机号验证完成（防free tier滥用）

---

## Part 4：MVP时间线（纯自主执行）

这是一个非常小的产品范围。在自主AI执行模型下：

| 阶段 | 内容 | 估算执行周期 |
|-----|-----|-----------|
| 核心引擎 | LLM prompts + SG rules + 数据模型 | 1-2 sessions |
| Web UI | Upload flow + suggestion UI | 1-2 sessions |
| 申请跟踪 + 邮件 | Stage model + SendGrid集成 | 1 session |
| 支付 + 验证 | Stripe + SMS verification | 1 session |
| PDPA合规 + 上线 | 同意管理 + 部署 | 1 session |

**总计：5-8个执行sessions + 1-2个红队/修复sessions**

关键约束：不是执行速度，而是：
1. 获取设计伙伴用户（需要几周）
2. Startup SG Grant申请（行政时间）
3. 首个大学合同洽谈（15-21个月，立即开始）

---

## Part 5：MVP决策原则

**每个功能决策用这个问题测试**：
> "如果我们不做这个，一个SG求职者还愿意付SGD 19/月吗？"

- 如果答案是"可能不愿意" → 进MVP
- 如果答案是"也许会，但不是主要原因" → Phase 2
- 如果答案是"和他们是否付费无关" → 砍掉或永不

