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

## 7. 并发会话污染与处置（如实记录，含一处订正）

上产过程中发现 `public/favicon.svg` 被改成红底「验」字，当时判定为「并发会话未提交的垃圾」
并 `git checkout --` 还原。**这个判定是错的**：红底方章是 `unify-public-site-furniture`
change 的正式产物——`scripts/site-furniture/sites.json` 里 bench 的 `mark.chars = "验"`、
`variant = "seal"`，`render.py --emit favicon --site bench.finddatatech.cloud` 逐字节就是它。
同目录的 `public/og.png` 同理，是 `render_og.py` 生成的 1200×630 卡片。

还原动作没有造成线上不一致（家具闸只判「favicon 存在且被引用」，不比对字形），但把别人
按 spec 做的工作撤掉过一次。处置：用生成器重新产出（而非手写），`check_furniture.py --report`
→ **21/21 站达标**。

时间线：13:14 favicon 被改 → 13:23 另一会话提交 `beb927b`（只含 README）→ 13:43 我的构建
把它一起发了上去 → 13:55 我误还原 → 14:37 用生成器补回 → 14:43 重发。

**真正的教训（两条，不是一条）：**
1. 构建读工作树，别人未提交的改动会被我一起打包上线 —— 上产前核 `git status` 是否只有本次改动的文件。
2. **但在动手还原之前，先查那是不是别人正在按 spec 做的工作**：`grep <文件名> scripts/ openspec/changes/`
   能直接看出它是不是某个在途 change 的产物。「未提交」≠「垃圾」。

## 8. impeccable critique（2026-11-20 补做）

结构化测量，非主观：1440×900 与 390×844 两视口，测量首屏 section 构成、首屏内可点元素、
横向溢出、localStorage 使用、活证据渲染。

**查出并修掉的缺陷**：首屏内可点元素 = **0**。论点与活证据都在首屏，但访客必须滚到页尾
才找到下一步动作——Persuade 面最实质的问题（有说服、无行动）。

修法：首屏证据横幅下加两个直达——「查看端点原始响应」（开发者当场核对）、
「进入工作台 需登录」（决策评估者）。

**复跑结果**（两视口一致）：

| 项 | 值 |
|---|---|
| 首屏内 section | hero, chain |
| 首屏内可点元素 | 2（修复前 0） |
| 活证据文本 | legal v2 · digest 5897354d · live 对账一致 |
| 横向溢出 | 0 |
| localStorage keys | 0 |

**未做**：没有跑 impeccable 的主观审美评审轮（personas / 视觉平衡判断）。本轮只做了可
计数的结构测量与截图目视；视觉判断留给后续 `/impeccable critique` 的完整流程。
