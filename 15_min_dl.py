import requests


def get_river():
    # Download a river

    # url = "http://realtimedata.water.nsw.gov.au/cgi/webhyd.pl?co=204001&t=rscf_org&v=100.00_100.00_CP,100.00_141.00_CP&vn=Stream+Water+Level,Discharge+Rate&ds=CP,CP&p=Custom,1,1,custom,1&pp=0,0&r=level,rate&o=Download,download&i=15+minutes,Minute,15&cat=rs&d1=00:00_20/12/2012&d2=00:00_20/12/2017&1513713623806"
    url = "http://realtimedata.water.nsw.gov.au/cgi/webhyd.pl?co=204001&t=rscf_org&v=100.00_100.00_CP,100.00_141.00_CP&vn=Stream+Water+Level,Discharge+Rate&ds=CP,CP&p=Custom,1,1,custom,1&pp=0,0&r=level,rate&o=Download,download&i=15+minutes,Minute,15&cat=rs&d1=00:00_20/12/2012&d2=00:00_20/12/2017&1513716366231"

    # Default cookies
    cookies = {
        'fontsize': '80.01',
        'plotsize': 'normal',
        'username': 'webuser',
        'userid': '818542479',
        'userclass': 'anon',
        'is_admin': '0',
        'language': 'English',
        'menu_width': '20'
    }

    # Ask website to prepare download
    r = requests.get(url, cookies=cookies)

    # Extract download link from response
    response_text = r.text
    # print(response_text)

    # Check that download link exists
    if 'login has timed out' in response_text:
        print('Invalid cookies/request. Download failed.')
        return
    elif not 'downloadlink' in response_text:
        print('no download avaliable')
        return

    # Search for the right line
    for line in response_text.split('\n'):
        print(line)
        if 'downloadlink' in line:
            download_url = line.split('onclick="location.href=\'')[1]
            download_url = download_url.split('\';" id="downloadlink">')[0]

    print(download_url)

    # Download the zip from the url in the response.
    r2 = requests.get(download_url, cookies)

    print('Downlaod complete.')

get_river()
