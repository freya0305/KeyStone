# Analysis 28 — Design Risks & Mitigations

> Phase 01 Analysis — 2026-04-29
> Top design risks for KeyStone MVP, with specific mitigation approaches

---

## Risk 1: AI建议感觉Generic，毁掉核心价值主张 [CRITICAL]

**风险描述**：如果建议输出是"Be more specific with your achievements"而不是"For this GLC Operations Manager role, your '管理团队' should be '率团队完成MAS 632合规改造，覆盖8个部门，达标率从76%提升至99%'"——用户立刻认为这是"ChatGPT加了个SG外壳"，不会付费。

**失败模式**：
- LLM prompt设计不足，输出通用career advice
- 公司类型检测失败，建议没有GLC vs MNC vs startup的差异化
- 建议针对JD要求不够精准（建议了resume没有提到的内容，而不是改写已有内容）

**缓解方案**：
1. **Specificity强制规则**：每条建议的rationale字段必须包含至少一个具体引用（JD中的具体词汇 OR 公司类型名称 OR SG市场特有规则ID）。没有具体引用的建议系统拒绝输出。
2. **Quality gate**：Design partner阶段（50-100用户），对"rejection rate"设置警戒线。如果第一次建议的Skip率 > 50%，暂停进入公测，重新调整prompt。
3. **Specificity test用例**：在CI pipeline中加入"建议通用性检测"——针对测试简历 + 测试JD，如果LLM输出包含["be more specific", "add quantifiable", "improve your", "consider adding"]等通用措辞，测试失败。
4. **A/B test建议版本**：Track"接受率"按照specificity评分。SG-specific建议 vs generic建议的接受率差异是产品质量最重要的leading indicator。

**指标**：首次使用的建议接受率目标 > 40%。低于30%触发prompt review。

---

## Risk 2: 四级匹配的Fundamental Gap令用户产生焦虑/放弃 [HIGH]

**风险描述**：用户——尤其是被裁员的PMET和转行的mid-career switcher——在情绪上脆弱。如果他们看到"FUNDAMENTAL GAP: 5/12 requirements"配上红色警告，会感觉"我根本不适合这份工作"，立刻放弃。

**失败模式**：
- 颜色使用红色（已解决：改为紫色plum，见Analysis 26）
- 措辞过于直接（"You don't have X"）
- Fundamental gap的数量在首屏太显眼

**缓解方案**：
1. **颜色**：Fundamental使用plum而非红色（已确认，见design system）
2. **措辞框架**："Skills to build toward" 而非 "Fundamental gaps"。配套文案："These aren't expected from day one. They're why the role is challenging."
3. **视觉层级**：Fundamental section默认折叠，在建议feed下方。用户需要主动展开。标题："Worth knowing (not a blocker)"
4. **上下文**：在Fundamental section顶部加一行计算："X of 12 requirements are strong matches. These 3 are longer-term — most candidates at this level face the same gaps."
5. **面向不同persona的tone调整**：
   - PMET用户（检测到10+年经验）：更强调可转移能力，更少强调gap
   - Fresh grad（检测到应届）：常态化gap（"Expected at entry level"）

**指标**：用户在看到Fundamental gaps后的放弃率（session abandonment）目标 < 20%。

---

## Risk 3: 免费Tier的Paywall设计打断用户动机 [HIGH]

**风险描述**：用户正在分析一份他们很想要的工作，到第4条建议时遇到paywall，中断了他们的"mental flow"。摩擦太大 → 用户不升级，直接离开。

**失败模式**：
- Paywall出现时机太早（第一个JD就出现）
- Paywall页面设计太"销售感"（破坏信任）
- Gate体验让用户感觉被"欺骗"（"你给我看了3条，但最重要的都锁起来了"）

**缓解方案**：
1. **First JD永远无限制**（已确认）：用户第一次使用获得完整体验，绝不在第一次就截断
2. **Gate copy的诚实原则**："6 more suggestions — this is where Pro comes in" 而不是 "Upgrade to unlock premium features"。诚实 > 营销。
3. **Gate显示内容预告**：告诉用户锁住的建议是关于哪个部分的（"6 more suggestions for your Experience section, which covers 60% of this JD's requirements"）——让用户感受到gate后面是有价值的内容，而不是空洞的"付费解锁更多"
4. **3-day free trial选项**：不需要信用卡，降低决策摩擦，让用户先体验再决定
5. **"Or analyze a different job free"**：始终提供替代路径，不把用户逼到角落

**指标**：Gate encounter → Pro upgrade率目标 > 15%（第30天内）。

---

