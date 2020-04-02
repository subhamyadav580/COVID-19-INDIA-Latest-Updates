import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

page = requests.get('https://www.mohfw.gov.in/')
html = BeautifulSoup(page.content, 'html.parser')


#Latest COVID update in INDIA
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

latest_covid_update = pd.DataFrame({
    'Date': date,
    'News': news,
    'News Link': news_link
})

#State wise update of COVID in INDIA
n = 0
sno = []
states = []
tcc = []
cd = []
death = []
for item in html.find_all('tr'):
    for t1 in (item.find_all('td')):
        if t1.text == 'Total number of confirmed cases in India':
            break
        if n == 0:
            sno.append(t1.text.strip())
            n += 1
        elif n == 1:
            states.append(t1.text.strip())
            n += 1
        elif n == 2:
            tcc.append(t1.text.strip())
            n += 1
        elif n == 3:
            cd.append(t1.text.strip())
            n += 1
        elif n == 4:
            death.append(t1.text.strip())
            n = 0


state_wise_covid_update = pd.DataFrame({
    'Name of State / UT': states,
    'Total Confirmed cases (Including 51 foreign Nationals)': tcc,
    'Cured/Discharged/Migrated': cd,
    'Death': death
})


plotting_states_data = state_wise_covid_update


#Getting total of each column
for column in state_wise_covid_update:
    if column == 'Total Confirmed cases (Including 51 foreign Nationals)':
        columnSeriesObj = state_wise_covid_update[column]
        cases = columnSeriesObj.values
        cases = sum(list(map(int, cases)))
    elif column == 'Cured/Discharged/Migrated':
        columnSeriesObj = state_wise_covid_update[column]
        total_cured = columnSeriesObj.values
        total_cured = sum(list(map(int, total_cured)))
    elif column == 'Death':
        columnSeriesObj = state_wise_covid_update[column]
        total_death = columnSeriesObj.values
        total_death = sum(list(map(int, total_death)))


#Adding total of each column in Dataframe
state_wise_covid_update = state_wise_covid_update.append({'Name of State / UT': 'Number of confirmed cases in India',
                                                          'Total Confirmed cases (Including 51 foreign Nationals)': cases, 'Cured/Discharged/Migrated': total_cured, 'Death': total_death}, ignore_index=True)


#To save the dataframe in csv
file_to_save = 'COVID-19-INDIA-Latest-Updates.csv'
latest_covid_update.to_csv(file_to_save, index=False)
#To save the state_wise_covid_update dataframe in csv
file_to_save = 'COVID-19-INDIA-State-Wise-Updates.csv'
state_wise_covid_update.to_csv(file_to_save, index=False)


for column in plotting_states_data:
    if column == 'Total Confirmed cases (Including 51 foreign Nationals)':
        columnSeriesObj = plotting_states_data[column]
        cases1 = columnSeriesObj.values
        cases1 = list(map(int, cases1))
    elif column == 'Name of State / UT':
        columnSeriesObj = plotting_states_data[column]
        state = columnSeriesObj.values
        state = list(map(str, state))


#Plotting the state data of no. of confirmed cases
sns.set(rc={'figure.figsize': (11, 9)})
plt.plot(state, cases1, 'go--')
plt.xticks(rotation='90', fontsize=15)
plt.ylabel('Total Confirmed cases (Including 51 foreign Nationals)', fontsize=15)
plt.xlabel('Name of State / UT', fontsize=15)
plt.title('Covid-Confirmed-Cases', fontsize=20)
plt.savefig('State-Wise-Data.png')
plt.show()
