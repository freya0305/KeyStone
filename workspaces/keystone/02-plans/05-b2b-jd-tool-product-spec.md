# KeyStone JD Tool — B2B Product Specification

**日期**：2026-05-03
**版本**：v1.0
**状态**：Draft
**跑道**：18个月

---

## 产品定位

**一句话**：面向猎头公司的AI JD生成工具——输入职位信息，输出专业JD、候选人画像、市场薪资洞察。

不是平台，不是ATS，不做简历匹配或候选人搜索。是独立的JD专用工具。

---

## 目标用户

| 维度 | 描述 |
|------|------|
| **规模** | 5–20人的小型猎头公司 |
| **日产** | 10–50个JD |
| **现状** | 手动写（40-50%）或ChatGPT改（10-15%） |
| **痛点** | 每个JD 30-60分钟，质量参差不齐 |
| **决策人** | 猎头顾问本人（不需要老板审批） |
| **典型画像** | Tech/Finance专精，日均10+ JD，已用ChatGPT但效果不满意 |

---

## 定价

| Tier | 月费 | 用户数 | JD数 | 核心功能 |
|------|------|--------|------|---------|
| Solo | $29 | 1 | 30 | JD生成、品牌模板 |
| Pro | $69 | 1 | 无限 | +候选人画像、市场薪资、版本历史 |
| Team | $179 | 5 | 无限 | +团队协作、客户分享、API |

**锚定策略**：LinkedIn Recruiter $250/月。$29 = 1/8，$69 = 1天节省价值，$179 = 低于ATS人均价格。

---

## v1 MVP 功能

### 1. JD生成（核心）

**输入字段**：
- 职位名称（必填）
- 必 Skills 3–5个（必填）
- 可 Skills 3–5个（选填）
- 经验要求：年限 + 层级（选填）
- 公司类型：Startup / MNC / GLC / Government / SME（选填）
- 薪资范围：最低–最高 + 货币（选填）
- 工作地点：城市 + 区域（选填）
- 合同类型：Full-time / Part-time / Contract（选填）

**输出**：
- 完整JD（结构化：Overview / Responsibilities / Requirements / Nice-to-have / Benefits）
- 字数：400–800字（市场标准）
- 语气：Professional / Casual / Startup（选填）
- 格式：可复制文本

### 2. 品牌模板定制

- 上传公司Logo（URL或图片）
- 公司名称 + 简介（可选默认）
- 预设品牌颜色（HEX）
- 保存为"我的模板"
- 模板列表：创建 / 编辑 / 删除

### 3. 版本历史

- 每次生成自动保存一个版本
- 版本列表：时间 + 输入摘要
- 查看历史版本
- 恢复到历史版本（克隆为新版本）
- 最多保留50个版本

### 4. 客户分享

- 生成一个链接（有效期24小时）
- 客户无需登录即可查看
- 支持评论（客户输入反馈）
- 复制JD文本

---

## v2 功能

### 5. 候选人画像

基于输入生成：
- 理想候选人特征（3–5条）
- 目标背景（学历/经验/行业）
- 面试重点问题（3–5个）
- 留人要点（compensation + culture）

### 6. 市场薪资洞察

- 根据职位名称 + 经验 + 公司类型
- 显示市场薪资范围（来自聚合数据）
- 与公司提供范围的对比
- 数据来源标注

### 7. JD优化建议

- 读取现有JD文本
- 对标优秀JD标准
- 提供修改建议（结构/关键词/语气）

---

## v3 功能

### 8. 团队协作（Team Tier）

- 共享模板库（公司级别）
- 团队使用统计（每人生成数）
- 评论和审批流程
- 团队品牌配置

### 9. API访问

- REST API：生成JD / 获取模板 / 获取历史
- Webhook：生成完成通知
- 限流：100次/分钟

### 10. 批量生成

- 上传CSV（职位列表）
- 批量生成 + 导出ZIP
- 进度跟踪

---

## 用户流程

### 每日核心流程（单次JD）

```
1. 打开工具（已登录）
2. 选择"新建JD"或从模板创建
3. 填写职位信息表单（3–5分钟）
4. 点击"生成"（5-10秒）
5. 预览JD
6. 如需调整 → 编辑字段 → 重新生成
7. 满意 → 复制 / 导出PDF / 发送给客户
8. 客户链接分享（可选）
```

### 客户反馈循环

```
1. 发送分享链接给客户
2. 客户打开 → 查看JD → 填写反馈表单
3. 猎头收到邮件通知（"客户反馈已提交"）
4. 猎头打开工具 → 查看反馈 → 编辑 → 重新生成
5. 重复直到客户满意
```

### 新用户引导（Onboarding）

```
Step 1: 注册（邮箱 + 密码，或SSO）
Step 2: 选择公司类型（个人/SME/Enterprise）
Step 3: 上传Logo + 公司名称（可选，跳过）
Step 4: 创建第一个JD（引导填写必填项）
Step 5: 预览 + 编辑
Step 6: 完成 → 显示"已节省X分钟"
Step 7: 引导至定价页面（可选）
```

---

## UI/UX 考虑

### 单页工具 vs 向导流程

**选择：单页 + 分步填写面板**

原因：
- 猎头每次只处理一个JD，不需要多步骤
- 分步向导打断思路
- 单页可以即时预览

### 布局结构

