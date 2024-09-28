import os
import json
import argparse
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()

# Set up Chrome options
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run headless if you don't need a UI
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")  # Disable GPU acceleration
options.add_argument("--window-size=1920,1080")  # Set a default window size

SESSION_FILE_NAME = "session/session.json"


def store_session(driver: webdriver.Chrome) -> None:
    """
    Saves the current Chrome session cookies to a JSON file, overwritten if it already exists.

    :param driver: The Chrome driver to save cookies from.
    :type driver: webdriver.Chrome
    """

    cookies = driver.get_cookies()
    cookies = {
        "cookies": cookies,
        "url": driver.current_url,
    }
    os.makedirs("session", exist_ok=True)

    with open(SESSION_FILE_NAME, "w") as f:
        json.dump(cookies, f)

    print("[Cookies saved]")


def load_session(driver: webdriver.Chrome) -> str:
    """
    Loads cookies from a JSON file and adds them to driver.

    :param driver: The Chrome driver to load cookies into.
    :type driver: webdriver.Chrome
    :return: The loaded cookies, as a dictionary.
    :rtype: returns a url
    """
    with open(SESSION_FILE_NAME, "r") as f:
        cookies = json.load(f)

    for cookie in cookies.get("cookies", []):
        driver.add_cookie(cookie)

    driver.refresh()

    return cookies.get("url", "")


def runner(URL: str, target: str) -> None:
    """
    Runs a series of tasks on the given Chrome driver.

    :param url: The URL to visit.
    :type url: str
    """

    try:
        driver = webdriver.Chrome(options=options)

        print(f"[Visisting]: {URL}")
        driver.get(URL)

        if os.path.exists(f"session/{SESSION_FILE_NAME}"):
            print("[Loading Session]")
            dashboard_url = load_session(driver)
            driver.get(dashboard_url)

        else:
            # Login
            WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located((By.ID, "txtCompanyName"))
            ).send_keys(os.getenv("COMPANY_NAME"))

            driver.find_element(By.ID, "txtUserName").send_keys(os.getenv("EMAIL"))
            driver.find_element(By.ID, "txtUserPass").send_keys(os.getenv("PASS"))
            driver.find_element(By.ID, "MainContent_loginUI_cmdLogin").click()

            store_session(driver)

        # Select Role
        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.ID, "evrDialog-button"))
        ).click()

        # Locating Menu and going to Location
        WebDriverWait(driver, 15).until(
            EC.visibility_of_all_elements_located(
                (
                    By.CLASS_NAME,
                    "FeatureToolbarButton.EverestHamburger.everest-menu-toggle",
                )
            )
        )[0].click()

        WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'Org Setup')]"))
        ).click()

        WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'Locations')]"))
        ).click()

        # Location Types
        if target == "types":

            WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//span[contains(text(),'Location Types')]")
                )
            ).click()

            table = WebDriverWait(driver, 15).until(
                EC.visibility_of_any_elements_located(
                    (By.CLASS_NAME, "dgrid-row.ui-state-default.dgrid-row-odd")
                )
            )

            rows = table[0].find_elements(By.CSS_SELECTOR, "tr")

            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")

                for cell in cells:
                    print(f"[✅ Data]: {cell.text.strip()}")
        else:
            # Location Properties

            WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//span[contains(text(),'Location Properties')]")
                )
            ).click()

            tables = WebDriverWait(driver, 15).until(
                EC.visibility_of_any_elements_located(
                    (By.CLASS_NAME, "dgrid-row.ui-state-default")
                )
            )

            for table in tables:
                rows = table.find_elements(By.CSS_SELECTOR, "tr")

                for row in rows:
                    cells = row.find_elements(By.TAG_NAME, "td")

                    for cell in cells:
                        print(f"[✅ Data]: {cell.text.strip()}")

        driver.quit()
        print("[Done]")
    except KeyboardInterrupt:
        print("[Ctr + c]")
        pass


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--target", type=str, required=True, help="eg: types or properties"
        )
        args = parser.parse_args()

        print("[Started]")
        URL = "https://usstage241.dayforcehcm.com/MyDayforce/u/X5u8jynQL0GANx00a1oH1A/Common/"

        runner(URL, args.target)
    except KeyboardInterrupt:
        print("[Ctr + c]")
