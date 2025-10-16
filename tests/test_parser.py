import unittest
import os
import tempfile
import json
from scripts.parse_products import parse_product_data, clean_filename

class TestParser(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.input_file = os.path.join(self.temp_dir.name, "raw_data.txt")
        # Create a dedicated output directory inside the temp directory
        self.output_dir = os.path.join(self.temp_dir.name, "output")
        os.makedirs(self.output_dir)

        with open(self.input_file, "w") as f:
            f.write("vendor1\tsku1\tProduct A\tColor\tRed\n")
            f.write("vendor1\tsku2\tProduct A \tColor\tBlue\n")
            f.write("vendor2\tsku3\tProduct B\tSize\tLarge\n")
            f.write("vendor3\tsku4\tProduct C / Special\tOption\tValue\n")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_parse_product_data(self):
        # Pass the dedicated output directory to the function
        parse_product_data(self.input_file, self.output_dir)

        # List only the files in the output directory
        generated_files = sorted(os.listdir(self.output_dir))

        self.assertEqual(len(generated_files), 3)

        product_a_filename = "product-a.json"
        self.assertIn(product_a_filename, generated_files)
        with open(os.path.join(self.output_dir, product_a_filename), 'r') as f:
            data = json.load(f)
        self.assertEqual(data['product_name'].strip(), 'Product A')
        self.assertEqual(len(data['variants']), 2)

        product_c_filename = "product-c-special.json"
        self.assertIn(product_c_filename, generated_files)

if __name__ == '__main__':
    unittest.main()