import os
import shutil
import json

domains_array_path = 'domains_array.json'
domains_jsonld_path = 'domains_jsonld.json'
tlds_path = 'tlds.txt'

def convert_to_array(src_path):
    # Read the domains.json file
    with open(src_path, 'r') as file:
        data = json.load(file)

    # Convert the object to an array of domain objects
    domains_array = [{'name': name, **domain} for name, domain in data.items()]

    # Sort the domains by name in ascending order
    domains_array.sort(key=lambda domain: domain['name'])

    # Write the updated data back to the domains.json file
    with open(domains_array_path, 'w') as file:
        json.dump(domains_array, file, indent=2)

    print("Conversion and sorting complete. The {domains_array_path} file has been updated.")
    return domains_array

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
        # Generate JSON-LD for each domain
        jsonld_data = []
        for domain in domains_array:
            jsonld_data.append(generate_jsonld(domain))

        # Write the JSON-LD data to a file
        with open(domains_jsonld_path, 'w') as file:
            file.write('[\n')
            file.write(',\n'.join(jsonld_data))
            file.write('\n]')

        print("JSON-LD data generated successfully.")

    except IOError as e:
        print(f"Error creating json-ld: {str(e)}")
        return False

def create_tlds(tlds_path, domains_array):
    # Generate a list of unique TLDs
    tlds = set()
    for domain in domains_array:
        tld = domain["name"].split(".")[-1]
        tlds.add(tld)

    # Write the TLDs to a file
    with open(tlds_path, 'w') as file:
        file.write('\n'.join(tlds))

    print("JSON-LD data and TLDs generated successfully.")

def copy_domains_json(src_path, COPY_DIR):
    try:
        # Create the destination directory if it doesn't exist
        os.makedirs(COPY_DIR, exist_ok=True)

        domains_array = convert_to_array(src_path)
        shutil.copy(domains_array_path, COPY_DIR + "/" + src_path)
        print(f"{COPY_DIR} copied successfully to {COPY_DIR}/{src_path}")

        create_json_ld(domains_array)
        shutil.copy(domains_jsonld_path, COPY_DIR)
        print(f"domains_jsonld.json copied successfully from {domains_jsonld_path} to {COPY_DIR}")

        create_tlds(tlds_path, domains_array)
        shutil.copy(tlds_path, COPY_DIR)
        print(f"tlds.txt copied successfully from {tlds_path} to {COPY_DIR}")
        return True
    except IOError as e:
        print(f"Error copying domains.json: {str(e)}")
        return False