# DESIGN — 知验台分发链介绍站（bench.finddatatech.cloud）

> 建成回写（2026-11-07，随 change `add-bench-chain-website` tasks 1.3）。方向契约见
> `.impeccable/surfaces/bench-site.md`；本文件记录建成后真世界，供后续 refine/extract 消费。

## World: 证据台账的扉页（the Evidence Ledger, title page）

- **Mode**: Persuade。单页 `index.astro` 承重（design D1：链路叙事一页讲完，深度内容外链）。
- **承接与区隔**: 承接 law-bench 工作台 **"The Evidence Ledger"**（`law-bench/DESIGN.md`）的材质语言，
  按 Persuade 面重述——工作台是「操作者的账本」（密、静、功能优先），本站是「账本的对外扉页」（
  论点、链路、证据的展示性排版）。与启材「编目卡抽屉」世界区隔不复用。
- **材质（No-Gloss Rule 全盘照搬，平由信念而定）**: Ledger Gray `#f6f7f9` 哑光纸底 /
  Panel White `#ffffff` 面板 / 1px Rule Gray `#e2e5ea` 全包边；零阴影、零渐变、零装饰、无 hero 图。
  dark 方案整组反转（纸 `#14181f` / 墨 `#e6eaf0`，分层色票全体提亮）。
- **色**: 单点强调 **Bench Blue** `#2563eb`（链路锚 / 主按钮 / 链接，rarity is the point）；
  语义色只作状态——Verdict Green `#047857`（可验证 / live 对账一致）、Objection Red `#dc2626`（报因卡）；
  质量分层色票（tint + 文字成对出现，沿工作台 Tint Verdict Rule）：
  gold `#92400e`/`#fdf6ec` · silver `#475569`/`#f1f5f9` · bronze `#7c2d12`/`#fbf3ee`。
- **字**: Noto Serif SC（display：H1/节点标题/区块标题，台账扉页铅字感，700）、
  Noto Sans SC（body 400/500）、JetBrains Mono（一切机器数据：digest、as_of、端点、表值、评审环流程）。
  @fontsource 本地子集，无外部字体依赖。

## Signature: 一锚贯之（live 对账）

链路第③节「柏讯消费」内嵌 digest 证据锚（legal v2 `5897354d`，mono 小字块）；实时概况带的版本表
渲染同一 digest。**水合成功且 digest 与端点一致时**，两处同挂绿缘「live 对账一致」标（`.node.live`）——
叙事里的证据与端点返回的证据互认，是全站唯一签名运动；失败态两处都不亮，绝不假装对上。

## Data discipline（本站的「不伪装」红线）

- 概况带数字全部来自同源 `/api/public/overview`（as_of 同显），**禁止硬编任何版本/计数/分层**。
- 水合失败 → 数据区报因卡（HTTP 状态码 + reason 文案，Objection Red tint）；不回退旧值、不摆拍。
- **不做 localStorage 缓存**：首查与「缓存命中」本不存在两口径，新鲜度完全由端点 as_of 表达（design D3）。
- 静态证据数字（32,275 部法规 / 43 类合同 / 37 工具）一律 `<data>` + `as_of` 口径 + 出处注，
  白名单外数字拒绝上页（`.impeccable/surfaces/bench-site.md`）。

## Structure

`index.astro`：hero（层 0 论点：竞争不在模型，在知识的沉淀与复利）→ 链路三节图（① 知识沉淀
② 本体发布 ③ 柏讯消费【digest 证据锚，消费节点锚真证据是 D2 钉的位】，节点间 mono 箭头）→ 实时概况带（水合数据区：stats 胶囊 +
版本表 domain/version/digest/published_at/counts 分层 + as_of；SSR 态仅「正在连接…」）→ 证据区
（门 A：四类资产卡 + 质量分层 + 判官评审环 + 静态事实数字）→ 动作区两扇门（门 A 回看证据面 /
门 B copy 端点 + curl 试令 + 认证说明）→ footer（认证口径与归属）。
部署：cheap-1 `/opt/fd/bench-web/dist`（Caddy `file_server` + `handle /api/public/overview` 反代
公共 pod，超时 10s、失败透传非 200、不缓存；SafeLine 443 → Caddy，design D4 全链参数）。

## Verified

-（待 tasks 3.3 验收后回填：桌面+移动 critique/audit 结论、四 criteria 结果、公网全链。）
