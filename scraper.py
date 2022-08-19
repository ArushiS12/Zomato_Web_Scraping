import pandas as pd
import numpy as np
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.parse import urljoin

driver = webdriver.Chrome(executable_path=r'C:\Users\ArushiSrivastava\Downloads\chromedriver_win32\chromedriver')
driver.get('https://www.zomato.com/chennai/dine-out')  # url of the website

time.sleep(2) #takes 2 seconds for web page to open
SCROLL_PAUSE_TIME = 3
last_height = driver.execute_script("return document.body.scrollHeight") # Get scroll height

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # Scroll down to bottom
    time.sleep(SCROLL_PAUSE_TIME) # Wait to load page
    new_height = driver.execute_script("return document.body.scrollHeight") # Calculate new scroll height and compare with last scroll height
    if new_height == last_height:
        break
    last_height = new_height
    
# create soup
soup = BeautifulSoup(driver.page_source, 'html.parser')
divs = soup.findAll('div', class_='jumbo-tracker')

url = []
rest_name = []
rating = []
price = []
cuisine = []
area = []

for div in divs: 

    name_tag = div.find('h4')
    rest_name.append(name_tag.text)

    link_tag = div.find('a')
    link = link_tag.get('href')
    base_url = 'https://www.zomato.com'
    result = urljoin(base_url, link)
    url.append(result)
    
    area_tag = div.find_all('p')
    area.append(area_tag[3].text)
    
    #using next_sibling
    cuisine_tag = div.div.a.next_sibling.p.text
    price_tag = div.div.a.next_sibling.p.next_sibling.text
    rating_tag = div.div.a.next_sibling.div.div.div.div.div.div.div.text
    
    rating.append(rating_tag)
    price.append(price_tag)
    cuisine.append(cuisine_tag)
    
df = pd.DataFrame({'Name': rest_name, 'Area': area, 'Rating': rating, 'Price': price, 'Cuisine': cuisine, 'URL': url})

#For specific cuisines
l=['South Indian']
x=df['Cuisine'].str.contains('|'.join(l))
df['Flag'] = np.where(x, 'Yes', 'No')
southindian_df = df.loc[df['Flag'] == 'Yes']
southindian_df.drop('Flag', axis=1)
