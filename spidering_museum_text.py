import requests #for http requests
import pandas as pd #gives us DataFrames
import numpy as np
import time
from selenium import webdriver

task_token = input('please input your task token: ')
task_range = task_token.split('_')
lb = int(task_range[0])
ub = int(task_range[1])
print('Your digits are: ')
print(lb, ub)
print('If this is not correct, please contact me and stop running this task. ')
confirm = input('Starting task (enter \'y\' to confirm starting): ')
if not confirm == 'y': 
    print('You cancelled this task. ')
    quit()
print('Starting...')
print('\nChrome will be automatically running on your computer. \n')
print('Please DO NOT operate the automatically-running Chrome windows. This task usually takes 10 minutes, depending on your internet connection.')
print('You may enjoy some pictures from the Art Institute of Chicago.\n')

exception = 0
# Write a function that spider content from a link and returns a DataFrame. 
def get_description(index, artwork_title, url): 
    global exception
    pars_dict = {'index':[], 'artwork_title' : [], 'metadata': [], 'description_text' : [], 'url' : []}
    driver = webdriver.Chrome('./chromedriver')
    try: 
        driver.get(url)
        descriptions = driver.find_element_by_class_name('o-blocks').find_elements_by_tag_name('p')
        metadata = driver.find_element_by_id('dl-artwork-details')
    except: 
        exception = (1, index)
        return None
    for para_text in descriptions: 
        pars_dict['index'].append(index)
        pars_dict['artwork_title'].append(artwork_title)
        pars_dict['metadata'].append(metadata.text)
        pars_dict['description_text'].append(para_text.text.strip())
        pars_dict['url'].append(url)
    driver.close()
    return pd.DataFrame(pars_dict)

# Read the csv file that stores the links of each artwork, prepare to spider the website. 
artwork_df = pd.read_csv('artwork_title_and_link.csv')


# Spidering. 
description_list = []
description_df = pd.DataFrame()

for index, artwork in artwork_df.iterrows(): 
    if lb <= index < ub and (index - lb) % 30 == 0 and index != lb:
        print(f'Sleep for 120s to avoid censorship. You have finished {100*(index-lb)/(ub-lb)}%. ')
        time.sleep(120)
    elif lb <= index < ub and (index - lb) % 10 == 0 and index != lb: 
        print(f'Sleep for 10s to avoid censorship. You have finished {100*(index-lb)/(ub-lb)}%. ')
        time.sleep(10)
    if lb <= index < ub:
        ready = get_description(index, artwork['collection'], artwork['link'])
        if not isinstance(ready, pd.DataFrame): 
            break
        description_list.append(ready)

for description in description_list: 
    for index, para in description.iterrows():   
        if para['description_text'] == '' or para['description_text'].startswith('Object information is'): 
            continue
        description_df = description_df.append(para, ignore_index=True)


description_df.to_csv(f'{exception}_artwork_description_metadata_{lb}_{ub}.csv', index=False)