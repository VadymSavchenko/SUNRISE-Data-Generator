import json
import requests
from requests.auth import HTTPBasicAuth
import os
import random
from config import Config

PROJECT_KEY = Config.PROJECT_KEY
API_URL = Config.API_URL


def auth():
    auth_url = Config.AUTH_URL
    url = f"{auth_url}/oauth/token?grant_type=client_credentials"
    client_id = Config.CLIENT_ID
    client_secret = Config.CLIENT_SECRET

    response = requests.post(url, auth=HTTPBasicAuth(client_id, client_secret))
    print(response.text)
    return response.json()['access_token']


def upload_image(token, product_id, variant_id, image_path):
    url = f"{API_URL}/{PROJECT_KEY}/products/{product_id}/images?variant={variant_id}&filename={os.path.basename(image_path)}"

    headers = {
        'Authorization': f'Bearer {token}',
    }

    mime = None
    if image_path.lower().endswith(".jpg") or image_path.lower().endswith(".jpeg"):
        mime = "image/jpeg"
    elif image_path.lower().endswith(".png"):
        mime = "image/png"
    elif image_path.lower().endswith(".gif"):
        mime = "image/gif"
    else:
        print("Unsupported file type")
        return

    headers["Content-Type"] = mime

    with open(image_path, 'rb') as f:
        response = requests.post(url, headers=headers, data=f)
        print("\tImage upload response: ", response.text)
        # convert response.text to JSON
        response_json = json.loads(response.text)
        return response_json["version"]


def get_products(token):
    url = f"{API_URL}/{PROJECT_KEY}/products?limit=500"

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(url, headers=headers)
    return response.json()


def get_category_by_id(category_id, token):
    url = f"{API_URL}/{PROJECT_KEY}/categories/{category_id}"

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"\tFailed to get category. Status code: {response.status_code}")
        return None


def remove_product_image(product_id, version, variant_id, image_url, token):
    url = f"{API_URL}/{PROJECT_KEY}/products/{product_id}"

    payload = json.dumps({
      "version": version,
      "actions": [
        {
          "action": "removeImage",
          "variantId": variant_id,
          "imageUrl": image_url
        }
      ]
    })
    headers = {
      'Content-Type': 'application/json',
      'Authorization': f'Bearer {token}'
    }

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:
        print(f"\tSuccessfully removed image {image_url} from product {product_id}")
        return response.json()
    else:
        print(f"\tFailed to remove image. Status code: {response.status_code}, response: {response.text}")
        return None


def publish_product(token, product_id, version):
    url = f"{API_URL}/{PROJECT_KEY}/products/{product_id}"
    payload = json.dumps({
        "version": version,
        "actions": [
            {
                "action": "publish"
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:
        print(f"Successfully published product {product_id}")
        return response.json()
    else:
        print(f"Failed to publish product. Status code: {response.status_code}, response: {response.text}")
        return None


def upload_pics():
    token = auth()
    products = get_products(token)
    product_count = products["total"]
    print(f"Found {product_count} products")
    for index, product in enumerate(products["results"]):
        product_id = product["id"]
        product_name = product["masterData"]["current"]["name"]["en"]
        print(f"{index}/{product_count}: Uploading images for product {product_name}")
        variant_id = 1  # product["masterVariant"]["id"]
        version = product["version"]
        category_id = product["masterData"]["current"]["categories"][0]['id']
        category_name = get_category_by_id(category_id, token)["key"]

        # Get random image from shop_images/{category_name} folder, checking if the folder exists and has images
        if not os.path.exists(f'shop_images/{category_name}') or len(os.listdir(f'shop_images/{category_name}')) == 0:
            print(f"\tNo images for category {category_name}")
            continue
        image_path = f"shop_images/{category_name}/{random.choice(os.listdir(f'shop_images/{category_name}'))}"

        remove_product_image(product_id, version, variant_id, 'placeholder.jpg', token)
        if os.path.exists(image_path):
            version = upload_image(token, product_id, variant_id, image_path)
            publish_product(token, product_id, version)
        else:
            print(f"Image {image_path} does not exist")


if __name__ == '__main__':
    upload_pics()
