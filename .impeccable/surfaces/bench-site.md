# Surface brief — 知验台分发链介绍站（bench.finddatatech.cloud）

Mode: **Persuade**（一条已上产分发链的门面；访客决定并行动）。Scope: 单页 index（首屏链路三节 + 实时概况带 + 证据区 + 两扇门 + footer）。

## Direction contract

**THESIS**: 层 0 论点——**竞争不在模型，在知识的沉淀与复利——评测出的知识以本体形态发布，多端消费**。本站拒绝模块站默认的「深色渐变 hero + 三特性卡」，也拒绝把「数据规模」当卖点；它把「这条链已上产、每个数字可核对、故障不伪装」做成可当场验证的体验。「本体」一词在本站专指 bench↔wire 分发链的本体资产，与壹座开放数据本体（及其数字）严格切割。

**OWN-WORLD**: 证据台账的扉页（Evidence Ledger, title page）。承接 law-bench 工作台 `law-bench/DESIGN.md` 的材质语言并按 Persuade 面重述：Ledger Gray `#f6f7f9` 哑光纸底 + Panel White `#ffffff` + 1px Rule Gray `#e2e5ea` 全包边（No-Gloss Rule：零阴影零渐变零装饰）；单点强调 Bench Blue `#2563eb`；Verdict Green `#047857` / Objection Red `#dc2626` 只作状态；质量分层色票 gold `#92400e` / silver `#475569` / bronze `#7c2d12`（tint + 文字成对，沿 Tint Verdict Rule）。display=Noto Serif SC（扉页铅字感），body=Noto Sans SC，机器数据（digest/as_of/端点/表值）=JetBrains Mono。浏览器面（选区/caret/focus/下划线偏移/tabular-nums）全随这套色主题化。

**STORY**: 访客（决策评估者 或 智能体开发者）第一眼看到层 0 论点，往下即**链路三节图**——① 知识沉淀（判官评审环迭代出的知识）→ ② 本体发布（版本化发布-拉取契约，节点内嵌 legal v2 digest `5897354d` 真证据锚）→ ③ 柏讯消费（跨命名空间拉取落库）——其下实时概况带当场验证②③：版本表 / 计数 / 分层分布 / as_of 全部活拉自匿名概览端点。签名运动「一锚贯之」：水合成功且 digest 对上时，链路节点与版本表同挂绿缘「live 对账一致」标。再往下：证据区（门 A 的资产/分层/评审环面，静态数字带 as_of 出处）→ 两扇门动作（门 A 回看证据面、门 B copy 端点 + curl 试令 + 认证说明）→ footer。边界如实：端点失败即报因卡，公开面只有概览窄口，全量访问需凭据。

**FIRST VIEWPORT**: 满幅 Ledger Gray 哑光纸，顶部一句论点（无 kicker，标题自带铅字重量）+ 两行 lede。其下链路三节图（三张 Panel White 平卡，蓝色顶缘 + mono 节点号，②号卡内嵌 digest 证据锚 mono 小字块）。再下实时概况带：SSR 态仅「正在连接匿名概览端点…」一行 mono 状态（**无任何摆拍数字**），水合后渲染 stats 胶囊 + 版本表 + as_of。整屏不见一张图、一道渐变。

**FORM**: 证据台账的扉页 — code-led（材质语言从 law-bench 工作台既有 design system 承接，无图像生成，无 comp）。

**FINISH**: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance.

## Raises (named donors)

- law-bench 工作台 "The Evidence Ledger"（`law-bench/DESIGN.md` Creative North Star）→ 台账纸 + 1px 规则 + 单点蓝 + tint 语义的世界本体；Persuade 重述 = 展示性排版（论点/链路/证据区隔）取代操作密度。
- 判官评审环（rubric × criteria、`generate → fill → evaluate → improve` 自愈）→ 证据区「知识是怎么被评测出来的」的说明支点。
- C3 知识分发契约的 digest（`3586552a`）→ 链路叙事的真证据锚 + 签名运动「一锚贯之」的对账物。

## Facts (claims binding — 每条有名有姓，白名单外数字拒绝上页)

