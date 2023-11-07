import requests
import os
import pandas as pd
from bs4 import BeautifulSoup

current_path = os.getcwd()
file_path = os.path.join(current_path, 'exports/')
if not os.path.exists(file_path):
    os.makedirs(file_path)

first_year = 2011
final_year = 2022

combined_df = pd.DataFrame()

for year in range(first_year, final_year+1):
    url = f'https://distrowatch.com/index.php?dataspan={year}'
    response = requests.get(url, timeout=60)
    html_content = response.content

    soup = BeautifulSoup(html_content, 'html.parser')

    table = soup.find('table', class_='News', style='direction: ltr')

    tr_elements = table.find_all('tr')

    elements_list = []

    for tr_element in tr_elements:
        th_element = tr_element.find('th', class_='phr1')
        td_a_element = tr_element.find('td', class_='phr2')
        td_value_element = tr_element.find('td', class_='phr3')

        if th_element and td_a_element and td_value_element:
            th_text = th_element.text
            td_a_text = td_a_element.text
            td_value = td_value_element.text

            row_list = [th_text, td_a_text, td_value]
            elements_list.append(row_list)

    elements_df = pd.DataFrame(elements_list)

    elements_df['year'] = year

    combined_df = pd.concat([combined_df, elements_df], ignore_index=True)

combined_df = combined_df.rename(columns={0: 'rank', 1: 'distro', 2: 'hpd'})

combined_df.to_csv(file_path+f'rank_by_years.csv', index=False)

print(file_path+'rank_by_years.csv saved successfully')