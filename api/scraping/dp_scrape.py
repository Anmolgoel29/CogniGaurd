import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from fake_useragent import UserAgent

import json
import re


# def get_scrape_data(url):
#     # Use a fake user agent to mimic a web browser
#     user_agent = UserAgent()
#     headers = {'User-Agent': user_agent.random}

#     # Making the request using the headers
#     response = requests.get(url, headers=headers)

    
#     if response.status_code == 200:
#         html_text = response.text

#         # Extracting the text
#         soup = BeautifulSoup(html_text, 'html.parser')

#         tags_list = ['div', 'span', 'p', 'a', 'ul', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
#         # text = ' '.join([tag.get_text() for tag in soup.find_all(tags_list)])
#         text_list = []

#         # Use tqdm to display a progress bar
#         for tag in tqdm(soup.find_all(tags_list), desc='Extracting Text', unit='tags'):
#             text_list.append(tag.get_text())

#         text = ' '.join(text_list)

#         return text

#     else:
#         # Handle the case where the request was not successful
#         print(f"Error: Unable to fetch content from {url}. Status code: {response.status_code}")
#         return None
    

def get_scrape_data(url):

    # Use a fake user agent to mimic a web browser
    user_agent = UserAgent()
    headers = {'User-Agent': user_agent.random}

    # Making the request using the headers
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        html_text = response.text

        # Extracting the text
        soup = BeautifulSoup(html_text, 'html.parser')

        tags_list = ['div', 'span', 'p', 'a', 'ul', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
        text_list = []

        # Use tqdm to display a progress bar
        for tag in tqdm(soup.find_all(tags_list), desc='Extracting Text', unit='tags'):
            text_list.append(tag.get_text())

        # Joining all text and stripping leading/trailing whitespaces
        full_text = ' '.join(text_list).strip()

        # Cleanup the text
        cleaned_text = cleanup_text(full_text)

        # Saving the cleaned text to a JSON file
        save_to_json(cleaned_text, "cleaned_text.json")

        # Splitting the cleaned text into sentences
        sentences = cleaned_text.split('. ')
        
        # Saving each sentence to a JSON file
        save_to_json(sentences, "sentences.json")

        return cleaned_text

    else:
        # Handle the case where the request was not successful
        print(f"Error: Unable to fetch content from {url}. Status code: {response.status_code}")
        return None

def cleanup_text(text):
    # Remove unwanted spaces, characters, and multiple newlines
    cleaned_text = re.sub(r'\s+', ' ', text)
    cleaned_text = re.sub(r'\s*\n\s*', '\n', cleaned_text)
    cleaned_text = re.sub(r'\s*-\s*', '-', cleaned_text)
    cleaned_text = re.sub(r'\s*,\s*', ',', cleaned_text)
    cleaned_text = re.sub(r'\s*\.\s*', '.', cleaned_text)
    cleaned_text = re.sub(r'\s*\(\s*', '(', cleaned_text)
    cleaned_text = re.sub(r'\s*\)\s*', ')', cleaned_text)
    cleaned_text = re.sub(r'\s*\[\s*', '[', cleaned_text)
    cleaned_text = re.sub(r'\s*\]\s*', ']', cleaned_text)
    cleaned_text = re.sub(r'\s*:\s*', ': ', cleaned_text)
    
    return cleaned_text
def save_to_json(data, filename):

    # Save data to a JSON file
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump({"text": data}, json_file, ensure_ascii=False, indent=2)

# Sample

my_url = "https://www.amazon.in/BassHeads-122-Earphones-Tangle-Straight/dp/B07QZ3CZ48/ref=sr_1_1?crid=I50H5USKYCLC&keywords=wired%2Bearphones%2Bboat&qid=1705597770&sprefix=wired%2Bearphones%2B%2Caps%2C2763&sr=8-1&th=1"


# my_url = "https://www.onionreads.com/disclaimer"
# scraped_text = get_scrape_data(my_url)

# if scraped_text:
#     print(f"Scraped Text : {scraped_text}")
# else:
#     print("Failed to Scrape")
