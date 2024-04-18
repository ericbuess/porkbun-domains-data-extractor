import os
import shutil
import json

domains_array_path = 'domains_array.json'

def convert_to_array(src_path):
    # Read the domains.json file
    with open(src_path, 'r') as file:
        data = json.load(file)

    # Convert the object to an array of domain objects
    domains = [{'name': name, **domain} for name, domain in data.items()]

    # Sort the domains by name in ascending order
    domains.sort(key=lambda domain: domain['name'])

    # Write the updated data back to the domains.json file
    with open(domains_array_path, 'w') as file:
        json.dump(domains, file, indent=2)

    print("Conversion and sorting complete. The {domains_array_path} file has been updated.")

def copy_domains_json(src_path, dest_path):
    try:
        # Create the destination directory if it doesn't exist
        dest_dir = os.path.dirname(dest_path)
        os.makedirs(dest_dir, exist_ok=True)

        convert_to_array(src_path)

        shutil.copy(domains_array_path, dest_path)
        print(f"domains.json copied successfully from {domains_array_path} to {dest_path}")
        return True
    except IOError as e:
        print(f"Error copying domains.json: {str(e)}")
        return False