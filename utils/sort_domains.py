import json

# Read the domains.json file
with open('domains.json', 'r') as file:
    data = json.load(file)

# Convert the object to an array of domain objects
domains = [{'name': name, **domain} for name, domain in data.items()]

# Sort the domains by name in ascending order
domains.sort(key=lambda domain: domain['name'])

# Write the updated data back to the domains.json file
with open('domains.json', 'w') as file:
    json.dump(domains, file, indent=2)

print("Conversion and sorting complete. The 'domains.json' file has been updated.")