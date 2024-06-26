import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from .navigation import navigate_to_domains, scroll_and_collect_rows
from .domain_processor import process_row


def get_domains(driver):
    navigate_to_domains(driver)

    rows = scroll_and_collect_rows(driver)
    print(f"Found {len(rows)} domain rows.")

    try:
        with open("domains.json", "r") as file:
            domains = json.load(file)
    except FileNotFoundError:
        domains = {}

    with ThreadPoolExecutor(max_workers=1) as executor:
        futures = [executor.submit(
            process_row, driver, row, domains) for row in rows]
        for future in as_completed(futures):
            future.result()

    print(f"Extracted data for {len(domains)} domains.")
    return domains
