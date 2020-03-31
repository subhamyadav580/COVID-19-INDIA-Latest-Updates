import requests
from bs4 import BeautifulSoup
import pandas as pd

page = requests.get('https://www.mohfw.gov.in/')
html = BeautifulSoup(page.content, 'html.parser')

date = []
news = []
news_link = []
num = 0

for update in html.find_all('div', class_='update-box'):
    st = update.select('p strong')
    link = update.select('p a')
    links = update.find('p')
    date.append(st[num].text.strip())
    news.append(link[num].text.strip())
    news_link.append(links.find('a')['href'])

covid_update = pd.DataFrame({
    'Date' : date,
    'News' : news,
    'News Link' : news_link
})

#To save the dataframe in csv
file_to_save = 'COVID-19-INDIA-Latest-Updates.csv'
covid_update.to_csv(file_to_save)
