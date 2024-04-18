from utils import web_driver, porkbun_extractor, ai_domains_forsale
from config import JSON_COPY_PATH

def main():
    src_path = 'domains.json'
    dest_path = '../ai-domains.forsale/domains.json'

    driver = web_driver.initialize_web_driver()

    try:
        domains = porkbun_extractor.get_domains(driver)
    except KeyboardInterrupt:
        print("\nScript interrupted by user.")
    finally:
        driver.quit()

    if domains:
        if JSON_COPY_PATH:
            success = ai_domains_forsale.copy_domains_json(src_path, JSON_COPY_PATH)
            if success:
                print(f"Domains.json copied successfully to {dest_path}")
            else:
                print(f"Failed to copy domains.json to {dest_path}")
        else:
            print("JSON_COPY_PATH not specified. Skipping file copy.")
    else:
        print(f"No domains found.")

if __name__ == '__main__':
    main()