import json
import requests
from requests.auth import HTTPBasicAuth

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


def get_products(token):
    url = f"{API_URL}/{PROJECT_KEY}/products?limit=500"

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(url, headers=headers)
    return response.json()


def change_product_prices(token, product_id, version):
    url = f"{API_URL}/{PROJECT_KEY}/products/{product_id}"

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    prices = get_product_prices(token, product_id, version)
    has_eur_price = any(price['value']['currencyCode'] == 'EUR' for price in prices)
    if has_eur_price:
        for price in prices:
            if price['value']['currencyCode'] != 'EUR':
                payload = json.dumps({
                    "version": version,
                    "actions": [
                        {
                            "action": "removePrice",
                            "priceId": price['id']
                        }
                    ]
                })
                response = requests.post(url, headers=headers, data=payload)
                if response.status_code != 200:
                    print(f"Failed to remove price. Status code: {response.status_code}, response: {response.text}")
    else:
        for price in prices:
            if price['value']['currencyCode'] == 'USD':
                payload = json.dumps({
                    "version": version,
                    "actions": [
                        {
                            "action": "changePrice",
                            "priceId": price['id'],
                            "price": {
                                "value": {
                                    "currencyCode": "EUR",
                                    "centAmount": price['value']['centAmount']
                                }
                            },
                            "staged": True
                        }
                    ]
                })
                response = requests.post(url, headers=headers, data=payload)
                if response.status_code != 200:
                    print(f"Failed to change price. Status code: {response.status_code}, response: {response.text}")
                break


def get_product_prices(token, product_id, version):
    url = f"{API_URL}/{PROJECT_KEY}/products/{product_id}"

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['masterData']['current']['masterVariant']['prices']
    else:
        print(f"Failed to get product prices. Status code: {response.status_code}")
        return []


if __name__ == '__main__':
    token = auth()
    products = get_products(token)
    for index, product in enumerate(products["results"]):
        product_id = product["id"]
        product_name = product["masterData"]["current"]["name"]["en"]
        print(f"{index}: Changing prices for product {product_name}")
        version = product["version"]
        change_product_prices(token, product_id, version)
