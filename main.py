from utils import web_driver, porkbun_extractor, ai_domains_forsale
from config import COPY_DIR

def main():
    src_path = 'domains.json'

    driver = web_driver.initialize_web_driver()

    try:
        domains = porkbun_extractor.get_domains(driver)
    except KeyboardInterrupt:
        print("\nScript interrupted by user.")
    finally:
        driver.quit()

    if domains:
        if COPY_DIR:
            success = ai_domains_forsale.copy_domains_json(src_path, COPY_DIR)
            if success:
                print(f"Domains.json copied successfully to {COPY_DIR}")
            else:
                print(f"Failed to copy domains.json to {COPY_DIR}")
        else:
            print("COPY_DIR not specified. Skipping file copy.")
    else:
        print(f"No domains found.")

if __name__ == '__main__':
    main()