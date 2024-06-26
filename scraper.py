import requests
from bs4 import BeautifulSoup

def scrape_website(url, selector):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Failed to load page {url} with status code {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')

    elements = soup.select(selector)

    if not elements:
        raise Exception(f"No elements found with the provided selector on {url}")

    data = []
    for element in elements:
        if element.name == 'img':
            data.append(element['src'])
        else:
            data.append(element.get_text(strip=True))

    return data