import requests
from bs4 import BeautifulSoup
import time
import json

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
chapters = {}
for i in range(500):
    number = i+1
    url = "https://wuxia.click/chapter/library-of-heavens-path-" + str(number)  # Replace with the desired URL
    webpage_text = scrape_website_text(url)
    chapter = "Chapter " + str(number)
    if chapter in webpage_text["body "]:
        chapters[chapter] = webpage_text["body "][webpage_text["body "].index(chapter):-1]
    else:
        chapters[chapter] = webpage_text["body "]
    if (i+1) % 10 == 0:
        print(i)
        webpage = "webpage"+str(i)+".json"
        print(webpage)
        with open(webpage, 'w') as json_file:
            json.dump(chapters, json_file, indent=4)
        chapters = {}


# Write to a JSON file
with open('webpage.json', 'w') as json_file:
    json.dump(chapters, json_file, indent=4)

url = "https://novelfulll.com/book/2568/1152941.html?c=Swindler-"  # Replace with the desired URL
