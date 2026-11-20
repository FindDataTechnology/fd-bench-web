#!/usr/bin/env python3
"""端点状态陈述探针：页面文案必须与端点实测相符。

它回答一个问题：门 B / 页面上关于端点可用性的措辞，是不是还站得住？

三种输出，退出码各不相同——「跑不了」与「跑过且通过」必须可区分（本仓纪律：
门从未执行与执行且通过输出一致，会被当成绿）：

    0  相符（端点可用且页面按可用口径陈述，或端点不可用且页面已改回能力口径）
    1  不符（端点实测与页面措辞矛盾——今天就得改）
    2  未判定（网络失败/超时/载荷不符预期，判不出来）

跑法：
    python3 scripts/check_status_wording.py                 # 打线上站点
    python3 scripts/check_status_wording.py --base http://localhost:8899
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
FACTS = ROOT / "bench-site-facts.json"
OVERVIEW = "/api/public/overview"


def fetch(url: str, timeout: float = 15.0) -> tuple[int, bytes]:
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310 - fixed host from caller
            return resp.status, resp.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()
    except Exception as exc:  # noqa: BLE001 - any transport failure is "undetermined", not "pass"
        raise SystemExit(_undetermined(f"请求失败：{exc}"))


def _undetermined(reason: str) -> int:
    print(f"⚠ 未判定：{reason}", file=sys.stderr)
    print("（这不是通过——判据没跑成。修好网络或换 --base 后重跑。）", file=sys.stderr)
    return 2


def endpoint_usable(status: int, body: bytes) -> bool:
    if status != 200:
        return False
    try:
        payload = json.loads(body)
    except Exception:  # noqa: BLE001
        return False
    return (
        isinstance(payload, dict)
        and bool(payload.get("as_of"))
        and isinstance(payload.get("ontology_versions"), list)
        and len(payload["ontology_versions"]) > 0
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="https://bench.finddatatech.cloud")
    args = ap.parse_args()

    spec = json.loads(FACTS.read_text(encoding="utf-8"))
    forbidden = spec["status_wording"]["forbidden_while_live"]

    page_status, page_html = fetch(args.base + "/")
    if page_status != 200:
        return _undetermined(f"页面本身返回 HTTP {page_status}")
    page = page_html.decode("utf-8", "replace")

    api_status, api_body = fetch(args.base + OVERVIEW)
    live = endpoint_usable(api_status, api_body)

    summary = "（无有效载荷）"
    if live:
        payload = json.loads(api_body)
        counts = payload.get("totals") or {}
        vs = ", ".join(
            f"{v.get('domain_key')} v{v.get('version')} {str(v.get('digest'))[:8]}"
            for v in payload["ontology_versions"]
        )
        summary = (
            f"as_of={payload.get('as_of')} · {vs} · 实体 {counts.get('entities')} / 关系 {counts.get('relations')}"
        )
    print(f"页面 HTTP {page_status} · 端点 HTTP {api_status} · 端点可用={live}")
    print(f"载荷摘要：{summary}")

    if live:
        stale = [w for w in forbidden if w in page]
        if stale:
            print(f"✗ 端点可用，但页面仍含过渡语 {stale} —— 按实测改成可读口径。", file=sys.stderr)
            return 1
        print(f"✓ 端点可用，页面无 {forbidden} 类过渡语。")
        return 0

    # 端点不可用：页面必须已改回能力口径（此处只判「不再声称可用」，具体措辞由人复核）
    claims_live = "已上线" in page and "端点不可用" not in page
    if claims_live:
        print("✗ 端点不可用，但页面仍陈述为已上线 —— 当日改回能力口径。", file=sys.stderr)
        return 1
    print("✓ 端点不可用，页面已按能力口径陈述。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
