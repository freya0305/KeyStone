# Analysis 17 — Browser-Only Outcome Logging Reminder Strategy

> Phase 01 Analysis — 2026-04-29
> Question: Push notifications don't work for browser users (the majority). What's the correct reminder mechanism?

---

## 核心结论

Push notifications（移动/桌面app通知）在纯Web产品上不是首选路径。SG用户90%+通过浏览器投简历（MCF、JobStreet、LinkedIn），不会安装原生app。**正确的主路径是：邮件序列 + 深链接。** Web Push API作为可选补充，Calendar ICS作为高意愿用户辅助工具。邮件解析（Gmail/Outlook解析MCF通知）是高价值但高复杂度的可选功能。

---

## Part 1：问题准确定义

### 当前spec的错误假设

spec写道："Day-7 and Day-21 nudges with company name and role in subject line"

这暗示了推送通知机制，但没有说明渠道。在纯Web产品中：
- 没有原生app → 没有APNs/FCM推送
- 没有SMS集成（已有手机验证但非营销SMS）
- 唯一可靠的异步触达渠道：**邮件**

### 用户行为现实

```
用户投简历路径（典型）：
1. 在MCF/JobStreet/LinkedIn发现职位
2. 在该平台提交申请（有时导入到KeyStone）
3. 关闭浏览器，做其他事
4. 几天后收到MCF/招聘系统的自动确认邮件
5. 1-2周后收到HR的邮件/LinkedIn消息
6. 除非主动想起，否则不会回到KeyStone记录结果

问题：KeyStone在步骤3-6之间没有触达用户的手段。
```

---

## Part 2：五个可选方案评估

### 方案A：邮件序列（主推，MVP必须）

**机制**：
- 每次用户提交申请（无论来源），系统安排一系列提醒邮件
- 邮件包含：公司名、职位名、深链接直达该申请的状态更新页
- 邮件内容基于申请后时间（Day 3、Day 10、Day 21）

**触发条件**：
- Day 3："你于3天前申请了[职位] at [公司]，有什么进展吗？" → [点击更新]
- Day 10："已过10天 — [公司]还没有消息？" → [标记为无回复] / [有好消息！]
- Day 21（若仍未更新）："自动标记为'无回复' — 点击撤销" → 用户不操作则auto-close

**技术实现**：
- SendGrid / Postmark等邮件服务
- 申请记录创建时添加cron job / scheduled task
- 邮件包含带JWT令牌的deep link → 一键更新无需登录

**成本估算**：
- SendGrid Essentials: USD 25/month → 50,000 emails/month
- 按1,000个活跃用户 × 5个open applications × 3封邮件 = 15,000 emails/month
- 成本可忽略不计

**局限**：
- 依赖用户在KeyStone留下有效邮件（手机验证已要求，但需also验证邮件）
- 邮件可能进垃圾箱（需要domain warm-up、SPF/DKIM设置）
- 不是实时的

**结论**：MVP必须包含。可靠性最高，跨平台覆盖最广。

---

### 方案B：Web Push API（可选增强，MVP+）

**机制**：
- 用户在浏览器中opt-in接受通知
- 浏览器在后台接收推送（用户关闭标签也能收到）
- 点击通知直达具体申请的更新页

**SG市场兼容性**：
| 浏览器/平台 | Web Push支持 |
|-----------|------------|
| Chrome（Windows/Android）| ✅ 完全支持 |
| Chrome（macOS）| ✅ 完全支持 |
| Safari（macOS 13+）| ✅ 支持（2023年起）|
| Safari（iOS 16.4+）| ⚠️ 仅PWA模式支持（需添加到主屏幕）|
| Firefox | ✅ 完全支持 |
| Samsung Internet | ✅ 支持 |

**SG实际情况**：SG用户桌面Chrome占比高（金融/科技用户约60-70%桌面使用），Web Push覆盖率约70-75%。iOS Safari限制是最大痛点。

**实现成本**：
- 中等复杂度：需要Service Worker、推送订阅存储、VAPID密钥管理
- Firebase Cloud Messaging（免费）或直接Web Push协议

**用户摩擦**：
- 需要用户主动点击"允许通知"→ SG用户对权限请求的接受率约15-25%
- 请求时机关键：在用户完成第一次成功申请记录后请求，而非首次访问

**结论**：Phase 2增强功能，不是MVP。邮件方案先行。

---

### 方案C：Calendar ICS（高意愿用户工具）

**机制**：
- 用户提交申请后，提供"添加提醒到日历"按钮
- 生成.ics文件，用户双击导入到Google Calendar / Outlook
- 提醒内容："{公司名}：{职位}申请跟进"
- 提醒时间：申请后Day 7、Day 14

**优点**：
- 零依赖：不需要邮件服务、不需要推送
- 跨平台：任何日历app都支持
- 高意愿用户会主动导入

