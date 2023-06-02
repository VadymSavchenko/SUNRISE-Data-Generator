import csv
import json
import random
import re
import string
from faker import Faker
from uuid import uuid4

from values import *
from config import Config

fake = Faker()


class ProductGenerator:
    def __init__(self):
        self.generated_skus = set()
        self.generated_base_ids = set()

    @staticmethod
    def generate_random_sku():
        return SKU_FORMAT.format(
            letter1=random.choice(string.ascii_uppercase),
            num1=str(random.randint(100000000000, 999999999999)),
            letter2=random.choice(string.ascii_uppercase),
            num2=str(random.randint(0, 999))
        )

    def generate_unique_base_id(self):
        while True:
            base_id = str(uuid4())
            if base_id not in self.generated_base_ids:
                self.generated_base_ids.add(base_id)
                return base_id

    @staticmethod
    def generate_prices():
        num_prices = random.randint(1, 5)
        shuffled_currencies = CURRENCIES[:]
        random.shuffle(shuffled_currencies)
        num_prices = min(num_prices, len(CURRENCIES))
        prices = [
            f"{shuffled_currencies[i]} {random.choice(AMOUNTS)} {random.choice(MARKETS)} {random.choice(STORES)}".strip()
            for i in range(num_prices)
        ]
        return ";".join(prices)

    def generate_products_file(self):
        with open(f'{Config.SUNRISE_PATH}/data/products.csv', 'w', newline='') as csvfile:
            fieldnames = list(possible_values.keys())
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_NONNUMERIC)
            writer.writeheader()

            for _ in range(NUM_ROWS):
                row = {}
                category = random.choice(list(possible_values["categories"]))
                row["categories"] = category

                for field in fieldnames:
                    if field == "creationDate":
                        row[field] = fake.date_between(start_date='-1y', end_date='today')
                    elif field == "sku":
                        sku = self.generate_random_sku()
                        self.generated_skus.add(sku)
                        row[field] = sku
                    elif field == "prices":
                        row[field] = self.generate_prices()
                    elif field == "name.en":
                        category = row["categories"]
                        row[field] = random.choice(possible_values["name.en"][category])
                    elif field == "description.en":
                        row[field] = f'{random.choice(possible_values["description.en"][row["categories"]])}'
                    elif field == "baseId":
                        unique_base_id = self.generate_unique_base_id()
                        row[field] = unique_base_id
                    elif field == "slug.en":
                        name = re.sub(r'\W+', ' ', row['name.en']).lower().replace(' ', '-')
                        sku = re.sub(r'\W+', '', row['sku']).lower()
                        row['slug.en'] = f'{name}-{sku}'
                    elif field == "variantKey":
                        row[field] = row["sku"]
                    elif field == "images":
                        row[field] = PLACEHOLDER_IMAGE
                    else:
                        if possible_values[field]:  # if list is not empty
                            row[field] = random.choice(possible_values[field])
                        else:  # if list is empty, generate placeholder
                            row[field] = f""
                writer.writerow(row)

    def generate_inventory_file(self):
        with open(f'{Config.SUNRISE_PATH}/data/inventory.csv', 'w', newline='') as csvfile:
            fieldnames = ["sku", "quantityOnStock", "supplyChannel"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_NONNUMERIC)
            writer.writeheader()
            for sku in self.generated_skus:
                row = {"sku": sku, "quantityOnStock": random.randint(0, 1000), "supplyChannel": ""}
                writer.writerow(row)
                # print("Generated inventory row: ", row)

    def generate_inventory_store_file(self):
        with open(f'{Config.SUNRISE_PATH}/data/inventory-stores.csv', 'w', newline='') as csvfile:
            fieldnames = ["sku", "quantityOnStock", "supplyChannel"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_NONNUMERIC)
            writer.writeheader()

            # Read the JSON data
            with open(f'{Config.SUNRISE_PATH}/data/channels.json', 'r') as jsonfile:
                data = json.load(jsonfile)
            for sku in self.generated_skus:
                for channel in data:
                    # Select a supplyChannel key
                    key = channel['key']
                    row = {"sku": sku, "quantityOnStock": random.randint(0, 1000), "supplyChannel": key}
                    writer.writerow(row)
                    print("Generated inventory row: ", row)

    def generate_taxes_file(self):
        # Generate the list of tax data
        data_list = []
        for key, data in tax_keys.items():
            rates_list = []
            # Add U.S. state tax data
            for state, tax in state_sales_tax.items():
                rates_list.append({
                    "name": f"{round(tax * data['percentage'] * 100, 2)}% incl.",
                    "amount": round(tax * data['percentage'], 2),
                    "includedInPrice": True,
                    "country": "US",
                    "state": state
                })
            # Add other countries tax data
            for country, tax in country_sales_tax.items():
                rates_list.append({
                    "name": f"{round(tax * data['percentage'] * 100, 2)}% incl.",
                    "amount": round(tax * data['percentage'], 2),
                    "includedInPrice": True,
                    "country": country
                })
            data_list.append({
                "name": data['name'],
                "key": key,
                "rates": rates_list
            })

        # Save the list of tax data to a JSON file
        with open(f'{Config.SUNRISE_PATH}/data/tax-category.json', 'w') as f:
            json.dump(data_list, f, indent=2)


def generate_all():
    generator = ProductGenerator()
    generator.generate_products_file()
    generator.generate_inventory_file()
    generator.generate_taxes_file()
    generator.generate_inventory_store_file()


if __name__ == '__main__':
    generate_all()
