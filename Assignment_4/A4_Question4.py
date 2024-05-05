#-------------------------------------------------------------------------
# AUTHOR: Julia Ybanez
# FILENAME: crawler.py
# SPECIFICATION: Retrieving information from html text using tags
# FOR: CS4250 - Assignment #4
# TIME SPENT: 3 hours
#-----------------------------------------------------------*/

import requests
from bs4 import BeautifulSoup
from queue import Queue
from pymongo import MongoClient
from urllib.parse import urljoin

client = MongoClient('mongodb://localhost:27017/')
db = client.web_crawler
pages_collection = db.pages

def is_permanent_faculty_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    h1_tag = soup.find('h1', class_='cpp-h1')
    return h1_tag and h1_tag.get_text().strip() == 'Permanent Faculty'

def fetch_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error retrieving HTML from {url}: {e}")
    return None

def save_page(url, html):
    pages_collection.insert_one({'url': url, 'html': html})

def extract_links(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('a', href=True)
    return [urljoin(base_url, link['href']) for link in links]

def crawler_thread(frontier, base_url):
    visited_urls = set()

    while not frontier.empty():
        url = frontier.get()

        if url not in visited_urls:
            visited_urls.add(url)

            html = fetch_html(url)
            if html:
                if is_permanent_faculty_page(html):
                    save_page(url, html)
                    return

                for link in extract_links(html, base_url):
                    if link not in visited_urls:
                        frontier.put(link)

if __name__ == "__main__":
    frontier = Queue()
    base_url = 'https://www.cpp.edu/sci/computer-science/index.shtml'
    frontier.put(base_url)

    crawler_thread(frontier, base_url)

    # Close MongoDB connection
    client.close()