import requests
from bs4 import BeautifulSoup
from pprint import pprint
import os
import json
from tqdm import tqdm


json_dir = 'json'

def get_river_info(num):
    url = "http://www.waterwaysguide.org.au/waterwaysguide/section/{}/partial"
    r = requests.get(url.format(num))
    html_content = r.text

    soup = BeautifulSoup(html_content, 'html.parser')

    # Deal with most rows
    rows = soup.select('div.section-left > div.detailrow')
    web_items = {}
    for row in rows:
        labels = [i.find(text=True) for i in row.select('span.rowlabel')]
        labels = [i.strip().replace(':','') for i in labels]
        values = row.select('div.rowtext') + row.select('div.rowtextlowercase')
        for label, text in zip(labels,values):
            web_items[label] = text

    # Handle the special cases
    for key in web_items:
        if 'POINT' in key:
            try:
                web_items[key] = web_items[key].select('span > a')[0]['href']
            except:
                web_items[key] = None
        else:
            web_items[key] = web_items[key].find(text=True)

    # Gauge link
    if 'GAUGE' in web_items:
        web_items['GAUGE'] = soup.select('span.new-river')[0].parent['href']

    # Section Heading 
    if 'SECTION HEADING' in web_items:
        web_items['SECTION HEADING'] = soup.select('div > h1')[0].find(text=True)

    if 'Latest water level' in web_items:
        web_items['Latest water level'] = web_items['Latest water level'].replace('m','').strip()
    
    web_items['URL_ID']=int(river_num)

    return web_items

# Get list of completed ids
json_file_list = [i.replace('.json','') for i in os.listdir(json_dir)]
# Get list of all ids
f = open('waterways_ids.txt','r')
# Don't download things that have already been finished
ids = [ filename for filename in f.read().split('\n') if filename not in json_file_list]

# Loop through every river that has not been downloaded.

for river_num in tqdm(ids):
    data = get_river_info(river_num)
    with open('{}/{}.json'.format(json_dir, river_num), 'w') as handle:
        json.dump(data, handle)
    # print('{} downloaded. Num:{}'.format(data['WATERWAY'],river_num))
