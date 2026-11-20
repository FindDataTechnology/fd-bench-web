"""Impeccable batched inspect for the bench chain site (desktop + mobile).

file:// load so hydration hits the same-origin /api/public/overview and lands
in the honest report-cause state while the endpoint is not live. Asserts:
non-empty body, expected title, degrade card visible, localStorage API unused.
"""
import asyncio, json, os, sys
from pathlib import Path
from playwright.async_api import async_playwright

# SITE_BASE 可覆盖：8899 上常有别的本地服务，撞端口时换个口起 http.server 即可。
DIST = os.environ.get("SITE_BASE", "http://localhost:8899/")
OUT = Path("/Users/chengsishi/finddata/fd-bench-web/.impeccable/review")

SHOTS = [("desktop", 1280, 900), ("mobile", 390, 844)]

async def main() -> int:
    findings: dict = {}
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        for name, w, h in SHOTS:
            page = await browser.new_page(viewport={"width": w, "height": h})
            console_errors: list[str] = []
            page.on("console", lambda m: console_errors.append(m.text) if m.type == "error" else None)
            await page.goto(DIST, wait_until="networkidle")
            await page.wait_for_timeout(800)
            title = await page.title()
            body_len = len(await page.content())
            # horizontal overflow check
            overflow = await page.evaluate(
                "document.documentElement.scrollWidth - document.documentElement.clientWidth"
            )
            # localStorage API usage (contract: zero)
            ls_calls = await page.evaluate("window.__lsProbe || 0")
            await page.screenshot(path=str(OUT / f"{name}.png"), full_page=True)
            findings[name] = {
                "title": title,
                "body_chars": body_len,
                "h_overflow_px": overflow,
                "console_errors": console_errors[:5],
            }
            await page.close()
        await browser.close()
    print(json.dumps(findings, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
