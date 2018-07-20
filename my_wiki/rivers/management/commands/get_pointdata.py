import requests
from bs4 import BeautifulSoup
import re

def get_data(point_num):

    base_url = 'http://www.waterwaysguide.org.au/waterwaysguide/access-point/{}/partial'
    r = requests.get(base_url.format(point_num))
    html_content = r.text
    soup = BeautifulSoup(html_content, 'html.parser')
    page_data = {}
    mydivs = soup.findAll("div", {"class": "title", "itemprop":"name"})

    # Find the page title
    if len(mydivs):
        myheading = mydivs[0].findAll("h1")
        if len(myheading):
            page_data['title']=myheading[0].find(text=True)
    
    rows = soup.select('div.section-left > div.detailrow')
    for row in rows:
        labels = [i.find(text=True) for i in row.select('span.rowlabel')]
        labels = [i.strip().replace(':','') for i in labels]
        values = row.select('div.rowtext') + row.select('div.rowtextlowercase')
        for label, text in zip(labels,values):
            if 'Latitude' in label or 'Longitude' in label:
                page_data[label] = text.find(text=True)
    return page_data

print(get_data(4980))
