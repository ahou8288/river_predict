import requests
from bs4 import BeautifulSoup

f = open('urls.txt','w')
with open('pages.txt','r') as handle:
    pages = handle.read().split('\n')

for page in pages:
    r=requests.get(page)
    soup = BeautifulSoup(r.text, 'html.parser')
    mydivs = soup.findAll("a", {"target": "_self"}, href=True)
    for i in mydivs:
        f.write('https://www.adventurepro.com.au/paddleaustralia/{}\n'.format(i['href']))
