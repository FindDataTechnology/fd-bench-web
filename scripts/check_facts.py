#!/usr/bin/env python3
"""构建期事实闸：对 dist/ 全量判定白名单与退役值。

为什么读 dist/ 而不是 src/：需要判定的两件事——「白名单外数字」与「退役值命中」——都
只能对构建产物成立；读源码会漏掉模板拼接与构建期注入。门序因此固定为 build → 本脚本。
（design D1）

判定顺序：先 retired（命中即失败，无论是否恰等于某个白名单值），再 facts。
（design D3）

跑法：
    python3 scripts/check_facts.py                # 读 dist/index.html
    python3 scripts/check_facts.py --from-remote  # 抓线上产物后判定（上产验收用）
退出码：0 通过 / 1 失败（含「产物不存在」）。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
FACTS = ROOT / "bench-site-facts.json"
DIST = ROOT / "dist" / "index.html"
REMOTE = "https://bench.finddatatech.cloud/"

DATA_RE = re.compile(r'<data[^>]*\bvalue="(\d+)"[^>]*>([^<]*)</data>')
# 正文里的裸数字串（千分位或纯数字，≥3 位）——只用于「同事实两处口径不一致」与白名单外判定
BARE_RE = re.compile(r"(?<![\w.,])\d{1,3}(?:,\d{3})+(?![\w,])|(?<![\w.,])\d{4,}(?![\w,])")


def fail(lines: list[str]) -> int:
    for line in lines:
        print(line, file=sys.stderr)
    return 1


def load_html(from_remote: bool) -> str:
    if not from_remote:
        return DIST.read_text(encoding="utf-8")
    with urllib.request.urlopen(REMOTE, timeout=30) as resp:  # noqa: S310 - 固定 https 目标
        return resp.read().decode("utf-8")


def _check(html: str, spec: dict) -> list[str]:
    """Return the problem list for one product snapshot (pure)."""
    problems: list[str] = []

    # ① 退役值优先：出现即失败
    for item in spec["retired"]:
        hits = html.count(item["text"])
        if hits:
            problems.append(f"✗ 退役值残留：{item['text']!r} 命中 {hits} 次（{item['why']}）")

    # ② 白名单：产物中的 <data value> 必须逐一登记
    allowed = {str(f["value"]) for f in spec["facts"]}
    by_value = {str(f["value"]): f for f in spec["facts"]}
    seen_data: dict[str, int] = {}
    for value, text in DATA_RE.findall(html):
        seen_data[value] = seen_data.get(value, 0) + 1
        if value not in allowed:
            problems.append(f'✗ 白名单外数字：<data value="{value}">{text}</data>')
        elif text.strip() != by_value[value]["text"]:
            problems.append(
                f'✗ 数字与其登记文本不符：value={value} 产物文本={text.strip()!r} 白名单={by_value[value]["text"]!r}'
            )

    # ③ 每一条白名单事实都必须在产物中出现（登记了却没上页 = 白名单与页面漂移）
    for f in spec["facts"]:
        if str(f["value"]) not in seen_data:
            problems.append(f"✗ 白名单条目未出现在产物中：{f['id']}（{f['text']}）")

    # ④ 「同一事实两处口径不一致」由 ① + ② 联合覆盖：旧值命中 retired、新值未登记则命中白名单外，
    #    两者都失败——spec 的判据正是「两处中至少一处被判为白名单外或退役值」。不另做正文裸数字扫描：
    #    正文里合法地会复述数字（出处注），按形态扫会产生假阳性。
    return problems


def _self_check(spec: dict) -> int:
    """夹具自检：确认这道闸对「能过」与「该红」都成立（红证纪律）。"""
    clean = "".join(f'<data value="{f["value"]}">{f["text"]}</data>' for f in spec["facts"])
    retired_text = spec["retired"][0]["text"]
    cases = [
        ("干净产物", clean, False),
        ("退役值残留", clean + f"<p>{retired_text}</p>", True),
        ("白名单外数字", clean + '<data value="9999">9,999</data>', True),
        # 同事实两处口径不一致：首屏旧的 retired 值 + 证据区的新值并存
        ("同事实两处不一致", clean + f"<p>{retired_text} 部</p>", True),
        ("白名单条目缺席", clean.replace(f'<data value="{spec["facts"][0]["value"]}">', "<span>"), True),
    ]
    bad = 0
    for name, html, should_fail in cases:
        got = bool(_check(html, spec))
        ok = got == should_fail
        print(f"{'✓' if ok else '✗'} 夹具[{name}] 期望{'红' if should_fail else '绿'} 实得{'红' if got else '绿'}")
        bad += 0 if ok else 1
    return 1 if bad else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--from-remote", action="store_true", help="抓线上产物判定（上产验收）")
    ap.add_argument("--self-check", action="store_true", help="跑夹具自检（判据本身是否有效）")
    args = ap.parse_args()

    spec = json.loads(FACTS.read_text(encoding="utf-8"))
    if args.self_check:
        return _self_check(spec)

    try:
        html = load_html(args.from_remote)
    except FileNotFoundError:
        return fail([f"✗ 构建产物不存在：{DIST}（先跑 npm run build）"])
    except Exception as exc:  # noqa: BLE001 - 抓取失败要区分「未判定」而不是「通过」
        return fail([f"✗ 无法取得产物：{exc}"])

    problems = _check(html, spec)
    if problems:
        return fail(problems + [f"\n共 {len(problems)} 处问题。"])
    print(f"✓ 事实闸通过：白名单 {len(spec['facts'])} 条全在产物中，退役值 {len(spec['retired'])} 条零命中。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
