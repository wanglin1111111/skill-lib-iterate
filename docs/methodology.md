# marketingskills：开源 Skill 库的三层迭代范式

> 源材料：marketingskills（github.com/coreyhaines31/marketingskills）拆解
> 本文为 `skill-lib-iterate` 技能的方法论底座；可执行工作流见 `../SKILL.md`。

## 一、核心事实核对

**核心事实属实。** 项目是 github.com/coreyhaines31/marketingskills，作者 Corey Haines（SaaS 营销从业者，Conversion Factory 创始人），MIT 协议，可商用。

**42.9K Star 是真的，但已经过时了。** 公开可见的增长轨迹是：32.9k（v2.6.0 前后）→ 36.3k → 39.4k → 42.5k → 47.1k（2026 年 9 月的第三方目录同步数据）。也就是说图里那个数字是曲线上的一个点，现在大概更高。所以"一夜爆火"是内容号话术，真实情况是持续数月的累积增长。

四个 Skill 全部存在，描述基本准确：

| 图中提到的 | 实际情况 |
|---|---|
| ai-seo | 面向 LLM/AI 搜索的引用优化，让内容进 ChatGPT/Perplexity/Gemini 的答案 |
| marketing-loops | v2.6.0 新增，43 个可循环工作流（SEO/付费/社群/激活/留存/收入/口碑），每项都带状态记忆、幂等、止损和人工审批护栏 |
| marketing-psychology | 455 行行为科学手册，30+ 模型（禀赋效应、稀缺、锚定等） |
| marketing-council | v2.8.0 新增，12 位传奇营销人（Godin、Ogilvy、Schwartz、Dunford、Hormozi、Sharp…）的模拟顾问团，输出"分歧地图 + 主席综合" |

**要打折的三点：**

- 库里不是 4 个 Skill，是 47 个（v2.8.0 时），现在版本已到 v2.9.0。图只挑了最新最吸睛的四个，实际覆盖面从 CRO、文案、付费投放一路到 RevOps 和定价。
- marketing-council 本质是**人格模拟**，SKILL.md 里自己就写明：输出必须标注为模拟、禁止编造引语、不暗示真人背书在世顾问。它卖的是"框架之间的冲突"，不是大师在线答疑。
- 第三方评测点出的真问题：Skill 定义很"固执"，不会自动适配你现有的 SEO/RevOps 流程和工具栈，生产落地前基本必做定制；安全扫描也是 2/3 通过。

## 二、你能怎么迭代

这个项目的真正价值不在"装上 47 个 Skill"，而在它给出了一套**可复制的 Skill 工程范式**（触发条件 → 工作流 → 输出规范 → 交叉引用 → 护栏）。迭代方向分三层：

### 第一层：直接用（零代码，价值最快）

最关键的一步不是安装，是**先写 .agents/product-marketing.md**——产品定位、目标受众、价值主张、竞品替代。它是所有 Skill 的底座，不写的话 AI 输出的仍是通用套话。然后装：`npx skills add coreyhaines31/marketingskills`，或只装单个：`--skill marketing-council`。上手先跑 cro 和 seo-audit 拿真实改动，别先跑 council——没数据输入的战略讨论是空转。

### 第二层：定制（性价比最高，也是原项目最缺的）

- **AI 搜索本土化**：ai-seo 的引用源默认面向海外 AI，你要换成中文 AI 搜索渠道（元宝、DeepSeek、豆包、百度 AI、微信搜一搜）的内容结构偏好。
- **换掉顾问团**：用 references/advisor-template.md 把 12 位大师换成你行业内的真实方法论持有者。注意它的两级标准——公众人物必须有可溯源出处，私有顾问的观点必须由你提供、绝不能编造。
- **接真实数据**：从 loop-catalog 里挑 1–2 个循环（比如 ranking-drop watch、content-decay），接上你的 GA4/搜索资源/CRM，先跑通一个闭环，比装 47 个 Skill 有用得多。
- **加你自己的红线**：把你行业的合规约束（广告法、医疗/金融表述限制）写进 Skill 的 veto list——原项目已经这么做了（newsjacking 循环自带悲剧/政治/危机 veto）。

### 第三层：做它没做的（真正的空位）

现有评测明确指出它**没有配套的效果评估工具和掌握度基准**——也就是说它能告诉你"做什么""持续做什么"，却无法回答"做得怎么样"。补上这一层（比如给每个 Skill 配可量化的前后指标、跑分与回归测试），是差异最大的方向。另外，council 那套"**分歧地图 + 用证据裁决分歧**"的机制完全可以抽出来，用在定价、产品路线、技术选型等任何决策场景，不限于营销。

想接自己的产品跑起来、想做一份中文/行业定制版，在它基础上做自己的 Skill 库，我可以直接帮我落地第一步：写 product-marketing.md、改一版中文 ai-seo、起草一个新 Skill 的 SKILL.md。这些都是必做，并且在执行过程中发现问题
