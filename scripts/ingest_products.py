import os
import json
import re
import sys

def clean_filename(name):
    """Cleans a string to be used as a filename."""
    name = name.lower()
    name = re.sub(r'[\s/&™_]+', '-', name)
    name = re.sub(r'[^a-z0-9\-_]', '', name)
    name = re.sub(r'-+', '-', name)
    return name.strip('-')

def ingest_products_from_raw_data(input_file, output_dir):
    """
    Parses a raw, tab-separated product file into individual JSON files
    for each unique product, correctly grouping all variants.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    products = {}
    print(f"Starting product ingestion from {input_file}...")

    with open(input_file, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line:
                continue

            parts = line.split('\t')

            if len(parts) < 3:
                print(f"Skipping malformed line {i+1}: Not enough parts.")
                continue

            vendor = parts[0].strip()
            sku = parts[1].strip()
            product_name = parts[2].strip()

            if not product_name:
                print(f"Skipping malformed line {i+1}: Empty product name.")
                continue

            # Use a cleaned, normalized name as the dictionary key
            normalized_key = clean_filename(product_name)

            if normalized_key not in products:
                products[normalized_key] = {
                    "vendor": vendor,
                    "product_name": product_name,
                    "variants": []
                }

            variant = {
                "sku": sku,
                "options": {}
            }

            option_parts = [p.strip() for p in parts[3:] if p.strip()]
            if len(option_parts) >= 2:
                for j in range(0, len(option_parts), 2):
                    if j + 1 < len(option_parts):
                        option_name = option_parts[j]
                        option_value = option_parts[j+1]
                        variant["options"][option_name] = option_value

            products[normalized_key]["variants"].append(variant)

    for normalized_key, data in products.items():
        filename = f"{normalized_key}.json"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    print(f"Successfully ingested and generated {len(products)} product files.")

if __name__ == "__main__":
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    sys.path.insert(0, project_root)

    ingest_products_from_raw_data("data/raw_products.txt", "products/")