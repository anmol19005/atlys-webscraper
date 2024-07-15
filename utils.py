import requests
import os


def download_image(url: str, title: str) -> str:
    image_response = requests.get(url)
    image_path = f"images/{title.replace(' ', '_')}.jpg"
    os.makedirs(os.path.dirname(image_path), exist_ok=True)
    with open(image_path, "wb") as image_file:
        image_file.write(image_response.content)
    return image_path
