import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import json


base_url = 'https://duunitori.fi'
category = 'ravintolatyontekija'
link = f'{base_url}/tyopaikat/ammatti/{category}'
filename = f"{category}_jobs.json"

def get_html(url):
    response = requests.get(url)
    return response.text

def get_cards(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find_all('div', class_='job-box')

def clean_location(location_text):
    if location_text is not None:
        cleaned_location = re.sub(r"\s*[–-]\s*$", '', location_text).strip()
        return cleaned_location
    else:
        return None

def parse_card(card, base_url):
    if card is None:
        return None
    job_name = card.find('h3', class_='job-box__title').get_text(strip=True)
    url_link = card.find('a', class_='job-box__hover').get('href')
    url_link = urljoin(base_url, url_link)
    company_tag = card.find('span', class_='job-box__company-name')
    if company_tag is not None:
        company_name = company_tag.get_text(strip=True)
    else:
        company_name = None
    location_tag = card.find('span', class_='job-box__job-location')
    if location_tag is not None:
        location_text = location_tag.get_text(strip=True)
        location = clean_location(location_text)
    else:
        location = None
    posted = card.find('span', class_='job-box__job-posted').get_text(strip=True).replace('Julkaistu',
                                                                                                  '').strip()
    job_data = {
        'title': job_name,
        'url': url_link,
        'company': company_name,
        'location': location,
        'posted': posted
        }

    return job_data

def parse_jobs(cards, base_url):
    jobs = []
    for card in cards:
        job_data = parse_card(card, base_url)
        if job_data is not None:
            jobs.append(job_data)
    return jobs

def save_jobs_to_json(jobs, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(jobs, file, ensure_ascii=False, indent=2)
    return filename

html = get_html(link)
cards = get_cards(html)
jobs = parse_jobs(cards, base_url)
save_jobs_to_json(jobs, filename)



