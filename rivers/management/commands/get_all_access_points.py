import requests
from bs4 import BeautifulSoup
import os
import json

filepath = 'json/'
filelist = os.listdir(filepath)


def get_data(point_num):

    base_url = 'http://www.waterwaysguide.org.au/waterwaysguide/access-point/{}/partial'

    print('Requesting access-point info for {}'.format(point_num))

    r = requests.get(base_url.format(point_num))
    html_content = r.text
    soup = BeautifulSoup(html_content, 'html.parser')
    page_data = {}
    mydivs = soup.findAll("div", {"class": "title", "itemprop": "name"})

    # Find the page title
    if len(mydivs):
        myheading = mydivs[0].findAll("h1")
        if len(myheading):
            page_data['title'] = myheading[0].find(text=True)

    rows = soup.select('div.section-left > div.detailrow')
    for row in rows:
        labels = [i.find(text=True) for i in row.select('span.rowlabel')]
        labels = [i.strip().replace(':', '') for i in labels]
        values = row.select('div.rowtext') + row.select('div.rowtextlowercase')
        for label, text in zip(labels, values):
            if 'Latitude' in label or 'Longitude' in label:
                page_data[label] = text.find(text=True)

    return page_data

required_points = set()

for i in filelist:
    with open(filepath + i, 'r') as handle:
        data = json.load(handle)
    if 'ENTRY POINT' in data and data['ENTRY POINT'] and len(data['ENTRY POINT']) > 20:
        required_points.add(data['ENTRY POINT'][20:])
    if 'EXIT POINT' in data and data['EXIT POINT'] and len(data['EXIT POINT']) > 20:
        required_points.add(data['EXIT POINT'][20:])

print(required_points)

for point in required_points:
    data = get_data(point)
    save_path = 'json_points/' + point + '.json'
    with open(save_path, 'w') as handle:
        json.dump(data, handle)
