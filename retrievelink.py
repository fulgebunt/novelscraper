import json

import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin


def get_all_links(url, pattern):
    response = requests.get(url)
    if response.status_code != 200:
        return {}

    soup = BeautifulSoup(response.text, 'html.parser')
    links_dict = {}

    for tag in soup.find_all('a', href=True):
        link = urljoin(url, tag['href'])
        if pattern.match(link):
            # Since we are using numbers as keys, we can't update the dictionary directly.
            # We need to return the list of found links instead.
            links_dict[link] = link

    return links_dict

def get_novels(a,b):
# Main script
    novels = {}
    link_pattern = re.compile(r'https://wuxia.click/novel/.*')
    key_counter = 1

    for i in range(a, b):
        website_url = f"https://wuxia.click/search?page={i}&order_by=-total_views"
        page_links = get_all_links(website_url, link_pattern)

        # Update the novels dictionary with numbered keys
        for link in page_links.values():
            novels[key_counter] = link
            key_counter += 1
        print(i)
    print(novels)

    # Print the results


    with open('novellist.json', 'w') as json_file:
        json.dump(novels, json_file, indent=4)

if __name__ == "__main__":
    get_novels(21,30)