import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def navigate_to_domains(driver):
    driver.get("https://porkbun.com/account/domains")
    print("Navigated to Porkbun website.")


def scroll_and_collect_rows(driver):
    try:
        rows = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CLASS_NAME, "domainManagementRow"))
        )
        print(f"Found {len(rows)} domain rows.")
    except TimeoutException:
        print("Timed out waiting for domain rows to appear.")
        return []

    while True:
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        displayed_count = int(driver.find_element(
            By.CLASS_NAME, "domainManagementCountsDisplayedCount").text.split(" ")[0])
        total_count = int(driver.find_element(
            By.CLASS_NAME, "domainManagementCountsTotalCount").text.split(" ")[0])

        print(f"Displayed: {displayed_count}, Total: {total_count}")

        if displayed_count == total_count:
            break

    rows = driver.find_elements(By.CLASS_NAME, "domainManagementRow")
    return rows
