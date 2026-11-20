# 事实闸上产验收（2026-11-20）

change `gate-bench-site-facts`；回滚点 `/opt/fd/bench-web/dist.bak-20261120-113829`。

## 1. 端点状态探针（上产前，按 design D5 记录）

- 时间：2026-11-20T03:38:17Z
- 命令：`python3 scripts/check_status_wording.py`（打线上站点）
- 结果：exit 1 —— 「端点可用，但页面仍含过渡语 ['上线中','部署收尾中']」
- 载荷摘要：as_of=2026-11-12T05:31:02Z · legal v2 5897354d · 实体 5117 / 关系 25
- 结论：端点自 11-12 起 live，旧文案陈述过期；本 change 的门 B 订正是按此实测做出的。

## 2. 上产后探针

- 时间：2026-11-20T03:44:28Z
- `python3 scripts/check_status_wording.py`：
```
  页面 HTTP 200 · 端点 HTTP 200 · 端点可用=True
  载荷摘要：as_of=2026-11-12T05:31:02.841819+00:00 · legal v2 5897354d · 实体 5117 / 关系 25
  ✓ 端点可用，页面无 ['上线中', '部署收尾中'] 类过渡语。
```

## 3. 线上产物事实闸（--from-remote）

```
  ✓ 事实闸通过：白名单 4 条全在产物中，退役值 4 条零命中。
```

线上抓取逐词命中：32,275 **0** / 43 类 **0** / 上线中 **0** / 部署收尾中 **0** / 37 个工具 **0**；
32,296 **2**（首屏 + 证据区，同口径）。

## 4. 双视口与水合

- `site_inspect.py`（本地 dist，port 8898）：desktop/mobile `h_overflow_px=0`；console 唯一
  404 是本地 http.server 没有 `/api/public/overview` 反代（预期偏差，非产物缺陷）。
- 线上真浏览器（1280×900 / 390×844）：`live=1`、`anchorHit=1`、版本表 1 行、as_of 与端点一致、
  fail-card 0、hOverflow 0、console error 0。
- `site_anchor_check.py` 双向 PASS：锚对上才亮（live 1 / anchorHit 1），对不上不亮（0 / 0）。

## 5. 判据自身的有效性（红证）

`check_facts.py --self-check` 五条夹具全过：干净绿；退役值/白名单外/两处不一致/条目缺席 四类红。
`check_status_wording.py` 双向自检：端点可用+旧过渡语 → 红；端点可用+可读口径 → 绿；网络失败 → 未判定（exit 2）。
