from typing import List
import httpx
from bs4 import BeautifulSoup
import requests

import config
from database import Database
from notifier import ConsoleNotifier
from models import Product
from schemas import ScrapeSettings
from utils import download_image
from cache import Cache


class Scraper:
    def __init__(self, settings: ScrapeSettings):
        self.settings = settings

    def fetch_page(self, page: int):
        base_url = config.Config.WEBSITE_URL
        url = base_url if page == 1 else f"{base_url}page/{page}"
        try:
            response = requests.get(url, proxies={"http": self.settings.proxy,
                                                  "https": self.settings.proxy} if self.settings.proxy else None)
            response.raise_for_status()
            return response.text
        except httpx.HTTPStatusError:
            return self.fetch_page(page)

    def scrape_products(self, page_limit) -> List:
        scraped_products = []

        for page in range(1, page_limit + 1):
            html = self.fetch_page(page)
            soup = BeautifulSoup(html, "html.parser")
            products = soup.select("ul.products .product")

            for product in products:
                title_element = product.select_one("div.mf-product-thumbnail img")
                if title_element:
                    title = title_element.get("title", "").strip()
                else:
                    title = "No title found"

                discounted_price_element = product.select_one("span.price ins .woocommerce-Price-amount")
                original_price_element = product.select_one("span.price .woocommerce-Price-amount bdi")

                if discounted_price_element:
                    price = float(discounted_price_element.text.strip().replace("₹", "").replace(",", ""))
                else:
                    if original_price_element:
                        price = float(original_price_element.text.strip().replace("₹", "").replace(",", ""))
                    else:
                        price = 0.0

                image_url = product.select_one(".mf-product-thumbnail img")["data-lazy-src"]
                image_path = download_image(image_url, title)

                scraped_products.append(Product(product_title=title, product_price=price, path_to_image=image_path))

        return scraped_products

    def scrape(self):

        products = self.scrape_products(self.settings.pages)
        db = Database()
        cache = Cache()
        updated_count = 0
        total_scraped = len(products)

        for product in products:
            cached_price = cache.get_product(product.product_title)
            if not cached_price or float(cached_price) != product.product_price:
                db.update_products([product])
                cache.set_product(product.product_title, product.product_price)
                updated_count += 1

        notifier = ConsoleNotifier()
        notifier.notify(f"Scraped {total_scraped} products and updated {updated_count} products.")

        return {"scraped": total_scraped,
                "updated": updated_count}
