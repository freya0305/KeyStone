# KeyStone MVP 技术架构

## 架构概览

```
┌─────────────────────────────────────────────────────────────┐
│                      用户端（Frontend）                       │
│                    Next.js + Tailwind                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      API层（Backend）                       │
│                    Python FastAPI                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │ JD解析API │  │简历解析API│  │匹配分析API│  │OutcomeAPI│ │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Redis      │    │ PostgreSQL   │    │  Claude API  │
│   (缓存)     │    │  (数据)      │    │  (AI模型)   │
└──────────────┘    └──────────────┘    └──────────────┘
```

---

## 技术栈

| 层级 | 技术选型 | 说明 |
|------|---------|------|
| 前端 | Next.js + Tailwind + shadcn/ui | 成熟稳定 |
| 后端 | Python FastAPI | AI生态好，异步支持 |
| 数据库 | PostgreSQL 16+ | 关系数据 |
| 缓存 | Redis | 减少AI调用 |
| AI | Claude Haiku + Sonnet | 解析+生成 |
| 认证 | Clerk | Google OAuth |
| 支付 | Stripe | SGD结算 |
| 托管 | AWS ap-southeast-1 | PDPA合规 |

---

## 数据模型

### 用户表（users）

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email VARCHAR(255) UNIQUE,
  name VARCHAR(255),
  auth_provider VARCHAR(50),  -- google, email
  stripe_customer_id VARCHAR(255),
  subscription_tier VARCHAR(20) DEFAULT 'free',  -- free, pro
  subscription_status VARCHAR(20) DEFAULT 'active',
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

### 简历表（resumes）

