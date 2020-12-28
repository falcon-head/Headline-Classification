"""

__foldername__ = Headline-Classification
__filename__ = crawl_gauradian.py
__author__ = Shrikrishna Joisa
__date_created__ = 25/07/2020
__date_last_modified__ =  28/12/2020
__python_version__ = 3.7.4 64-bit

"""

import numpy as np
import pandas as pd
import json
import bs4 as bs4
import datetime
import config
import requests
import time
from tqdm import tqdm

def capture_data():

    """
    Capture the data from the gaurdian api
    """

    # List of category data to capture from the gaurdian news
    category_list = ['technology', 'business', 'culture', 'environment', 'fashion', 'film', 'food', 'lifeandstyle', 'politics', 'science',
    'football', 'sport', 'travel', 'music']

    #category_list = ['technology', 'science', 'fashion', 'culture', 'travel']

    # The api url
    api_url = "https://content.guardianapis.com/search?section={section}"

    # The api date
    api_date="from-date=2018-01-01&to-date=2020-12-26"

    # the api page
    api_page="page={number}"

    # number of article in a page
    api_article_number = 199

    # size of the page for api
    api_page_size = ''.join(['page-size=',str(api_article_number)])

    # fields for the api
    fields='format=json&show-fields=all&use-date=newspaper-edition'

    # api key
    api_key = config.gaurdian_api_key    # Create a config.py file and create a variable gaurdian_api_key with your API key

    # Create the api url and extract the data
    url_link = [api_url, api_date, api_page, api_page_size, fields, api_key]
    initial_url = "&".join(url_link)

    # List to store the data
    item_list = []

    # Loop through the categories and capture the response
    for section_name in tqdm(category_list):
        for j in range(10):
            time.sleep(6)
            # The URL
            url = initial_url.format(section = section_name, number = j+1)
            response = requests.get(url)
            data = response.json()
            try:
                results = data['response']['results']
                for i in results:
                    # Capture the item and append it to a list
                    item = {}
                    item["Heading"] = i['webTitle']
                    item["Category"] = i['sectionName']
                    item["URL"] = i['webUrl']
                    item["Field Heading"]= i['fields']['headline']
                    print(item)
                    item_list.append(item)
            except:
                print("nice")

    # Article data
    df = pd.DataFrame(item_list)
    df.to_csv('article_others.csv', index=False)


if __name__ == "__main__":
    capture_data()
