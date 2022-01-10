from xml.etree import cElementTree as ElementTree
import xml_parser as xml
from snrs_api import get_bearer, add_item_to_catalog, add_item_to_catalog_batch
import time
import requests
start = time.time()
#  Zmienne SNRS
api_key = "cd7d1bb4-42e4-447b-a74d-5d9e48f95506"
bag_id = "12122"
feed_url = 'https://files.channable.com/W3FhUYGZ3s2UUCSh2vWsIw==.xml'

# Pobranie feedu
feed = requests.get(feed_url)
# Parsowanie feedu do dict + tworzenie tablicy z unikalnymi item_group_id
root = ElementTree.fromstring(feed.text)

unique_item_group_ids = []
feed_dict = []

for item in root.findall("./channel/item"):
    xmldict = xml.XmlDictConfig(item)
    feed_dict.append(xmldict)
    if xmldict['{http://base.google.com/ns/1.0}item_group_id'] not in unique_item_group_ids:
        unique_item_group_ids.append(xmldict['{http://base.google.com/ns/1.0}item_group_id'])

# Tworzenie nowego feedu
new_feed = []

for item_group_id in unique_item_group_ids:
    grouped_ids = []
    grouped_colors = []
    grouped_imgs = []
    for item in list(feed_dict):
        if item_group_id == item.get('{http://base.google.com/ns/1.0}item_group_id'):
            grouped_ids.append(item.get('{http://base.google.com/ns/1.0}id'))
            grouped_colors.append(item.get('color'))
            grouped_imgs.append(item.get('{http://base.google.com/ns/1.0}image_link'))
            feed_dict.remove(item)

    new_item = {"itemKey": item_group_id,
                "value":
                    {"itemId": item_group_id,
                     "ids": grouped_ids,
                     "images": grouped_imgs,
                     "colors": grouped_colors}}
    new_feed.append(new_item)

# Request api auth + batch do katalogu
bearer = get_bearer(api_key)
add_item_to_catalog_batch(bearer, bag_id, new_feed)

end = time.time()
print(f'Executed in: {end - start}')
