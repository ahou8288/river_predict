import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

sessions = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
sessions.mount('http://', adapter)
sessions.mount('https://', adapter)

from time import sleep


def get_river(river_num, year_start, year_end, discharge=False):
    # Download a river

    # Build the url
    url = (
        "http://realtimedata.water.nsw.gov.au/cgi/webhyd.pl?co={river}"
        "&t=rscf_org&v=100.00_100.00_CP{discharge1}"
        "&vn=Stream+Water+Level{discharge2}&ds"
        "=CP{discharge3}&p=Custom,1,1,custom,1&pp=0{discharge4}"
        "&r=level{discharge5}&o=Download,download&i=15+minutes,Minute,15&cat=rs&d1=00:00_"
        "{start_date}&d2=00:00_{end_date}&1"
    )
    url_args = {
        'river': river_num,
        'discharge1': ",100.00_141.00_CP" if discharge else "",
        'discharge2': ",Discharge+Rate" if discharge else "",
        'discharge3': ",CP" if discharge else "",
        'discharge4': ",0" if discharge else "",
        'discharge5': ",rate" if discharge else "",
        'start_date': "01/01/{}".format(year_start),
        'end_date': "01/01/{}".format(year_end)
    }
    url = url.format(**url_args)

    # Default cookies
    cookies = {
        'fontsize': '80.01',
        'plotsize': 'normal',
        'username': 'webuser',
        'userid': '341369628',
        'userclass': 'anon',
        'is_admin': '0',
        'language': 'English',
        'menu_width': '20'
    }

    # Ask website to prepare download
    sleep(4)
    try:
        r = sessions.get(url, cookies=cookies)
    except requests.exceptions.ConnectionError:
        print("Connection refused")
        return

    # Extract download link from response
    response_text = r.text

    # Check that download link exists
    if 'login has timed out' in response_text:
        print('Invalid cookies/request. Download failed.')
        print(response_text)
        return
    elif not 'downloadlink' in response_text:
        print('no download avaliable')
        print(response_text)
        return

    # Search for the right line
    for line in response_text.split('\n'):
        if 'downloadlink' in line:
            download_url = line.split('location.href=\\\'')[1]
            download_url = download_url.split('\\\';" id="downloadlink">')[0]

    # Download the zip from the url in the response.
    sleep(4)
    try:
        r2 = sessions.get(download_url, cookies)
    except requests.exceptions.ConnectionError:
        print("Connection refused")
        return

    # Create download filename
    download_name = "river_{}_{}_{}.zip".format(
        river_num, year_start, year_end)

    # Write info to file
    with open(download_name, "wb") as zip_file:
        zip_file.write(r2.content)
    print('Download complete.')

for i in range(1950, 2020, 10):
    # print(i)
    print('Downloading year {} to {}.'.format(i, i + 10))
    get_river(204001, i, i + 1, False)
    break
