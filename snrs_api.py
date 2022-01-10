import requests
import json

def get_bearer(apiKey):
    url = "https://api.synerise.com/v4/auth/login/profile"
    payload = json.dumps({
      "apiKey": apiKey
    })
    headers = {
      'Api-Version': '4.4',
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    request_json = response.json()
    token = request_json["token"]
    return token

def add_item_to_catalog(bearer,bagid, payload):
    url = f"https://api.synerise.com/catalogs/bags/{bagid}/items"

    payload = json.dumps(payload)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {bearer}'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

def add_item_to_catalog_batch(bearer,bagid, payload):
    url = f"https://api.synerise.com/catalogs/bags/{bagid}/items/batch"

    payload = json.dumps(payload)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {bearer}'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)




