# 落地页刷新上产验收（2026-11-20）

change `refresh-bench-landing`。回滚点 `/opt/fd/bench-web/dist.bak-20261120-133004`。

## 1. 首屏活证据（tasks 1.x）

线上真浏览器实测（桌面 1440×900 / 移动 390×844）：

```
首屏横幅（#hero-fact）在折叠线内：两视口均 true
成功态文本：发布面 · 活拉 | legal v2 | digest 5897354d
            | as_of 2026-11-12T05:31:02.841819+00:00 | live 对账一致
```

**三态等高（design D3 的判据 ≤4px）：**

| 视口 | 成功 | 失败 | 加载中 | 最大差 |
|---|---|---|---|---|
| desktop 1440×900 | 108px | 108px | 108px | **0px** |
| mobile 390×844 | 140px | 140px | 140px | **0px** |

> 首版 `min-height: 74px` 实测差 29px（成功态两行），改为 92 仍差 16px，最终 108/140 归零。
> 这是真跑出来的，不是估的。

**同源（design D2）**：网络面板只出现一次 `/api/public/overview` 请求（200），首屏横幅与
概况带由同一份响应渲染，无第二条取数路径。

## 2. 链路卡视觉执行（tasks 2.x）

| 判据 | 实测 |
|---|---|
| 三卡等高 | 346 / 346 / 346，差 0px |
| 连接线为真实元素 | `.arrow` 28×1px 横线 + 线尾箭头（原为 13×35 的字符） |
| 分层色票 | `.tierline .tier` 从 43/58/58px（8px 圆点）变为 54/69/69px（tint 底 + 文字） |
| 出处注分层 | 11.52px mono muted（既有值已达标，未改） |
| 双视口溢出 | desktop 0 / mobile 0 |

## 3. 访客下一步（tasks 3.x）

- 门 A 的 `href="#evidence"` 伪动作：产物中命中 **0**（已替换为
  「进入工作台」→ `https://lawbench.finddatatech.cloud/d` + 「需登录」标注）。
- 匿名访问该地址实测 **302 → /auth/login**，与页面「需登录」标注一致。
- 门 B 端点 + curl 试令未改动。

## 4. 事实闸（tasks 4.x）

```
$ python3 scripts/check_facts.py --self-check   # 5 条夹具 1 绿 4 红
$ python3 scripts/check_facts.py                # ✓ 白名单 4 条全在，退役值 4 条零命中
$ python3 scripts/check_facts.py --from-remote  # ✓ 同上（线上产物）
```
线上逐词命中：32,275 / 43 类 / 上线中 / 部署收尾中 / 37 个工具 均 **0**。

## 5. 文档（tasks 5.x）

- `PRODUCT.md`：Users 段保留两扇门，新增「本站之外还有一个运营面」段说明工作台需登录，
  与门 A 入口一致。
- `.impeccable/surfaces/bench-site.md`：STORY 与 FIRST VIEWPORT 两段按实现更新
  （首屏横幅、连接线、门 A 改工作台入口）；Direction Contract / Facts / 圈禁清单未动。
- `law-bench-internal/PRODUCT.md` 的「A solo operator」**未改**——那是另一仓的文档，
  归 `console-progress-and-value` 处理。

## 6. 上线后完整验收

```
事实闸 --from-remote     ✓
状态探针                 ✓ 端点可用，页面无过渡语
真浏览器水合             live=1  anchorHit=1  版本表 1 行  console error 0
localStorage 调用         0
h_overflow_px            desktop 0 / mobile 0
```

## 7. 并发会话污染与处置（如实记录）

上产过程中发现 `public/favicon.svg` 被改成红底「验」字——**不是本 change 的改动**。
时间线：13:14 该文件被改（本会话当时在写门 A），13:23 另一会话提交 `beb927b`（只含
README），13:43 我的构建把这枚未提交的 favicon 一起发了上去。

处置：`git checkout -- public/favicon.svg` 还原 → 重构建 → 重上产；线上 favicon 已确认
回到原版（`viewBox="0 0 32 32"` 的台账纸卡图标）。

**教训**：构建产物来自工作树，别人未提交的改动会被我一起发出去。上产前应核
`git status` 是否只有本次改动的文件。
