import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import json


base_url = 'https://duunitori.fi'
category = 'ravintolatyontekija'
link = f'{base_url}/tyopaikat/ammatti/{category}'



response = requests.get(link)

soup = BeautifulSoup(response.text, 'html.parser')

cards = soup.find_all('div', class_="job-box")


jobs = []

for num, card in enumerate(cards, start=1):
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
        location  = re.sub(r"\s*[–-]\s*$", '', location_text).strip()
    else:
        location = None
    posted = card.find('span', class_='job-box__job-posted').get_text(strip=True).replace('Julkaistu', '').strip()

    job_data = {
        'title': job_name,
        'url': url_link,
        'company': company_name,
        'location': location,
        'posted': posted
    }

    jobs.append(job_data)

filename = f"{category}_jobs.json"
with open(filename, 'w', encoding='utf-8') as file:
    json.dump(jobs, file, indent=2, ensure_ascii=False)
