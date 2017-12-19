import requests
url = "http://realtimedata.water.nsw.gov.au/cgi/webhyd.pl?co=204001&t=rscf_org&v=100.00_100.00_CP,100.00_141.00_CP&vn=Stream+Water+Level,Discharge+Rate&ds=CP,CP&p=Custom,1,1,custom,1&pp=0,0&r=level,rate&o=Download,download&i=15+minutes,Minute,15&cat=rs&d1=00:00_20/12/2012&d2=00:00_20/12/2017&1513713623806"

cookies = {
    'fontsize': '80.01',
    'plotsize': 'normal',
    'username': 'webuser',
    'userid': '341156005',
    'userclass': 'anon',
    'is_admin': '0',
    'language': 'English',
    'menu_width': '20'
}

r = requests.get(url, cookies=cookies)

response_text = r.text
print(r.text)

for line in response_text.split('\n'):
    if 'more than 2000 lines returned' in line:
        download_url = line[89:]
        download_url = download_url[:len(download_url)-64]
        break

print(download_url)