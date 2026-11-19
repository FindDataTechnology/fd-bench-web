# Product

<!-- impeccable:product-schema 1 -->

> 推断项标注：**Stack**（Astro 静态，随 `fd-qicai-web` 先例）与**语言轨**（zh-first，en 另立）为本轮 delegated 项，沿 proposal/design 已裁决定记；其余源自 change `add-bench-chain-website` 的 proposal/design/spec 与本会话核实的事实账本。

## Platform

web

## Stack

delegated: Astro（静态构建，随 `fd-qicai-web` 先例；Caddy `file_server` 直出 `/opt/fd/bench-web/dist`，`/api/public/overview` 同源反代 bench 公共 pod）。理由：单页 Persuade 面 + 活水合脚本，依赖版本与构建形态直接复制启材例；不做多页路由（design D1）。

## Users

两类**同级**访客（design D2 两扇门）：

- **门 A · 决策评估者**：在评估这条分发链值不值得信、值不值得接入的人（法务科技选型、合作尽调、内部立项）。job=看懂「知识沉淀 → 发布 → 柏讯消费」链路，并看到**可核对的证据**（评测语料规模、资产分类、质量分层、评审环、已发布 digest）。成功动作=到达证据面并核对至少一项真证据。
- **门 B · 智能体开发者**：要让 agent 消费 bench 发布的本体知识的人。job=拿到匿名概览端点、当场复现一次调用、搞清认证边界。成功动作=复制端点 + 跑通 curl 试令。

## Product Purpose

bench（知验台）与柏讯本体在官网零存在——bench 只有一张 repo 卡 + 一篇研究文章，官网上「本体」一词还与壹座开放数据本体撞名。本站是这条分发链的唯一门面：传达层 0 论点——

> **竞争不在模型，在知识的沉淀与复利——评测出的知识以本体形态发布，多端消费。**

并把「人和智能体读同一份台账」做成可当场验证的体验：页面数字活拉自匿名概览端点（带 `as_of`），失败如实报因。成功=访客理解链路 + 门 A 到达证据面 + 门 B 当场跑通试令。

**口径纪律（add-bench-wire-seam-contract）**：沉淀与发布两段在产（有已发布 digest 与实时端点可核）；**消费端按能力口径表述**——「接入能力已交付、生产订阅尚未开启」。改回「已上线」需同时满足两个条件：① 生产订阅开启且 `bench_pull_log` 有持续成功足迹；② 消费方侧存在可见的拉取读面。只满足其一时 MUST NOT 声称「正在订阅/已上线」。

## Positioning

邻品抄不走的机制：**沉淀与发布这一段已经上产**。知识沉淀端是法条锚定的评测基座（32,296 部法规目录、66 类母版模板其中 41 类带种子条款、判官评审环自愈迭代）；发布端是版本化发布-拉取契约（legal v2 已发布，digest `5897354d`，5,117 实体）。消费端消费能力已交付（拉取客户端 / 幂等落库 / 只读投影），生产订阅未开启——措辞随「口径纪律」的两个条件浮动。结构装置「**链路三节图 + 实时概况带**」把「证据台账」从工作台内部语汇翻成对外可核对的门面——数字不是口号，是端点返回。

## Operating Context

- 域名 bench.finddatatech.cloud（雷池并入既有 site → Caddy `file_server` + 同源代理；design D4 全链参数）。
- 数据源 = law-bench change `add-bench-public-overview-tier` 的匿名概览端点 `GET /api/public/overview`（载荷：`as_of` + `ontology_versions[]`（domain/version/digest/published_at/counts 含 gold/silver/bronze 分层）+ `totals`；故障 503 带 `{"error","reason"}`，429 带 `Retry-After`）。**该端点由上游 change 提供后本站即其第一个消费者；端点未 live 期间站点水合区以报因态呈现亦诚实（proposal 已裁）。**
- 本站不做 bench 全产品文档（docs 归 `law-bench` / `fd-coding-law-bench-mcp` 的 mkdocs）；不做官网导航挂接（另立）。

