import os
import shutil
import json
import logging

# Set up basic configuration for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

domains_array_path = 'domains_array.json'
domains_jsonld_path = 'domains_jsonld.json'
domains_in_use = ["asi.bible","chatgpt.recipes","gptprime.ai","bom.chat","bookofmormon.chat","standardworks.chat","standard-works.chat","sermonwriter.ai","hemeonc.ai","chatgpt.makeup","ai-domains.forsale","cardiology.chat"]

# Priority order for TLDs
tld_priority = ['.ai', '.com', '.app', '.io', '.codes', '.chat', '.tech', '.news', '.dev', '.technology', '.expert', '.consulting', '.pro', '.tips', '.guide', '.blog', '.cloud']

def convert_to_array(src_path):
    try:
        with open(src_path, 'r') as file:
            data = json.load(file)

        domains_array = [{'name': name, **domain} for name, domain in data.items()]
        mark_domains_in_use(domains_array)  # Call function to mark domains in use
        logging.info("Conversion to array complete.")
        return domains_array
    except json.JSONDecodeError as e:
        logging.error(f"Error reading JSON: {str(e)}")
        return []
    except IOError as e:
        logging.error(f"Error opening file: {str(e)}")
        return []
    
def mark_domains_in_use(domains_array):
    # Set of domains in use for faster lookup
    domains_in_use_set = set(domains_in_use)
    for domain in domains_array:
        domain['inUse'] = domain['name'] in domains_in_use_set
    logging.info("Marking domains in use complete.")

def sort_domains(domains_array):
    # Define a custom sort key that handles TLDs not in the priority list
    def domain_sort_key(domain):
        parts = domain['name'].split('.')
        name = '.'.join(parts[:-1])  # Domain name without TLD
        tld = '.' + parts[-1]        # TLD with leading dot

        # Log the TLD and domain name being processed
        logging.debug(f"Processing domain '{name}' with TLD '{tld}'")

        # Determine sort index for TLD
        if tld in tld_priority:
            priority_index = tld_priority.index(tld)
        else:
            priority_index = float('inf')  # Assign a high number for undefined TLDs

        # Log the priority index
        logging.debug(f"TLD '{tld}' has sort index '{priority_index}'")

        return (priority_index, name)  # First sort by TLD, then by domain name

    # Sort the domains using the custom key
    domains_array.sort(key=domain_sort_key)
    with open(domains_array_path, 'w') as file:
        json.dump(domains_array, file, indent=2)
    logging.info("Sorting by TLD and name complete.")

def generate_jsonld(domain):
    jsonld = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": domain["name"],
        "description": domain["blurb"],
        "offers": {
            "@type": "Offer",
            "priceCurrency": "USD",
            "price": domain["price"],
            "url": f"https://{domain['name']}"
        }
    }
    return json.dumps(jsonld, indent=2)

def create_json_ld(domains_array):
    try:
        jsonld_data = [generate_jsonld(domain) for domain in domains_array]
        with open(domains_jsonld_path, 'w') as file:
            file.write('[\n' + ',\n'.join(jsonld_data) + '\n]')
        logging.info("JSON-LD data generated successfully.")
    except IOError as e:
        logging.error(f"Error creating JSON-LD: {str(e)}")
        return False

def update_html(COPY_DIR):
    try:
        dev_html_path = os.path.join(COPY_DIR, 'dev.html')
        index_html_path = os.path.join(COPY_DIR, 'index.html')

        with open(dev_html_path, 'r') as file:
            dev_html = file.read()

        with open(domains_jsonld_path, 'r') as file:
            jsonld_data = file.read()

        index_html = dev_html.replace('<!--JSONLD-->', f"<script type='application/ld+json'>\n{jsonld_data}\n</script>")
        index_html = index_html.replace('<!-- <script', '<script').replace('</script> -->', '</script>')

        with open(index_html_path, 'w') as file:
            file.write(index_html)

        logging.info("HTML file updated successfully.")
        return True
    except IOError as e:
        logging.error(f"Error updating HTML file: {str(e)}")
        return False

def copy_domains_json(src_path, COPY_DIR):
    try:
        os.makedirs(COPY_DIR, exist_ok=True)
        domains_array = convert_to_array(src_path)
        sort_domains(domains_array)

        shutil.copy(domains_array_path, os.path.join(COPY_DIR, src_path))
        logging.info(f"domains_array.json copied successfully to {os.path.join(COPY_DIR, src_path)}")

        create_json_ld(domains_array)
        shutil.copy(domains_jsonld_path, COPY_DIR)
        logging.info(f"domains_jsonld.json copied successfully to {COPY_DIR}")

        update_html(COPY_DIR)

        return True
    except IOError as e:
        logging.error(f"Error during file operations: {str(e)}")
        return False

# Example usage:
if __name__ == "__main__":
    copy_domains_json('domains.json', 'output_directory')