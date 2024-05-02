from utils import web_driver, porkbun_extractor

def main():
    driver = web_driver.initialize_web_driver()

    try:
        domains = porkbun_extractor.get_domains(driver)
    except KeyboardInterrupt:
        print("\nScript interrupted by user.")
    finally:
        driver.quit()

    if domains:
        print(f"Extracted data for {len(domains)} domains.")
    else:
        print(f"No domains found.")

if __name__ == '__main__':
    main()