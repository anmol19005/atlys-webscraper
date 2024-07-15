import json
import os
from typing import List

import config
from models import Product


class Database:
    def __init__(self, db_path: str = config.Config.DATABASE_URL):
        self.db_path = db_path
        self.load_data()

    def load_data(self):
        if os.path.exists(self.db_path):
            with open(self.db_path, "r") as file:
                self.data = json.load(file)
        else:
            self.data = []

    def save_data(self):
        with open(self.db_path, "w") as file:
            json.dump(self.data, file, indent=4)

    def update_products(self, products: List[Product]):
        update_count = 0
        for product in products:
            existing_product = next((p for p in self.data if p['product_title'] == product.product_title), None)
            if existing_product:
                if existing_product['product_price'] != product.product_price:
                    existing_product['product_price'] = product.product_price
                    update_count += 1
            else:
                self.data.append(product.dict())
                update_count += 1

        self.save_data()
        return update_count
