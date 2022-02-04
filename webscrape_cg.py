#!/usr/bin/env python
# coding: utf-8

# In[4]:


import numpy as np
import pandas as pd
import requests
import re
from bs4 import BeautifulSoup

import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.by import By


# In[9]:


# Check for latest file to load.
file_title = f'cg_comp_list'
coins_df = pd.read_csv(f'{file_title}.csv')


# In[10]:


coins_df


# In[11]:


#get pass Cloudfare anti-ddos
driver = uc.Chrome()


# In[114]:


def bs4_requests(name_):
    soup_dict = {}
    soup_dict['cg_id'] = name_
    with driver:
        driver.get(f'https://www.coingecko.com/en/coins/{name_}')
    page_source = driver.page_source
#     if page.status_code == 404:
#         logger.error(f'{name_} has error code - {page.status_code}')
#         print(f'{name_} has error code - {page.status_code}')
#         soup_dict['cg_watchlist_count'] = None
#     else:
    soup = BeautifulSoup(page_source, 'html.parser')
    try:
        token_price = soup.find('div', string = re.compile("Rank")).next_sibling.next_sibling.next_sibling.next_sibling.find('span', attrs = {"data-target":"price.price"}).text
        soup_dict['token_price'] = float(''.join(token_price.strip("$").split(',')))
    except:
        soup_dict['token_price'] = None
    try:
        circ_supply = soup.find(string = re.compile('Circulating Supply')).parent.parent.next_sibling.next_sibling.text
        soup_dict['circ_supply'] = float(''.join(circ_supply.strip('\n').split(',')))
    except:
        soup_dict['circ_supply'] = None
    try:
        total_supply = soup.find(string = re.compile('Total Supply')).parent.parent.next_sibling.next_sibling.text
        soup_dict['total_supply'] = float(''.join(total_supply.strip('\n').split(',')))
    except:
        soup_dict['total_supply'] = None
    try:
        max_supply = soup.find(string = re.compile('Max Supply')).parent.next_sibling.next_sibling.text
        soup_dict['max_supply'] = float(''.join(max_supply.strip('\n').split(',')))
    except:
        soup_dict['max_supply'] = None
    try:
        tvl = soup.find(string = re.compile('Total Value Locked')).parent.next_sibling.next_sibling.text
        soup_dict['tvl'] = float(''.join(tvl.strip('$').split(',')))
    except:
        soup_dict['tvl'] = None
    try:
        like_count = soup.find(string = re.compile(' people like this'))
        soup_dict['cg_watchlist_count'] = int(''.join(like_count.split(' ')[1].split(',')))
    except:
        soup_dict['cg_watchlist_count'] = None
    return soup_dict


# In[115]:


total = len(coins_df) - 1
count = 0

soups = []
for name in coins_df['token_id']:
    print(f'{count}/{total}: {name}')
    soup_d = bs4_requests(name)
    soups.append(soup_d)
    count+=1


# In[126]:


soups_df = pd.DataFrame(soups)


# In[127]:


soups_df['market_cap'] = soups_df['token_price'] * soups_df['circ_supply']
soups_df['fdv'] = soups_df['token_price'] * soups_df['max_supply']
soups_df['mc_tvl_ratio'] = soups_df['market_cap'] / soups_df['tvl']
soups_df['fdv_tvl_ratio'] = soups_df['fdv'] / soups_df['tvl']


# In[128]:


soups_df


# In[ ]:




