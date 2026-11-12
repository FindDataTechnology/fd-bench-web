"""签名运动「一锚贯之」的双向判据（bench.finddatatech.cloud）。

为什么需要它：站点首屏有三处装置靠同一个判断点亮——链路节点 ③ 的绿缘「live 对账一致」、
版本表里那一行的 `anchor-hit` 高亮。判断是
`String(v.digest || "") === ANCHOR_DIGEST`，而 `ANCHOR_DIGEST` 只有 **8 位**
（`3586552a`，对外展示用的短锚），端点返回的是 **64 位**全串。全等永远不成立，
于是这三处装置**结构性地永远不亮**——页面看着正常（表格、as_of、数字都在），
只有那枚"对上了"的绿标从不出现。2026-11-12 在线上用真浏览器实测：
`{"live": 0, "anchorHit": 0, "digestCell": "3586552a01b041b7…"}`。

这个检查因此必须**双向**：
1. 端点返回以短锚开头的 digest 时，`.live` 与 `tr.anchor-hit` 必须出现（否则是假死）；
2. 端点返回**不同** digest 时，两者必须都不出现（否则是假亮——把"对上了"变成装饰）。

跑法（用有 playwright 的解释器）：
    /Users/chengsishi/finddata/fd-industry-data/.venv/bin/python scripts/site_anchor_check.py
"""

from __future__ import annotations

import asyncio
import json
import sys
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

DIST = Path(__file__).resolve().parent.parent / "dist"
PORT = 8931

ANCHOR_PREFIX = "3586552a"
MATCHING_DIGEST = ANCHOR_PREFIX + "01b041b777db3dc6c5252b5a275c2c138395d6c4088c6025d4674203"
OTHER_DIGEST = "ffffffff" + MATCHING_DIGEST[len(ANCHOR_PREFIX):]


def _overview(digest: str) -> dict:
    return {
        "as_of": "2026-11-06T03:25:44.532532+00:00",
        "ontology_versions": [{
            "domain_key": "legal",
            "version": 1,
            "digest": digest,
            "published_at": "2026-11-06T03:25:44.532532+00:00",
            "counts": {"entities": 1, "relations": 0,
                       "by_tier": {"gold": 0, "silver": 0, "bronze": 0, "raw": 1}},
        }],
        "totals": {"domains": 1, "entities": 1, "relations": 0,
                   "by_tier": {"gold": 0, "silver": 0, "bronze": 0, "raw": 1}},
    }


def _serve() -> ThreadingHTTPServer:
    handler = partial(SimpleHTTPRequestHandler, directory=str(DIST))
    httpd = ThreadingHTTPServer(("127.0.0.1", PORT), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


async def _probe(digest: str) -> dict:
    from playwright.async_api import async_playwright

    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        page = await browser.new_page(viewport={"width": 1280, "height": 900})
        payload = json.dumps(_overview(digest))

        async def _stub(route):
            await route.fulfill(status=200, content_type="application/json", body=payload)

        await page.route("**/api/public/overview*", _stub)
        await page.goto(f"http://127.0.0.1:{PORT}/", wait_until="networkidle", timeout=60000)
        await page.wait_for_timeout(1200)
        out = await page.evaluate(
            """() => ({
                 live: document.querySelectorAll('.live').length,
                 anchorHit: document.querySelectorAll('tr.anchor-hit').length,
                 rows: document.querySelectorAll('table.versions tbody tr').length,
               })"""
        )
        await browser.close()
        return out


def main() -> int:
    if not (DIST / "index.html").exists():
        print(f"dist 不存在：先 `npm run build`（{DIST}）", file=sys.stderr)
        return 2
    httpd = _serve()
    try:
        hit = asyncio.run(_probe(MATCHING_DIGEST))
        miss = asyncio.run(_probe(OTHER_DIGEST))
    finally:
        httpd.shutdown()

    ok_hit = hit["live"] >= 1 and hit["anchorHit"] >= 1 and hit["rows"] == 1
    ok_miss = miss["live"] == 0 and miss["anchorHit"] == 0 and miss["rows"] == 1
    print(json.dumps({"matching_digest": hit, "other_digest": miss}, ensure_ascii=False))
    if ok_hit and ok_miss:
        print("PASS：锚对上才亮、对不上不亮")
        return 0
    if not ok_hit:
        print("FAIL：端点 digest 以短锚开头却没点亮（假死）——检查 ANCHOR_DIGEST 的比较方式")
    if not ok_miss:
        print("FAIL：digest 不同却也点亮（假亮）")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
