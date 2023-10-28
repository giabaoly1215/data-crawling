from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import time
import numpy as np


DRIVER = None

def initialize_driver():
    global DRIVER
    if DRIVER is None:
        print('Initiating driver...')
        service = Service(executable_path=r'/usr/local/bin/chromedriver')
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('-headless')
        chrome_options.add_argument('-no-sandbox')
        DRIVER = webdriver.Chrome(service=service, options=chrome_options)  # Create the new chrome browser with specific options
        print('Finished!')

def close_driver():
    global DRIVER
    if DRIVER is not None:
        print("Quitting drive...")
        DRIVER.quit()
        print("Done")

    DRIVER = None

close_driver()
initialize_driver()

def get_info(url):
    # print(   time.ctime(time.time()))
    DRIVER.get(url)
    soup = BeautifulSoup(DRIVER.page_source, 'html.parser')

    location_span = soup.find('span', class_='company-location').find_all('a')
    locations = [link.text for link in location_span]
    combined_locations = ', '.join(locations)    

    industry_tags = soup.find('span', class_='content-label', string='Ngành Nghề').find_next('span', class_='content').find_all('a')
    industries = [tag.get_text(strip=True) for tag in industry_tags]

    benefit_names = soup.find('div', class_='benefits').find_all('div', class_='benefit-name')
    benefit_text = ', '.join(name.get_text(strip=True) for name in benefit_names)

    job_description = soup.find('div', class_='job-description')
    if job_description:
        description_text = job_description.find('div', class_='description').get_text(strip=True).replace('\n', ', ')

    data.append({
        'title': soup.find('h1', class_ = 'job-title').contents[0].strip(),
        'company': soup.find('div', class_ = 'col-sm-12 company-name').find('a').span.text.strip(),
        'location': combined_locations,
        'date_update': soup.find('span', class_='content').get_text(strip=True),
        'category': ', '.join(industries), 
        'position': soup.find('span', class_='content-label', string='Cấp Bậc').find_next('span', class_='content').get_text(strip=True),
        'salary': soup.find('strong', class_='text-primary text-lg').get_text(strip=True),
        'welfare': benefit_text,
        'description': description_text,
        'requirement': soup.find('div', class_='job-requirements').find('div', class_='requirements').get_text(strip=True).replace('\n', ', ')})
    # print(time.ctime(time.time()))
    return data

data = []

urls = pd.read_csv('C:/Users/lygia/Desktop/vnworks_link.csv')

start = time.ctime(time.time())

for url in urls.iloc[:5229,0]:
    try:
        print(len(data))
        # print(url)
        get_info(url)
        df = pd.DataFrame(data)
        df.to_csv('C:/Users/lygia/Desktop/final_data/vnworks.csv', index=False)
    except Exception: continue

finish = time.ctime(time.time())

df = pd.DataFrame(data)
df.to_csv('C:/Users/lygia/Desktop/final_data/vnworks.csv', index=False)