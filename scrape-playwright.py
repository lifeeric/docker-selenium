import os
import json
import asyncio
import argparse
from pathlib import Path
from dotenv import load_dotenv
from playwright.async_api import async_playwright, BrowserContext

load_dotenv()

COOKIES_FILE_PATH = "session/cookies-py.json"


async def save_cookies(context: BrowserContext, url: str) -> None:
    """
    Saves all cookies from a context to a file.

    :param context: The context whose cookies should be saved.
    :param url: The URL associated with the cookies.
    """

    os.makedirs("session", exist_ok=True)

    cookies = await context.cookies()
    with open(COOKIES_FILE_PATH, "w") as f:
        json.dump({"cookies": cookies, "url": url}, f, indent=2)


async def load_cookies(context: BrowserContext) -> str:
    """
    Loads all cookies from a file and adds them to a context.

    :param context: The context to add the cookies to.
    :return: The URL associated with the cookies.
    """
    with open(COOKIES_FILE_PATH, "r") as f:
        cookies_data = json.load(f)
    await context.add_cookies(cookies_data["cookies"])
    return cookies_data["url"]


async def runner(target):
    print("[Started]")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(viewport={"width": 1920, "height": 1080})
        page = await context.new_page()

        try:
            print("[Visiting page.]")
            await page.goto(
                "https://usstage241.dayforcehcm.com/MyDayforce/u/X5u8jynQL0GANx00a1oH1A/Common/"
            )

            if Path(COOKIES_FILE_PATH).exists():
                print("[Loading cookies]")
                url = await load_cookies(context)
                await page.goto(url)
            else:
                # Fill in the login form
                await page.fill("#txtCompanyName", os.getenv("COMPANY_NAME", ""))
                await page.fill("#txtUserName", os.getenv("EMAIL", ""))
                await page.fill("#txtUserPass", os.getenv("PASS", ""))
                await page.click("#MainContent_loginUI_cmdLogin")
                await save_cookies(context, page.url)

            # Navigate to the desired options
            await page.click("#evrDialog-button")
            await page.click(
                ".FeatureToolbarButton.EverestHamburger.everest-menu-toggle"
            )
            await page.click("//*[contains(text(),'Org Setup')]")
            await page.click("//*[contains(text(),'Locations')]")

            if target == "types":
                print("[Fetching Location Types]")
                await page.click("//span[contains(text(),'Location Types')]")

                # Wait for the table rows to be visible
                await page.wait_for_selector(
                    ".dgrid-row.ui-state-default.dgrid-row-odd", state="visible"
                )

                rows = await page.query_selector_all(
                    ".dgrid-row.ui-state-default.dgrid-row-odd tr"
                )
                for row in rows:
                    cells = await row.query_selector_all("td")
                    for cell in cells:
                        cell_text = await cell.text_content()
                        print(f"[✅ Data]: {cell_text.strip()}")

            else:
                await page.click("//span[contains(text(),'Location Properties')]")
                await page.wait_for_selector(
                    ".dgrid-row.ui-state-default", state="attached"
                )

                all_tables = await page.query_selector_all(
                    ".dgrid-row.ui-state-default"
                )
                for table in all_tables:
                    rows = await table.query_selector_all("tr")
                    for row in rows:
                        cells = await row.query_selector_all("td")
                        for cell in cells:
                            cell_text = await cell.text_content()
                            print(f"[✅ Data]: {cell_text.strip()}")

        except Exception as e:
            print("Error:", e)
        finally:
            await browser.close()
            print("[Done]")


def main():
    parser = argparse.ArgumentParser(
        description="Run the script with the types or properties target"
    )
    parser.add_argument(
        "--target", required=True, help="Specify the target: types or properties"
    )
    args = parser.parse_args()

    asyncio.run(runner(args.target))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("[Ctr + c]")
