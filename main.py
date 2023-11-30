import os

import requests
from bs4 import BeautifulSoup
import time
import json
from retrievelink import get_novels

def scrape_website_text(url, delay=5, max_retries=5):
    retries = 0

    while retries < max_retries:
        response = requests.get(url)

        # Check for 429 error (Too Many Requests)
        if response.status_code == 429:
            try:
                # Parse retry time from response headers and wait
                retry_after = int(response.headers.get("Retry-After", delay))
                print(f"Rate limit hit. Retrying after {retry_after} seconds.")
                time.sleep(retry_after)
            except ValueError:
                # Default wait time if header is missing or not an integer
                time.sleep(delay)
            retries += 1
        elif response.status_code != 200:
            return f"Failed to retrieve the webpage. Status code: {response.status_code}"
        else:
            # Successful request, parse the content
            soup = BeautifulSoup(response.content, 'html.parser')
            text_dict = {f"{tag.name} {' '.join([f'{attr}={tag[attr]}' for attr in tag.attrs])}": tag.get_text(strip=True) for tag in soup.find_all(True)}
            return text_dict

    return "Max retries exceeded."


# Example usage

def reformat_url(base_novel_url):
    # Replace 'novel' with 'chapter' and append a hyphen at the end
    return base_novel_url.replace('/novel/', '/chapter/') + "-"

def download_basic():
    with open('novellist.json', 'r') as json_file:
        novel = json.load(json_file)
    # Example usage
    for i in range(1,len(novel)):
        base_novel_url = novel[str(i)]
        new_url = reformat_url(base_novel_url)
        url = base_novel_url

        # Split the URL by '/'
        parts = url.split('/')

        # Get the last part of the URL
        last_part = parts[-1]
        print("NOVEL: " + str(i))
        if os.path.isfile("static/" + last_part + '.json'):
            print("EXISTS")
            pass
        else:
            chapters = {}
            for j in range(100):
                print("CHAPTER: " + str(j))
                number = j+1
                url = new_url + str(number)  # Replace with the desired URL
                webpage_text = scrape_website_text(url)
                chapter = "Chapter " + str(number)
                if chapter in webpage_text["body "]:
                    chapters[chapter] = webpage_text["body "][webpage_text["body "].index(chapter):-1]
                else:
                    chapters[chapter] = webpage_text["body "]

        # Write to a JSON file
            url = base_novel_url

            # Split the URL by '/'
            parts = url.split('/')

            # Get the last part of the URL
            last_part = parts[-1]
            with open("static/"+last_part+'.json', 'w') as json_file:
                json.dump(chapters, json_file, indent=4)


def download_more(name):
    chapters = {}

    filename = name  # Replace this with your actual filename string

    # Extract the name part from the filename
    name = filename.rsplit('.', 1)[0]

    base_novel_url='https://wuxia.click/novel/' + name
    url = base_novel_url

    # Split the URL by '/'
    parts = url.split('/')

    # Get the last part of the URL
    last_part = parts[-1]
    new_url = reformat_url(base_novel_url)

    with open("static/" + last_part + '.json', 'r') as json_file:
        chapters = json.load(json_file)

    for j in range(len(chapters),len(chapters)+50):
        print("CHAPTER: " + str(j))
        number = j + 1
        url = new_url + str(number)  # Replace with the desired URL
        webpage_text = scrape_website_text(url)
        chapter = "Chapter " + str(number)
        if chapter in webpage_text["body "]:
            chapters[chapter] = webpage_text["body "][webpage_text["body "].index(chapter):-1]
        else:
            chapters[chapter] = webpage_text["body "]

    with open("static/" + last_part + '.json', 'w') as json_file:
        json.dump(chapters, json_file, indent=4)

if __name__ == "__main__":
    download_basic()