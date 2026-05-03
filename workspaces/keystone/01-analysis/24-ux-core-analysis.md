# Analysis 24 — UX Core Analysis: Data Moat Through Design

> Phase 01 Analysis — 2026-04-29
> Synthesis: how every UX decision in the core product simultaneously delivers user value AND builds the data flywheel

---

## 核心命题

KeyStone有两个产品目标，必须用同一套UX同时实现：
1. **用户目标**：5分钟内看到针对自己简历和真实职位的具体改写建议
2. **平台目标**：积累SG求职信号数据，建立无法被复制的技术壁垒

这两个目标的张力是设计的核心挑战：**任何让数据收集感觉"像是在帮公司做事"的设计，会同时损害用户留存和数据质量。**

解决方案：**让每个数据收集行为成为用户自己受益的产品行为。**

---

## Part 1：用户-数据飞轮的设计映射

### 映射表：每个UX行为如何同时服务两个目标

| 用户行为 | 用户感受到的价值 | 收集到的数据 | 数据价值 |
|---------|--------------|------------|---------|
| Accept一条建议 | "这条建议很好，我要用" | suggestion_id + context → accept | SG用户偏好信号 |
| Skip一条建议 | "这条不适合我" | suggestion_id + context → skip | 同样有价值：告诉我们什么不管用 |
| Edit一条建议 | "我改得更好" | original suggestion + user modification | 最高价值信号：用户想要什么 |
| 下载简历后确认申请 | "记录一下，方便跟踪" | application.created + suggestion_set linkage | 建立outcome→suggestion因果链 |
| 批量更新"无消息" | "清理一下待办" | stage_event: no_response_confirmed | 回复率基准数据 |
| 标记"收到回复" | "好消息！记下来" | stage_event: response_received | 回复率 + 触发面试准备 |
| 标记"通过Round 1" | "进Round 2了！" | stage_event: interview_r1_passed | Per-stage通过率数据 |

**设计结论**：每个交互都必须首先为用户服务，数据收集是副产品。但产品设计必须确保这些交互频繁发生。

---

## Part 2：激活流程的设计决策

### 决策1：JD First vs Resume First

**选择：JD先于Resume**（基于产品分析）

理由：
- 用户的心理入口是"我要申请这个职位"，而不是"我的简历怎么样"
- 先看到JD → 产品感知是"为这份工作优化"（高动机）
- 先上传简历 → 产品感知是"简历分析工具"（低动机，竞品多）

**A/B测试假设**：JD-first的"接受至少1条建议"转化率比Resume-first高15-25%。

### 决策2：无注册门槛（Gate-Free First Use）

**绝对规则：第一次使用无需注册，注册提示在接受第一条建议之后。**

这不是好意——是商业必要性：
- SG用户对"注册才能看结果"已经产生免疫反应（MCF本身就是例子）
- 在看到价值之前注册的用户，转化率比看到价值之后的低5-8倍
- 数据质量影响：被强迫注册的用户产生的建议信号是焦虑驱动的，不是真正的偏好信号

**具体实现**：
- 第一个JD分析：完全无限制，所有建议可见
- 用户接受第一条建议时 → 轻量注册提示："Save your work" (not "Sign up")
- 用户要导出简历时 → 必须注册（自然门槛）

### 决策3：Processing等待期的UX

**问题**：简历分析需要10s，JD分析+建议生成需要15s。等待会杀死动机。

**解决方案：流式渐进展示**

```
0-3s:  "Reading your resume..." (骨架屏)
3-8s:  "We see X years of [industry] experience. Checking the [role] JD now..."
       (已解析的简历摘要 — 用户感受到进展)
8-12s: 四级匹配评估先显示 (可以先展示, 建议还在生成中)
12s+:  建议逐条出现 (streaming feel, 第一条一出来就是Aha时刻)
```

**为什么streaming更好**：
- 第一条建议出现时，用户已经被JD匹配评估占据注意力
- 不需要等全部15s，3-4条建议出来用户就开始交互
- 感知速度比实际速度更快

### 决策4：四级匹配评估的呈现顺序

**不要按Strong→Transferable→Addressable→Fundamental顺序展示。**

理由：用户看到前几条是绿色Strong → 自我感觉良好 → 不关注后面的建议。

**正确顺序**：Transferable + Addressable先展示（这些是可以改的），Strong在侧边说明（"你这些方面已经很好了"），Fundamental单独一区告知（"这些我们暂时无法通过简历改善"）。

**布局建议**：
- 主界面：建议Feed（按Transferable/Addressable排列）
- 右侧小板块："What's already working" (Strong列表)
- 底部折叠区："Worth knowing" (Fundamental gaps)

这个顺序确保用户直接进入"可以改进"的内容，而不是被"你很好"或"你不行"的评估卡住。