```sql
CREATE TABLE resumes (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  file_name VARCHAR(255),
  file_type VARCHAR(20),  -- pdf, docx, txt
  raw_text TEXT,
  parsed_data JSONB,  -- 结构化后的简历数据
  vector_embedding ARRAY(FLOAT),  -- 简历向量
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

### 职位表（jobs）

```sql
CREATE TABLE jobs (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  source_url TEXT,
  source_type VARCHAR(50),  -- mycareersfuture, jobstreet, linkedin, free_text
  raw_text TEXT,
  parsed_data JSONB,  -- {title, company, company_type, requirements: [...]}
  vector_embedding ARRAY(FLOAT),
  created_at TIMESTAMP DEFAULT NOW()
);
```

### 匹配分析表（analyses）

```sql
CREATE TABLE analyses (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  resume_id UUID REFERENCES resumes(id),
  job_id UUID REFERENCES jobs(id),
  match_score FLOAT,  -- 0-1
  skill_details JSONB,  -- [{skill, match_level, resume_level, job_level}]
  suggestions JSONB,  -- [{original, suggested, aspect, confidence}]
  created_at TIMESTAMP DEFAULT NOW()
);
```

### Outcome追踪表（outcomes）

```sql
CREATE TABLE outcomes (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  job_id UUID REFERENCES jobs(id),
  resume_id UUID REFERENCES resumes(id),
  applied_at TIMESTAMP,
  current_stage VARCHAR(50),  -- applied, callback, screening, interview, offer, rejected, no_response
  outcome_at TIMESTAMP,
  notes TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

### 建议采纳表（suggestion_feedback）

```sql
CREATE TABLE suggestion_feedback (
  id UUID PRIMARY KEY,
  analysis_id UUID REFERENCES analyses(id),
  outcome_id UUID REFERENCES outcomes(id),
  original_text TEXT,
  suggested_text TEXT,
  action VARCHAR(20),  -- adopted, modified, rejected
  modified_text TEXT,  -- 如果用户修改了
  created_at TIMESTAMP DEFAULT NOW()
);
```

---

## API设计

### 认证相关

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/auth/callback` | GET | Google OAuth回调 |
| `/api/auth/me` | GET | 获取当前用户 |
| `/api/auth/logout` | POST | 登出 |

### 简历相关

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/resumes/upload` | POST | 上传简历文件 |
| `/api/resumes/{id}` | GET | 获取简历详情 |
| `/api/resumes/{id}` | DELETE | 删除简历 |
| `/api/resumes` | GET | 获取用户所有简历 |

### JD相关

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/jobs/parse` | POST | 解析Job URL或文字 |
| `/api/jobs/{id}` | GET | 获取Job详情 |
| `/api/jobs` | GET | 获取用户所有Job |

### 分析相关

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/analyses` | POST | 创建新分析（简历+Job） |
| `/api/analyses/{id}` | GET | 获取分析结果 |
| `/api/analyses/{id}/suggestions/{sid}` | PATCH | 更新建议状态（采纳/拒绝/修改） |

### Outcome相关

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/outcomes` | POST | 记录新投递 |
| `/api/outcomes/{id}` | PATCH | 更新投递状态 |
| `/api/outcomes` | GET | 获取用户所有投递记录 |

### 订阅相关

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/subscription` | GET | 获取订阅状态 |
| `/api/subscription/create` | POST | 创建订阅（Stripe） |
| `/api/subscription/cancel` | POST | 取消订阅 |

---

## 核心流程

### 1. 简历上传 + 解析

```
POST /api/resumes/upload
  │
  ▼
文件上传 → 保存原始文件
  │
  ▼
调用Claude Haiku解析
  │
  ▼
存储：parsed_data (JSON) + vector_embedding
  │
  ▼
返回：resume_id + 解析结果预览
```

### 2. JD解析

```
POST /api/jobs/parse
  │
  ▼
判断输入类型：
  - URL → 爬取网页 → 提取文本
  - 文字 → 直接使用
  │
  ▼
调用Claude Haiku结构化
  │
  ▼
识别：公司类型（GLC/MNC/SME）
  │
  ▼
存储：parsed_data + vector_embedding
  │
  ▼
返回：job_id + 解析结果
```

### 3. 匹配分析

```
POST /api/analyses
Body: {resume_id, job_id}
  │
  ▼
获取：resume + job
  │
  ▼
计算：向量相似度 → match_score
  │
  ▼
生成：skill_details (逐项匹配分析)
  │
  ▼
生成：suggestions (3-5条修改建议)
  │
  ▼
存储：analyses表
  │
  ▼
返回：match_score + skill_details + suggestions
```

### 4. Outcome追踪

```
POST /api/outcomes
Body: {job_id, applied_at}
  │
  ▼
用户选择当前阶段
  │
  ▼
存储：outcomes表
  │
  ▼
用户后续更新：callback / screening / interview / offer / rejected
  │
  ▼
数据积累：用于AI学习
```

---

## AI调用策略

### Phase 1（无缓存）

| 功能 | 模型 | 成本/次 |
|------|------|---------|
| 简历解析 | Haiku | $0.001 |
| JD解析 | Haiku | $0.001 |
| 匹配分析 | Sonnet | $0.01 |
| 建议生成 | Sonnet | $0.02/条 |

### 缓存策略

```
简历解析结果 → Redis缓存7天
JD解析结果 → Redis缓存7天（热门Job更长）
匹配结果 → 不缓存（每次Job+简历组合不同）
```

---

## 安全考虑

### NRIC检测

```
Step 1: 文件上传后，Server-side正则检测NRIC格式
Step 2: 如果检测到 → 立即mask（替换为XXXX）
Step 3: 验证mask完成
Step 4: 后续所有处理使用masked版本
Step 5: 原文件不存储
```

### 数据隔离

```
每个用户只能访问自己的：
- 简历
- Job记录
- 分析结果
- Outcome数据

RLS（Row-Level Security）在PostgreSQL层强制执行
```

### PDPA合规

```
- 所有数据存储在AWS ap-southeast-1
- Claude API配置zero data retention
- 用户可申请删除所有数据
- 6-type独立consent
```

---

## 开发优先级

### Week 1-2：基础设施

```
✅ 项目初始化（Next.js + FastAPI）
✅ 数据库Schema设计
✅ 认证（Clerk）
✅ 基础API框架
```

### Week 3-4：核心功能

```
✅ 简历上传 + 解析
✅ JD解析（URL + 文字）
✅ 匹配分析
✅ 基础前端展示
```

### Week 5-6：用户体验

```
✅ 修改建议展示
✅ 简历编辑区
✅ 导出功能（PDF）
✅ Outcome追踪
```

### Week 7-8：发布准备

```
✅ Stripe订阅集成
✅ Referral系统
✅ Bug修复
✅ 测试
```

### Week 9-10：Launch

```
✅ MVP发布
✅ 监控 + 日志
✅ 初步数据分析
```

---

## 成本估算（月度）

| 项目 | 成本 |
|------|------|
| AWS EC2 + RDS | $150 |
| Redis (ElastiCache) | $25 |
| Claude API (100用户) | $500 |
| Clerk认证 | $25 |
| Stripe | 免费 |
| **总计** | **~$700/月** |

---

## 下一步

| 事项 | 负责 | 状态 |
|------|------|------|
| 详细技术设计 | 工程师 | 待分配 |
| 数据库Schema评审 | 工程师 | 待分配 |
| API设计评审 | 工程师 | 待分配 |

---

*待工程师评审和细化*
