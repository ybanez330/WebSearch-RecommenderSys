#-------------------------------------------------------------------------
# AUTHOR: Julia Ybanez
# FILENAME: parser.py
# SPECIFICATION: Retrieving information from html text using tags
# FOR: CS4250 - Assignment #4
# TIME SPENT: 2 hours
#-----------------------------------------------------------*/

from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client.web_crawler
pages_collection = db.pages
faculty_collection = db.faculty

def parse_faculty_information(html):
    soup = BeautifulSoup(html, 'html.parser')

    # Find all faculty members
    faculty_members = soup.find_all('div', class_='clearfix')

    parsed_data = []
    for member in faculty_members:
        name_tag = member.find('h2')
        name = name_tag.get_text().strip() if name_tag else None

        strong_tags = member.find_all('strong')
        title, office, email, website = None, None, None, None

        for tag in strong_tags:
            if 'Title' in tag.get_text():
                title = tag.find_next('br').next_sibling.strip() if tag.find_next('br') else None
            elif 'Office' in tag.get_text():
                office = tag.find_next('br').next_sibling.strip() if tag.find_next('br') else None
            elif 'Email' in tag.get_text():
                email = tag.find_next('a').get_text().strip() if tag.find_next('a') else None
            elif 'Web' in tag.get_text():
                website = tag.find_next('a')['href'].strip() if tag.find_next('a') else None

        faculty_info = {
            'name': name,
            'title': title,
            'office': office,
            'email': email,
            'website': website,
        }

        if any(faculty_info.values()):
            parsed_data.append(faculty_info)

    return parsed_data

def process_faculty_pages():
    pages = pages_collection.find()

    for page in pages:
        html = page['html']
        faculty_info = parse_faculty_information(html)

        faculty_collection.insert_many(faculty_info)

if __name__ == "__main__":
    process_faculty_pages()

    # Close MongoDB connection
    client.close()
