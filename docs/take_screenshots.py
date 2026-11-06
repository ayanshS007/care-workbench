"""Re-make the README screenshots: python docs/take_screenshots.py
Needs Python, Playwright and Pillow. Set PLAYWRIGHT_CHROMIUM_PATH to use a custom browser."""
import os, io, pathlib
from playwright.sync_api import sync_playwright
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "screenshots"
SHOTS = [("01-my-day", "#/day", False), ("00-my-day-explained", "#/day", True), ("02-prepare", "#/member/P1", False),
         ("03-care-plan", "#/member/P1/plan", False), ("04-call-notes", "#/call/P1", False), ("05-data-trust", "#/trust", False),
         ("06-care-map", "#/map", False), ("07-caseload", "#/caseload", False)]

OUT.mkdir(parents=True, exist_ok=True)
with sync_playwright() as p:
    exe = os.environ.get("PLAYWRIGHT_CHROMIUM_PATH")
    b = p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
    pg = b.new_page(viewport={"width": 1600, "height": 1000}, device_scale_factor=2)
    pg.goto((ROOT / "index.html").as_uri())
    pg.wait_for_timeout(800)
    for name, route, explain in SHOTS:
        pg.evaluate(f"location.hash='{route}'")
        pg.wait_for_timeout(500)
        pg.evaluate("(d)=>document.querySelectorAll('.flo-btn').forEach(e=>e.style.display=d?'':'none')", route == "#/day")
        if explain:
            pg.keyboard.press("e"); pg.wait_for_timeout(400)
        png = pg.screenshot()
        if explain:
            pg.keyboard.press("e"); pg.wait_for_timeout(200)
        Image.open(io.BytesIO(png)).convert("RGB").save(OUT / f"{name}.jpg", quality=82, optimize=True, progressive=True)
        print(name)
    b.close()
