# bench chain site 验收报告（2026-11-07）

 impeccable 有界流程：构建全量 → 一次批量检视（桌面 1280×900 + 移动 390×844）→ 一次批量修 → 一轮确认。截图：`.impeccable/review/{desktop,mobile}.png`。

## 可计数 criteria（tasks 3.3 四条）

| # | criterion | 结果 | 证据 |
|---|-----------|------|------|
| 1 | 首屏链路 | **PASS** | 层 0 论点 + 链路三节（沉淀→发布→消费）+ C3 真证据锚（legal v1 · digest 3586552a，as_of 口径标注）在首屏；两视口截图可核 |
| 2 | 门 B 试令可执行 | **PASS（结构）** | copy 端点按钮 + `curl -fsS` 试令 + 认证口径说明在场；curl 命令与冻结端点路径 `/api/public/overview` 一致。**真值执行挂账**：待上游 `add-bench-public-overview-tier` 公共 pod live 后随 tasks 4.5 复验 |
| 3 | Facts 全部有出处 | **PASS** | 每条事实性数字带 `<data value>` + as_of + 出处注（law-bench PRODUCT.md/README、blueprint §二、blueprint C3 行、fleet-packs blueprint.json）；dist 断言：禁编造数字（452/24,395）零命中；`localStorage` API 调用零次 |
| 4 | 失败报因可复现 | **PASS** | 端点不可达时数据区渲染报因卡（本检视实测两态：`Failed to fetch`（file://）与 `HTTP 404`（http.server）），无假数据、无旧缓存回落；`as_of 未取得` 如实标注 |

## 检视发现与修复（一轮批量修）

| 发现 | 严重度 | 修复 |
|------|--------|------|
| 移动端横向溢出 186px：门 B `pre.snippet`（white-space: pre）min-content ≈498px 撑爆 1fr 门卡列 | P1 | `global.css` 追加：`.door-grid > .door { min-width: 0; max-width: 100% }`、`.snippet { overflow-x: auto }`、`.endpoint-row { flex-wrap: wrap }` |
| file:// 检视时 CSS 未加载（Astro 绝对路径 `/_astro/`） | 检视方法问题，非产物缺陷 | 检视改走 `http.server`（`scripts/site_inspect.py` 指向 origin）；生产 Caddy 部署不受影响 |

## 确认轮

- 桌面 `h_overflow_px: 0`、移动 `h_overflow_px: 0`；标题串、报因卡、curl 片段（可横向滚动）、端点 chip（换行）复验通过。
- 停轮：无第四轮。

## 挂账（如实）

- 活水合真值渲染（版本表/计数/分层/as_of 与端点逐字段一致）待端点 live 后随 tasks 4.5 验收。
- OG 卡图（og-hero.png）尚未产出——上线前补（不影响功能验收）。
- DNS/雷池/Caddy 上产链（tasks 4.1-4.5）未执行。

## 检视环境

`scripts/site_inspect.py`（playwright headless chromium，viewport 1280×900 / 390×844，full-page 截图 + h_overflow 探针 + console error 收集 + localStorage 探针）。
