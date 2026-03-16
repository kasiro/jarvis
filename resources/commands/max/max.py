#!/usr/bin/env python3
import asyncio
import subprocess
import sys
from time import sleep

from jarvis_api import init_jarvis
from playwright.async_api import async_playwright


def zenity_select(prompt: str, options: list, title: str = "Выбор") -> str:
    """
    Показывает окно Zenity со списком вариантов (радиокнопки).
    Возвращает выбранную строку или None при отмене.
    """
    cmd = [
        "zenity",
        "--list",
        f"--title={title}",
        f"--text={prompt}",
        "--radiolist",
        '--column="Выбор"',
        '--column="Опция"',
    ]
    # Добавляем все опции, первую делаем выбранной по умолчанию
    for i, opt in enumerate(options):
        cmd.append("TRUE" if i == 0 else "FALSE")
        cmd.append(opt)

    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    return result.stdout.strip()


def zenity_input(title: str, prompt: str) -> str:
    cmd = ["zenity", "--entry", f'--title="{title}"', f"--text={prompt}", "--width=400"]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return result.stdout.strip()


async def send_message(page, text: str):
    search_input = page.locator(".composer .input .input .contenteditable")
    await search_input.click()
    await search_input.fill(text)
    await asyncio.sleep(0.5)
    await page.keyboard.press("Enter")


async def get_chat(page, chat_name: str):
    await page.evaluate(
        """
        (chatName) => {
            const items = document.querySelectorAll('.content .scrollListContent > .item');
            for (const item of items) {
                const nameEl = item.querySelector('.title .name .text');
                if (nameEl && nameEl.innerText === chatName) {
                    const btn = item.querySelector('button');
                    if (btn) btn.click();
                    break;  // прерываем цикл после клика
                }
            }
        }
        """,
        chat_name,
    )


async def run_browser():
    person = zenity_select("Кто обращается?", ["Савелий", "Настя"], title="Пациент")
    list_ = {
        "Савелий": [
            "педиатр",
            "лор",
        ],
        "Настя": ["терапевт", "гинеколог"],
    }[person]
    birdh = {
        "Савелий": "05.10.2023",
        "Настя": "02.07.2002",
    }[person]
    doctor = zenity_select(
        "Выберите специалиста",
        list_,
        title="Врач",
    )
    date = zenity_input(person, "введите дату записи")
    full_name = {
        "Савелий": "Каширских Савелий Данилович",
        "Настя": "Каширских Анастасия Корнеевна",
    }[person]
    # jarvis = init_jarvis({})
    p = await async_playwright().start()
    user_data_dir = "/home/kasiro/.playwright-profile-max"
    context = await p.firefox.launch_persistent_context(
        user_data_dir,
        headless=False,
        viewport=None,
    )
    page = context.pages[0] if context.pages else await context.new_page()
    await page.set_viewport_size({"width": 1920, "height": 970})

    await page.goto("https://web.max.ru/")
    await page.wait_for_load_state("networkidle")
    await asyncio.sleep(1)
    await page.wait_for_selector(".foldersViewport", timeout=20000)
    # await get_chat(page, "Мой Ангелочек")
    await get_chat(page, "Мое здоровье НСО")

    # await asyncio.sleep(9999)
    await asyncio.sleep(1)
    await send_message(page, "Записаться на приём")

    # нажать принять
    await asyncio.sleep(0.5)
    await page.evaluate(
        'document.querySelector(".openedChat .content.scrollListContent .item:last-child .button[aria-label="Принять"]").click()'
    )

    await asyncio.sleep(1.5)
    await send_message(page, "Записаться на приём")

    await asyncio.sleep(1.5)
    await send_message(page, doctor)

    await asyncio.sleep(1.5)
    await send_message(page, full_name)

    await asyncio.sleep(1.5)
    await send_message(page, birdh)

    await asyncio.sleep(2)
    await send_message(page, date)

    await asyncio.sleep(2)
    await send_message(page, "16:00")

    try:
        await asyncio.Future()
    except asyncio.CancelledError:
        await context.close()
        await p.stop()


if __name__ == "__main__":
    asyncio.run(run_browser())