```
┌─────────────────────────────────────────────────────────┐
│  [Logo] KeyStone JD    [我的模板] [历史] [定价] [头像]   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────────┐  ┌─────────────────────────┐  │
│  │   输入表单（左）     │  │   预览输出（右）         │  │
│  │                     │  │                         │  │
│  │  职位名称           │  │   [Overview]            │  │
│  │  必 Skills          │  │   [Responsibilities]    │  │
│  │  可 Skills          │  │   [Requirements]        │  │
│  │  经验要求           │  │   [Benefits]            │  │
│  │  公司类型           │  │                         │  │
│  │  薪资范围           │  │   ─────────────────     │  │
│  │  工作地点           │  │   [候选人画像] (v2)     │  │
│  │  合同类型           │  │   [市场薪资] (v2)      │  │
│  │                     │  │                         │  │
│  │  [生成JD]           │  │   [复制] [导出] [分享]   │  │
│  └─────────────────────┘  └─────────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 响应式策略

- **桌面优先**（猎头主要在PC端工作）
- **平板支持**（iPad可用）
- **手机不重点优化**（猎头不在手机上写JD）

### 关键屏幕

| 屏幕 | 功能 | 路径 |
|------|------|------|
| 首页/Dashboard | 快速新建 + 最近历史 | `/` |
| 生成页 | 单页JD生成工具 | `/jd/new` |
| 历史页 | 所有JD列表 + 搜索 | `/jd/history` |
| 模板页 | 管理品牌模板 | `/templates` |
| 设置页 | 账号 + 公司信息 | `/settings` |
| 分享查看页 | 客户无登录查看 | `/share/{token}` |

---

## 数据模型（高阶）

### 核心实体

```
User
├── id (UUID)
├── email
├── password_hash
├── name
├── company_name
├── company_type (startup/mnc/glc/government/sme)
├── logo_url
├── brand_color
├── tier (solo/pro/team)
├── created_at
└── updated_at

JD
├── id (UUID)
├── user_id (FK)
├── title
├── required_skills (JSON array)
├── optional_skills (JSON array)
├── experience_level
├── company_type
├── salary_min / salary_max / salary_currency
├── location_city / location_region
├── employment_type (fulltime/parttime/contract)
├── tone (professional/casual/startup)
├── content (JSON: overview/responsibilities/requirements/benefits)
├── source_version_id (FK, nullable — 指向原版，如是编辑后生成)
├── share_token (unique)
├── share_expires_at
├── created_at
└── updated_at

Template
├── id (UUID)
├── user_id (FK)
├── name
├── company_name
├── company_description
├── logo_url
├── brand_color
├── is_default (bool)
├── created_at
└── updated_at

ShareFeedback
├── id (UUID)
├── share_token (FK)
├── client_name
├── client_email
├── feedback_text
├── submitted_at
```

### Analytics 要追踪的数据

| 数据 | 用途 | 何时收集 |
|------|------|---------|
| JD生成数/用户/天 | 产品健康度 | 每次生成 |
| 模板使用率 | 功能价值 | 每次生成 |
| 分享打开率 | 客户参与度 | 链接打开时 |
| 反馈提交率 | 流程有效性 | 反馈提交时 |
| 付费转化 | 商业健康度 | 升级时 |
| Tier分布 | 收入分析 | 注册时 |

---

## 技术方向（待细化）

| 组件 | 选择 |
|------|------|
| 前端 | Next.js + Tailwind + shadcn/ui |
| 后端 | Python FastAPI（或Kailash Nexus） |
| 数据库 | PostgreSQL |
| AI | Claude Haiku（快速生成）+ Sonnet（优化/v2） |
| 认证 | Clerk |
| 邮件 | SendGrid / Resend |
| 存储 | S3 / R2（Logo + 导出文件） |
| 部署 | Vercel（前端）+ Railway/Fly.io（后端） |

---

## 实施优先级

### Phase 1（0–4周）：MVP上线

```
Week 1–2: 后端 + 数据库
- User认证
- JD CRUD
- 模板CRUD
- AI生成接口（Haiku）

Week 3: 前端
- 登录/注册
- JD生成单页
- 预览 + 复制

Week 4: 上线
- 分享链接
- 基础统计
- $29 Solo定价
```

### Phase 2（5–8周）：Pro功能

```
- 候选人画像
- 市场薪资洞察
- 版本历史（恢复/克隆）
- $69 Pro定价
```

### Phase 3（9–18周）：Team + API

```
- 团队协作
- API访问
- 批量生成
- $179 Team定价
```

---

## 成功指标

| 指标 | 目标（6个月） |
|------|--------------|
| 付费用户 | 200 |
| 月经常性收入 | $15,000 |
| JD生成数/天 | 1,000 |
| 分享打开率 | 60% |
| 客户反馈提交率 | 30% |
| NPS | 40+ |

---

## 风险和应对

| 风险 | 概率 | 影响 | 应对 |
|------|------|------|------|
| AI生成质量不稳定 | 中 | 高 | 人工抽检 + 用户反馈循环 |
| 定价太高用户不接受 | 中 | 高 | 30天免费试用 + 锚定LinkedIn |
| 猎头不改变现有习惯 | 高 | 高 | 极低门槛试用（$29 Solo） |
| 竞品复制 | 中 | 中 | 快速迭代 + 数据护城河 |

---

*最后更新：2026-05-03*