**白名单（数字的唯一机器源是 [`bench-site-facts.json`](../../bench-site-facts.json)，本节不再复述数字）**：

> 白名单 #1–#3 的取值、来源与 `as_of` 全部登记在 `bench-site-facts.json` 的 `facts` 数组；
> 这组数字的退役旧值登记在同文件的 `retired` 数组。两者由 `scripts/check_facts.py` 在每次
> 构建时对 `dist/` 全量判定——白名单外数字与退役值命中都让构建失败。改数字只改 JSON，
> 不在本文件与页面分别复述（此前首屏与证据区各自复述同一个计数，结果一处被订正、另一处长期留着旧值）。

1. **法规目录计数**——出处与口径见 `bench-site-facts.json` `facts[id=law-catalog]`；页面 MUST 以 `<data value="…">` + `as_of` 标注。判据取样自现网，不取文档历史句。
2. **合同母版 / 带种子条款计数**——两个口径分别登记在 `facts[id=contract-masters]` 与 `facts[id=contract-seeds]`；两者 MUST 分开标注，不得用一个数字含混指代。
3. **MCP 工具数**——出处与口径见 `facts[id=mcp-tools]`（现网 `tools/list`，不取 README 历史句）。
4. **4 类知识资产**（① 本体 ② RAG 知识资产 ③ 评测资产（尺子）④ 微调数据）——出处 `law-bench/docs/knowledge-platform-blueprint.md` §二（"四类知识资产，一套内核"）。
5. **legal v2 已发布，digest `5897354d`**（5,117 实体 / 25 关系；2026-11-12 由 `publish_domain` 追加，v1 保留）——出处=**现网 `/api/public/overview` 实测**（v1 `3586552a` 是 2026-11-06 的联调冒烟：1 个实体）。判据取样自现网，不取历史文档句。
6. **ontology-builder 五岗舰队**（本体盘账员 → 本体建模师 → 纪律校验闸 → 声明提案员 → 台账主编；wire-ops 工具全只读 + 提案制，人工确认后落库）——出处 `fleet-packs/blueprints/ontology-builder/blueprint.json`（五 agent title）+ `fleet-packs/README.md`（"五岗（盘账/建模/校验闸/提案/主编）…全只读+提案制"）。
7. **判官评审环**（rubric × criteria 逐条判定 PASS/FAIL + 理由，多评审模型并行；自愈管线 `generate → fill → evaluate → improve` 迭代至达标）——出处 `law-bench/README.md` §能力表。
8. **gold/silver/bronze 质量分层**与**版本化发布-拉取契约**（domain/version/digest/published_at/counts）——出处 `knowledge-platform-blueprint.md`（四类资产共享质量档位/发布机制）与 law-bench change `add-bench-public-overview-tier` spec（概览载荷字段口径）。

**动态数字口径**：版本 / 计数 / 分层分布 / as_of 只从同源 `/api/public/overview` 活拉，**禁止硬编**；失败如实报因（状态码 + reason），不回退旧值、不摆拍、不做 localStorage 缓存。

**禁编造清单（圈禁）**：

- **壹座开放数据本体的数字禁挪用**：452 指标概念、24,395 概念、7 数据源等属开放数据本体公开口径（`openspec/specs/solution-package/spec.md`），与本模块叙事无关，一个都不上页。
- **wire dev 库内部状态不作卖点**：开发库实体数（0 实体等）是内部环境状态，不构成对外证据。
- **未上产能力不得写成完成态**：概览端点未 live 前，水合区以报因态呈现（诚实），文案不写「已上线」「实时在线」类完成态断言；评测环说明只述机制，不写未验收的效果承诺。
- **无用户数 / 无客户案例 / 无「世界最好」类断言**；官网上「本体」撞名歧义由 THESIS 的语义切割条款处理。

## Unresolved

- 端点 live 时点：上游 law-bench `add-bench-public-overview-tier` apply 后，水合即真；此前站点以报因态上产亦诚实（proposal 已裁）。
- 英文轨：delegated 中文为主，en 留 harden（未定）。
- 官网五线目录 / 导航挂接：本 change 外，待官网侧另立。
