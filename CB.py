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

data = []

def get_info(url):
    DRIVER.get(url)
    soup = BeautifulSoup(DRIVER.page_source, 'html.parser')

    company = soup.find('a', class_ = 'employer job-company-name')
    company = np.nan if company is None else company.text
    
    welfare_list = soup.select('.welfare-list li')
    welfare_texts = [li.get_text(strip=True) for li in welfare_list]
    welfare_combined = ', '.join(welfare_texts)
    
    job_require = soup.find_all('div', class_='detail-row')[2]
    job_require_text = ' '.join(job_require.stripped_strings) if job_require else ""
    
    data.append({
        'title': soup.find('h1', class_ = 'title').text,
        'company': company,
        'location': soup.select_one('.map p a').text,
        'date_update': soup.select_one('.detail-box ul li:nth-of-type(1) p').text,
        'category': soup.select_one('.detail-box ul li:nth-of-type(2) p').get_text(strip = True), 
        'position': soup.select_one('.detail-box ul li:nth-of-type(3) p').text,
        'salary': soup.select('.detail-box.has-background')[2].select_one('li:nth-of-type(1) p').text.strip(),
        'welfare': welfare_combined,
        'description': ' '.join(soup.find('div', class_='detail-row reset-bullet').stripped_strings),
        'requirement': job_require_text})
    return data

urls = pd.read_csv('C:/Users/lygia/Desktop/careerbuilder_link.csv') # duyệt qua list các link cần vào 

start = time.ctime(time.time())

for i, url in enumerate(urls.iloc[:,0]):
    try:
        print(i, len(data))
        # print(url)
        get_info(url) # lấy thông tin của link đang duyệt
        df = pd.DataFrame(data) # lưu vào df
        df.to_csv('C:/Users/lygia/Desktop/final_data/careerbuilder_4.csv', index=False) # xuất
    except Exception: continue

finish = time.ctime(time.time())

df = pd.DataFrame(data)
df.to_csv('C:/Users/lygia/Desktop/final_data/careerbuilder_4.csv', index=False)

print('Done')
print(start)
print(finish)





