## Risk 4: 申请跟踪感觉像"在帮公司收集数据" [HIGH]

**风险描述**：如果用户意识到申请记录和outcome数据是KeyStone的商业资产，会停止提供。更糟的是，如果这种感觉广泛传播（Reddit帖子、Telegram群），会形成品牌舆情。

**失败模式**：
- 任何界面文案提到"help us improve"或"our AI needs your data"
- PDPA同意界面中的训练同意被设计成默认勾选
- Dashboard的framing是"你在为我们收集数据" 而不是"这是你的求职数据"

**缓解方案**：
1. **Copy规则**：产品内所有文案禁止出现"help us"、"our AI"、"training data"、"dataset"的组合。文案唯一允许的框架是"your data, your insights"。
2. **训练同意UI**：明确opt-in，默认off，说明清楚（"Your accept/skip patterns help improve suggestions for everyone — only if you opt in"）。把这个选项设计成高质量的、让用户感觉信息透明的界面。
3. **Dashboard命名**：叫"Your job search"，不叫"Application tracker"或"Outcomes log"。每个分析页面都以"your"开头。
4. **Data export**：在设置页面提供"Export all your data"（PDPA要求，但也是信任信号）。
5. **PDPA visible placement**：Landing page的footer显示"PDPA Compliant · Your data stays in Singapore · You can delete everything anytime"——这三句话对SG用户比任何品牌宣言都有力。

---

## Risk 5: 产品在面试准备Phase 2前无法解决完整求职周期，用户流失 [MEDIUM-HIGH]

**风险描述**：用户拿到面试邀请后，KeyStone MVP无法提供任何支持（面试准备在Phase 2）。此时用户的需求最强烈，但产品无法满足 → 用户转向ChatGPT，习惯断裂，不再回来。

**失败模式**：
- MVP上线后，Phase 2 > 90天没有发布
- 面试准备入口完全缺失（用户不知道有这个功能要来）
- 拿到面试后的"next step"是空白页

**缓解方案**：
1. **MVP占位符UX**：当用户标记"收到面试邀请"时，显示一个informative screen："Interview prep is coming — subscribe for early access." + 提供现有的ChatGPT面试准备prompt作为临时工具（真实有用的内容，不是空洞的"coming soon"）
2. **时间承诺**：Phase 2（面试准备）必须在MVP上线后60天内发布。这是对用户的隐性承诺，也是LTV实现的关键。
3. **Email序列（合规的）**：用户拿到面试邀请后，发一封邮件："Congrats on the interview! Here's how to prepare specifically for [Company Type]" — 链接到一篇有价值的公开内容（blog post / guide）。这维持了产品与用户的连接，等待Phase 2发布。

---

## Risk 6: SG市场过于小众，B2C收入无法支撑运营 [STRATEGIC]

**风险描述**：红队分析已确认：Year 1 B2C ARR = SGD 27K–68K（仅靠organic），break-even需要SGD 100K ARR。这意味着B2C alone无法持续。

**这不是UX风险，但UX是解法的一部分**：
- 如果产品激活率 < 30%，Free→Pro转化率 < 4%，用户基数永远达不到break-even所需规模
- 如果口碑NPS < 40，有机增长停滞，无法突破B2C收入天花板

**UX层面的缓解**：
1. **NPS > 60是产品KPI**：Design中每个"delight moment"（第一条建议的Aha、阶段推进的庆祝、达到100%完整度的"All caught up"状态）都是NPS的投资
2. **Referral机制内置**：在用户拿到Offer时，显示"Share your success story（匿名可选）"。这既是口碑传播，也是成功故事数据
3. **B2B Demo Ready**：产品从Day 1要能展示给大学career centre director看。设计上注意"institutional demo"场景下的视觉质量和数据展示层

**指标**：NPS > 50 by Month 3；口碑推荐占新注册用户的比例 > 30% by Month 6。

---

## 风险优先级矩阵

| 风险 | 概率 | 影响 | 缓解难度 | 优先级 |
|-----|-----|-----|---------|------|
| 建议Generic | 高 | 产品致命 | 中（prompt工程）| P0 |
| Fundamental gap焦虑 | 中 | 转化率 -30% | 低（copy + color）| P1 |
| Paywall摩擦 | 高 | 转化率 -20% | 低（copy + timing）| P1 |
| 数据收集感觉extractive | 中 | 信任/品牌 | 中（copy system）| P1 |
| 面试准备缺口 | 高 | LTV -40% | 中（Phase 2时间表）| P2 |
| B2C规模天花板 | 高 | 战略生存 | 高（B2B必须配套）| P0（战略层）|