## Capabilities and Constraints

- **水合数字 MUST 来自实时端点**（同源 `/api/public/overview`），MUST NOT 硬编任何版本/计数/分层/`as_of`；失败 MUST 如实报因（状态码 + reason），MUST NOT 回退旧值、不摆拍、**不做 localStorage 缓存**（首查与缓存命中同口径，design D3）。
- **静态事实数字 MUST 带 `as_of` 口径标注且出处可指名**（Facts 白名单见 `.impeccable/surfaces/bench-site.md`）；白名单外数字拒绝上页。
- **「本体」语义在本站专指 bench↔wire 分发链的本体资产**；壹座开放数据本体的数字（452 指标概念 / 24,395 概念等）禁挪用。
- code-led：无摄影图资产（台账扉页世界靠字体 + 1px 规则 + 单点蓝 + 分层色票）。
- 语言轨：delegated 中文为主；en 留 harden 阶段（v1 沿启材 zh-first 先例）。

## Brand Commitments

- 名 **知验台**（bench）；母品牌 **寻数**；产品线 **识律**（法律 AI）；消费端 **柏讯**（fd-wire）。
- 视觉世界方向（binding，工艺见 DESIGN.md）：**证据台账的扉页**——承接 law-bench 工作台 "The Evidence Ledger"（`law-bench/DESIGN.md` Creative North Star）材质语言，按 Persuade 面重述；与启材「编目卡抽屉」世界区隔不复用。

## Evidence on Hand

（每条有名有姓，详证见 `.impeccable/surfaces/bench-site.md` Facts 节）

- 32,296 部法规目录（现网 `law_catalog.laws` 行数，2026-11-12 实测；2026-09 刷新时为 32,275）。
- 66 类合同母版模板、其中 41 类带种子条款（`list_contract_types()` 实枚举 / `data/clause_seeds/*.yaml` 实计，2026-11-12）。
- 54 个 MCP 工具（现网 `tools/list` 实枚举，2026-11-12；README 旧记 37 已订正）。
- 4 类知识资产：本体 / RAG / 评测资产（尺子）/ 微调数据（`law-bench/docs/knowledge-platform-blueprint.md` §二）。
- legal v2 已发布，digest `5897354d`（5,117 实体 / 25 关系，2026-11-12）；v1 `3586552a` 为 2026-11-06 联调冒烟（1 实体），按追加式保留可取用。wire 跨 ns 真拉落库幂等**在 2026-11-06 联调时验证过**（C3 `add-knowledge-distribution-contract`，`knowledge-platform-blueprint.md` 分发链表）；此后生产订阅未开启——这是一条历史证据，不是当前运行态。
- ontology-builder 五岗舰队（本体盘账员 / 本体建模师 / 纪律校验闸 / 声明提案员 / 台账主编；wire-ops 全只读 + 提案制人工确认，`fleet-packs/blueprints/ontology-builder/blueprint.json` + `fleet-packs/README.md`）。
- 判官评审环 `generate → fill → evaluate → improve` 自愈管线（`law-bench/README.md` §能力表）。

## Success Criteria（对应 tasks 3.3 验收四 criteria）

1. **首屏即链路**：不滚动可见链路叙事与至少一项真证据（已发布 digest / 版本号，活水合或 `as_of` 标注快照），而非泛化口号。
2. **门 B 试令可执行**：访客照页面复制端点、跑 curl 即得端点真实响应（或如实报因），认证边界（概览匿名 / 全量需 key / MCP）在页内自洽。
3. **Facts 全部有出处**：页面每一条事实性数字都能在 surface brief 白名单里指名出处；白名单外数字为零。
4. **失败报因可复现**：端点不可达 / 非 200 / 429 时，数据区渲染报因卡（状态码 + reason），无任何旧缓存数字或摆拍数据；两次加载口径一致（无 localStorage）。
