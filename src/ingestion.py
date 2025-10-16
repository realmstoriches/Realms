"""
This module handles the ingestion of knowledge from various sources
into the ChromaDB knowledge base.
"""
from src.knowledge import KnowledgeBase
import os
import json
import re

def parse_product_data(input_file, output_dir):
    """
    Parses a raw, tab-separated product file into individual JSON files
    for each unique product.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    products = {}
    print(f"Starting product data ingestion from {input_file}...")

    with open(input_file, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line:
                continue

            parts = line.split('\t')

            if len(parts) < 3:
                continue

            vendor = parts[0].strip()
            sku = parts[1].strip()
            original_product_name = parts[2].strip()

            if not original_product_name:
                continue

            normalized_key = clean_filename(original_product_name)

            if normalized_key not in products:
                products[normalized_key] = {
                    "vendor": vendor,
                    "product_name": original_product_name,
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

def clean_filename(name):
    """Cleans a string to be used as a filename."""
    name = name.lower()
    name = re.sub(r'[\s/&™_]+', '-', name)
    name = re.sub(r'[^a-z0-9\-_]', '', name)
    name = re.sub(r'-+', '-', name)
    return name.strip('-')

def ingest_text_file(knowledge_base: KnowledgeBase, file_path: str):
    """
    Simulates scraping and ingesting knowledge from a text file.
    Each line in the file is treated as a separate document.

    Args:
        knowledge_base (KnowledgeBase): The knowledge base to ingest into.
        file_path (str): The path to the text file.
    """
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return

    with open(file_path, 'r') as f:
        for i, line in enumerate(f):
            line = line.strip()
            if line:
                doc_id = f"{os.path.basename(file_path)}-line-{i+1}"
                metadata = {"source": os.path.basename(file_path)}
                knowledge_base.add_document(line, metadata, doc_id)
    print(f"Successfully ingested {file_path}")