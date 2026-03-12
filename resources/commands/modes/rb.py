#!/usr/bin/env python3
import asyncio
from time import sleep

# from jarvis_api import init_jarvis
from playwright.async_api import async_playwright


async def run_browser():
    # jarvis = init_jarvis({})
    p = await async_playwright().start()
    user_data_dir = "/home/kasiro/.playwright-profile"
    context = await p.firefox.launch_persistent_context(
        user_data_dir,
        headless=False,
        viewport=None,
    )
    page = context.pages[0] if context.pages else await context.new_page()
    await page.set_viewport_size({"width": 1920, "height": 1080})

    await page.goto("https://www.youtubekids.com?hl=ru")
    await page.wait_for_load_state("networkidle")
    await asyncio.sleep(1)
    await page.wait_for_selector("#input", timeout=20000)
    await page.fill("#input", "синий трактор")
    await page.keyboard.press("Enter")

    await page.wait_for_load_state("networkidle")
    await asyncio.sleep(2)

    await page.wait_for_selector(
        'ytk-compact-video-renderer[data-index="tile-0"]',
        state="attached",
        timeout=15000,
    )
    await page.evaluate(
        "document.querySelectorAll('ytk-compact-video-renderer[data-index=\"tile-0\"] a')[1].click()"
    )

    # FIX: page.focus + page.keyboard.press, page.evaluate.click, page.click не работают правильно

    # await page.focus("#player-play-pause-button")
    # jarvis.environment.press_tab(3)
    # await asyncio.sleep(9999)

    # await page.wait_for_selector("#player-fullscreen-button", timeout=15000)
    # await asyncio.sleep(3)
    # await page.click("#player-fullscreen-button")

    # await page.evaluate("document.querySelector('#player-fullscreen-button').click()")

    # await page.focus("#player-fullscreen-button")
    # await page.keyboard.press("Enter")

    try:
        await asyncio.Future()
    except asyncio.CancelledError:
        await context.close()
        await p.stop()


if __name__ == "__main__":
    asyncio.run(run_browser())