**局限**：
- 被动：用户需要主动操作下载.ics
- 无法动态更新：已创建的日历提醒不能被撤销或修改
- 覆盖面有限：只有30-40%的用户会实际使用

**结论**：低成本补充功能，配合邮件方案使用。单独不够。

---

### 方案D：邮件解析集成（高价值，高复杂度，Phase 3）

**机制**：
- 用户授权KeyStone读取其Gmail/Outlook收件箱（OAuth2）
- 解析来自MCF、JobStreet、LinkIn等招聘平台的通知邮件
- 自动识别："Your application for [职位] at [公司] has been received"
- 自动更新申请状态，无需用户手动记录

**技术可行性**：
- Gmail API / Microsoft Graph API — 完全可行
- 解析逻辑：固定发件人域名 + 关键词匹配
- MCF邮件格式固定（政府系统），解析准确率高
- LinkedIn邮件格式一致，解析可靠

**用户价值**：
- **彻底解决手动记录问题** — 日志率从3-6%可能跃升到40-60%（自动记录）
- 真正的"零摩擦"数据积累

**PDPA考量**：
- 需要明确的邮件访问授权（OAuth2 scope说明清楚）
- 读取邮件内容属于敏感权限，需要PDPC合规评估
- 建议：读取时仅处理招聘相关邮件（发件人白名单），不存储邮件内容

**实现成本**：
- 高：OAuth集成 + 邮件解析逻辑 + 错误处理 + 白名单维护
- 需要专门的Phase 3工程工作量

**结论**：最高价值但不是MVP。列为Phase 3功能，现在架构时为接入点预留。

---

### 方案E：Periodic Digest邮件（主推，与方案A并行）

**机制**：
- 每周一发送"你上周的申请进展"摘要
- 列出所有open applications，每条附"有更新？"按钮
- 对3周以上无更新的申请："这些可能已经关闭了，确认一下？"

**与方案A的关系**：
- 方案A = 申请级触发（每次申请的个性化提醒）
- 方案E = 账户级触发（所有申请的周汇总）
- 两者互补：方案A覆盖时间敏感的节点；方案E覆盖长期open的申请

**结论**：与方案A一起在MVP实现。技术实现复用邮件基础设施。

---

## Part 3：推荐方案矩阵

### MVP（必须）

1. **申请级邮件序列**（方案A）：Day 3 / Day 10 / Day 21提醒，附深链接
2. **周摘要邮件**（方案E）：所有open申请汇总，降低"记录遗漏"
3. **下载即记录**（现有spec）：简历下载时提示"是否已提交？" — 这是最高转化率的记录触发点

### MVP+（Phase 2）

4. **Web Push API**（方案B）：Chrome/macOS opt-in通知，覆盖非邮件偏好用户
5. **Calendar ICS导出**（方案C）：配合邮件提醒，供高意愿用户使用

### Phase 3（高价值，延后）

6. **邮件解析集成**（方案D）：Gmail/Outlook OAuth读取，自动记录申请状态

---

## Part 4：深链接设计要求

邮件提醒的核心价值在于深链接——用户点击就能直达该申请的更新页面，无需登录。

**技术要求**：
- 每封提醒邮件包含唯一的JWT令牌（7天有效）
- 链接格式：`keystone.app/track/{application_id}?token={jwt}`
- 令牌解析后直接打开该申请的状态更新modal
- 用户完成一步操作（选择新状态）即结束，无需浏览器导航

**转化率估算**：
- 带deep link的邮件：点击→更新转化率约30-40%
- 无deep link（仅提示"去网站更新"）：转化率<5%
- Deep link是这个策略成功的关键变量

---

## Part 5：修正后的日志率预测

| 方案组合 | 预计日志率 | 说明 |
|---------|----------|-----|
| 无任何提醒（当前spec基线）| 3-6% | Teal/LinkedIn基准 |
| + 下载即记录触发 | 8-12% | 最高转化点 |
| + 邮件序列（MVP）| 12-18% | 3x提升 |
| + 周摘要邮件 | 15-22% | 叠加效果 |
| + Web Push（Phase 2）| 18-28% | Chrome用户补充 |
| + 邮件解析（Phase 3）| 40-60% | 自动化颠覆性提升 |

**MVP目标**：15-22%日志率（vs 3-6%基线）。这对数据积累速度有3-4x的提升效果。

---

## 诚实评估

| 方案 | 开发成本 | 用户覆盖率 | 日志率提升 | 推荐 |
|-----|---------|----------|---------|-----|
| 邮件序列 | 低-中 | 95%+ | 高 | ✅ MVP |
| 周摘要邮件 | 低（复用邮件）| 95%+ | 中 | ✅ MVP |
| 下载即记录 | 低 | 100% | 高 | ✅ 已在spec |
| Web Push | 中 | 70-75% | 中 | Phase 2 |
| Calendar ICS | 低 | 30-40% | 低 | Phase 2 |
| 邮件解析 | 高 | 60-70%（Gmail用户）| 极高 | Phase 3 |

