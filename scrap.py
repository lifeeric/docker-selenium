from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Set up Chrome options
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run headless if you don't need a UI
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--remote-debugging-port=9222")  # Allows for debugging
options.add_argument("--disable-gpu")  # Disable GPU acceleration
options.add_argument("--window-size=1920x1080")  # Set a default window size


print("[Started]")

# Create a new Chrome session
driver = webdriver.Chrome(options=options)

try:
    # Navigate to the desired webpage (replace with your target URL)
    print("[Visisting page.]")

    driver.get("https://news.yahoo.com/")  # Change this to your actual URL

    # Wait for the page to load
    time.sleep(
        3
    )  # Adjust if necessary; consider using WebDriverWait for better handling

    # Search for the specific text in the h2 element
    try:
        element = driver.find_element(By.XPATH, "//h2[text()='Stories for you']")

        print("[Scraped data]:", element.text)
    except Exception as e:
        print("Element not found:", e)

finally:
    # Close the driver
    driver.quit()
    print("[Exited]")
