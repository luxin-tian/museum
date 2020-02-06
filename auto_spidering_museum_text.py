import pandas as pd #gives us DataFrames
import numpy as np
import time
from selenium import webdriver


print('Currently this script runs on macOS with Chrome v7.9 or Linux with Firefox')
system = input('Select your OS (macOS/Linux): ')
headless = input('Would you like to run with headless mode (not displaying)? y/n: ')
if system == 'macOS': 
    if headless == 'y': 
        options = webdriver.chrome.options.Options()
        options.headless = True
    driver_path = webdriver.Chrome(options=options, executable_path='./chromedriver')
elif system == 'Linux': 
    if headless == 'y': 
        options = webdriver.firefox.options.Options()
        options.headless = True
    driver_path = webdriver.Firefox(options=options, executable_path='./geckodriver')

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
if headless == 'y': 
    print()
    print('Chrome is running in a headless mode. ')
else: 
    print()
    print('Please DO NOT operate the automatically-running Chrome windows. This task can take hours, depending on your internet connection.')
    print('You may enjoy some pictures from the Art Institute of Chicago.\n')

# Write a function that spider content from a link and returns a DataFrame. 
def get_description(index, artwork_title, url): 
    global exception
    exception = 0
    pars_dict = {'index':[], 'artwork_title' : [], 'metadata': [], 'description_text' : [], 'url' : []}
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
    return pd.DataFrame(pars_dict)

# Read the csv file that stores the links of each artwork, prepare to spider the website. 
artwork_df = pd.read_csv('artwork_title_and_link.csv')

def start_driver(): 
    global driver
    if system == 'macOS': 
        if headless == 'y': 
            options = webdriver.chrome.options.Options()
            options.headless = True
        driver = webdriver.Chrome(options=options, executable_path='./chromedriver')
    elif system == 'Linux': 
        if headless == 'y': 
            options = webdriver.firefox.options.Options()
            options.headless = True
        driver = webdriver.Firefox(options=options, executable_path='./geckodriver')


def restart_driver(): 
    global driver
    driver.close
    start_driver()

# Spidering. 
def spidering(lb, ub): 
    global catch_exception
    catch_exception = 0
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
                catch_exception = 1
                break
            description_list.append(ready)

    for description in description_list: 
        for index, para in description.iterrows():   
            if para['description_text'] == '' or para['description_text'].startswith('Object information is'): 
                continue
            description_df = description_df.append(para, ignore_index=True)


    description_df.to_csv(f'{exception}_artwork_description_metadata_{lb}_{ub}.csv', index=False)


def main(lb, ub): 
    global catch_exception
    node = lb
    even_odd = 0
    start_driver()
    while node < ub: 
        if ub - node <= 50: 
            spidering(node, ub)
            if catch_exception == 1: 
                print('The task has been censored, sleep for one hour and then resume. ')
                lb = exception[1]
                ub = ub
                time.sleep(60*40)
                break
        else: 
            spidering(node, node + 50)
            if catch_exception == 1: 
                print('The task has been censored, sleep for one hour and then resume. ')
                lb = exception[1]
                ub = ub
                time.sleep(60*40)
                break
            if even_odd % 2 == 0:
                time.sleep(60 * 5)
                restart_driver()
            elif even_odd % 2 == 1: 
                time.sleep(60*15)
                restart_driver()
            if even_odd % 3 == 0: 
                time.sleep(60*40)
                restart_driver()
        even_odd += 1
        node += 50
    if catch_exception == 1: 
        print('Restarting...')
        catch_exception = 0
        restart_driver()
        main(lb, ub)

start_driver()
main(lb, ub)