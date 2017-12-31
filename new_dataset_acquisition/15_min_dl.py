import requests
from time import sleep


def get_river(river_num, year_start, year_end, discharge=False):
    # Download a river

    # Build the url
    print('Building the url for request.')
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
        'userid': '942108153',
        'userclass': 'anon',
        'is_admin': '0',
        'language': 'English',
        'menu_width': '20'
    }

    print('Request ready: url = {}'.format(url))
    # Ask website to prepare download
    try:
        r = requests.get(url, cookies=cookies)
    except requests.exceptions.ConnectionError:
        print("Connection refused")
        return

    # Extract download link from response
    response_text = r.text
    print('Request complete. Searching for download link.')
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
        print('Sending download request.')
        r2 = requests.get(download_url, cookies)
    except requests.exceptions.ConnectionError:
        print("Connection refused")
        return

    # Create download filename
    download_name = "river_{}_{}_{}.zip".format(
        river_num, year_start, year_end)

    # Write info to file
    print('Writing downloaded data to file.')
    with open(download_name, "wb") as zip_file:
        zip_file.write(r2.content)
    print('Saving file complete.')

year_interval = 5
for i in range(1955, 2020, year_interval):
    # print(i)
    print('Downloading year {} to {}.'.format(i, i + year_interval))
    get_river(204001, i, i + year_interval, True)