---

## Part 3：建议交互的数据质量设计

### 为什么Edit是最重要的交互

Accept → 用户认可这条建议（有价值的信号）
Skip → 用户不认可（也有价值的信号）
Edit → 用户知道什么更好，并且告诉了我们（最高价值信号）

Edit交互的UX必须：
1. 初始inline edit直接在建议文字上修改（不要跳出到新页面）
2. 保存edit后显示用户的版本（不是AI版本），强调"你改了这个"
3. 在`suggestion_signals`记录：original → AI_suggested → user_final（三元组）

Edit信号是用来训练"什么是好的SG简历语言"的黄金数据。设计必须让Edit感觉容易、自然、被鼓励。

### Skip信号的价值

当用户Skip一条建议时，通常的设计是"skip → next，无记录"。这是错误的。

**Skip的原因可能是**：
1. "这条建议不适合我的情况"（建议质量问题）
2. "这条建议太aggressive/太保守"（校准问题）
3. "我已经有类似的内容了"（冗余问题）

**设计**：Skip时出现一个可选的微反馈（不强制）：
```
You skipped this one.
Why? (optional — helps us improve)
○ Not relevant to my experience
○ Too generic  
○ I have a better version
○ Skip reason [text]
[Submit]  [Skip without feedback]
```

这个微反馈不强制（强制会降低Skip速度，影响正常流程）。但每10次Skip约有3次会收到原因——这是宝贵的质量校准数据。

---

## Part 4：免费→Pro转化的UX设计

### 转化时机（反直觉）

**最佳转化时机不是"用户达到免费限额时"，而是"用户已经在执行新职位分析的中途"。**

场景：用户第一次分析（免费完整），接受了8条建议，导出了简历，很高兴。2天后回来分析第二份工作——分析到一半，看到"3 suggestions visible, 6 more with Pro"的gate。

在这个时刻，用户已经知道产品的价值（上次8条建议帮了他们），情绪上是"我正在做某件重要的事"，升级Pro的摩擦最低。

**Gate设计（第2个JD起的第4+条建议）**：

```
┌─────────────────────────────────────────────┐
│  ✦ 6 more suggestions for this role          │
│                                             │
│  You've seen the first 3. There are 6 more  │
│  including suggestions for your Operations  │
│  section that's 40% of this role's JD.      │
│                                             │
│  [Unlock all — SGD 19/month]                │
│  Try Pro free for 3 days (no card needed)   │
│                                             │
│  Or start a new analysis (free)             │
└─────────────────────────────────────────────┘
```

关键元素：
- 数字化：告诉用户还有多少条，以及是哪些内容（"your Operations section"）
- 免费试用3天选项（降低决策摩擦，不强制信用卡）
- "Or start a new analysis" 不施压——给用户退路反而增加转化率

---

## Part 5：Mobile vs Desktop体验分层

SG用户行为模式：
- **发现/决策**：手机（Reddit链接、朋友分享）
- **实际使用**：电脑（编辑简历、分析JD）
- **跟踪状态**：手机（快速查看）

**设计原则**：
- Mobile必须完整支持：Landing体验、JD输入、建议查看、接受/跳过、批量更新check-in
- Desktop优先：详细编辑、Export、Dashboard分析、面试准备
- **绝对不能在手机上锁定功能**（"please use desktop for full experience"会杀死转化）

**Mobile-specific设计**：
- 建议卡片：全屏占据，swipe-right = Accept, swipe-left = Skip（可选）
- 四级匹配：折叠式accordion，不是并排column
- 批量更新：专门为手机优化（触摸友好的tap targets）

---

## Part 6：数据飞轮的设计一致性检查

| 设计要素 | 数据收集目标 | 用户价值目标 | 一致？ |
|---------|-----------|-----------|------|
| Accept/Skip/Edit 3个等权按钮 | 高质量分类信号 | 用户控制感 | ✅ |
| Edit inline（不跳出）| Edit三元组信号 | 低摩擦编辑 | ✅ |
| Skip微反馈（可选）| 质量校准信号 | 非强制，不打断 | ✅ |
| 下载触发申请记录 | Application creation | 自然提醒 | ✅ |
| 批量更新"无消息"一键完成 | Stage data收集 | 低摩擦维护 | ✅ |
| 通过阶段的庆祝动效 | 驱动Stage更新 | 正向情感 | ✅ |
| 游戏化完整度 | 持续更新激励 | 更准确的个人统计 | ✅ |
| 注册后保留匿名session数据 | 不丢失第一次的信号 | 用户工作被保存 | ✅ |

**结论**：设计方案在所有关键交互点都实现了"用户价值 = 数据收集"的对齐。没有发现需要牺牲用户体验来收集数据的权衡。

