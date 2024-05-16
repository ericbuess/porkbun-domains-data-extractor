import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException, ElementNotInteractableException


def get_domains(driver):
    driver.get("https://porkbun.com/account/domains")
    print("Navigated to Porkbun website.")

    try:
        rows = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CLASS_NAME, "domainManagementRow"))
        )
        print(f"Found {len(rows)} domain rows.")
    except TimeoutException:
        print("Timed out waiting for domain rows to appear.")
        return {}

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
    print(f"Found {len(rows)} domain rows.")

    try:
        with open("domains.json", "r") as file:
            domains = json.load(file)
    except FileNotFoundError:
        domains = {}

    def process_row(row):
        try:
            market_column = row.find_element(
                By.CLASS_NAME, "domainManagementDomainRowCell")
            if "$" in market_column.text:
                domain_name = row.find_element(
                    By.CLASS_NAME, "domainManagementDomainName").text.split(" ")[0]
                # print(f"Extracted domain name: {domain_name}")

                if domain_name not in domains:
                    try:
                        market_link = market_column.find_element(
                            By.TAG_NAME, "strong")
                        driver.execute_script(
                            "arguments[0].click();", market_link)
                        print("Clicked market link to open the modal.")
                    except ElementClickInterceptedException:
                        print("Element click intercepted. Trying to close the modal.")
                        try:
                            modal = driver.find_element(
                                By.ID, "modal_marketplace")
                            close_button = modal.find_element(
                                By.CLASS_NAME, "close")
                            driver.execute_script(
                                "arguments[0].click();", close_button)
                            print("Closed the modal.")
                        except NoSuchElementException:
                            print("Modal not found. Skipping to the next row.")
                            return

                    try:
                        modal = WebDriverWait(driver, 20).until(
                            EC.visibility_of_element_located(
                                (By.ID, "modal_marketplace"))
                        )
                        print("Modal appeared.")

                        price_input = modal.find_element(
                            By.ID, "modal_marketplace_price")
                        domain_price = price_input.get_attribute("value")
                        print(f"Extracted domain price: {domain_price}")

                        blurb_textarea = modal.find_element(
                            By.ID, "marketplaceBlurbFormContent")
                        domain_blurb = blurb_textarea.get_attribute("value")
                        print(f"Extracted domain blurb: {domain_blurb}")

                        try:
                            min_offer_input = modal.find_element(
                                By.ID, "marketplaceOfferInput")
                            min_offer = min_offer_input.get_attribute("value")
                            if min_offer and float(min_offer) > 0.00:
                                domain_data = {
                                    "price": domain_price,
                                    "blurb": domain_blurb,
                                    "minOffer": min_offer
                                }
                            else:
                                domain_data = {
                                    "price": domain_price,
                                    "blurb": domain_blurb
                                }
                        except NoSuchElementException:
                            domain_data = {
                                "price": domain_price,
                                "blurb": domain_blurb
                            }

                        domains[domain_name] = domain_data
                        print(
                            f"Added domain data to domains dictionary: {domain_name}")

                        with open("domains.json", "w") as file:
                            json.dump(domains, file, indent=4)
                            print(f"Updated domains.json with {domain_name}")

                        close_button = modal.find_element(
                            By.CSS_SELECTOR, "button.close[data-dismiss='modal']")
                        driver.execute_script(
                            "arguments[0].click();", close_button)
                        print("Closed the modal.")

                    except TimeoutException:
                        print("Timed out waiting for the modal to appear.")
                    except NoSuchElementException as e:
                        print(f"Element not found: {str(e)}")
                    except StaleElementReferenceException:
                        print("Stale element reference. Skipping to the next row.")
                    except ElementNotInteractableException:
                        print("Element not interactable. Skipping to the next row.")
                    except Exception as e:
                        print(
                            f"Error processing row: {str(e)}. Skipping to the next row.")
                        return
                else:
                    print(
                        f"{domain_name} already exists")

        except NoSuchElementException:
            print("Market column not found for the current row.")

    with ThreadPoolExecutor(max_workers=1) as executor:
        futures = [executor.submit(process_row, row) for row in rows]
        for future in as_completed(futures):
            future.result()

    print(f"Extracted data for {len(domains)} domains.")
    return domains
