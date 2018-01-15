import requests
from bs4 import BeautifulSoup
from pprint import pprint

url = "http://www.waterwaysguide.org.au/waterwaysguide/section/{}/partial"
num = 6361 #7636
r = requests.get(url.format(num))
html_content = r.text

# with open('cached_web_request.html','w') as f:
#     f.write(html_content)
# with open('cached_web_request.html','r') as f:
#     html_content = f.read()

soup = BeautifulSoup(html_content, 'html.parser')

# Deal with most rows
rows = soup.select('div.section-left > div.detailrow')
web_items = {}
for row in rows:
    labels = [i.find(text=True) for i in row.select('span.rowlabel')]
    values = row.select('div.rowtext') + row.select('div.rowtextlowercase')
    for label, text in zip(labels,values):
        web_items[label] = text

# Handle the special cases
for key in web_items:
    if 'POINT' in key:
        web_items[key] = web_items[key].select('span > a')[0]['href']
    else:
        web_items[key] = web_items[key].find(text=True)

# Gauge link
web_items['GAUGE'] = soup.select('span.new-river')[0].parent['href']
# Section Heading 
web_items['SECTION HEADING'] = soup.select('div > h1')[0].find(text=True)

pprint(web_items)