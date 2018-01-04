import requests
from pprint import pprint
from bs4 import BeautifulSoup
from multiprocessing import Pool

print('Loading urls.')
with open('levels_urls.txt', 'r') as f:
    urls = f.read().split('\n')


def get_html(url):
    print('Getting data from {}'.format(url))
    try:
        r = requests.get(url)
    except:
        print('Request failed. Bad url?')
        return 'Error'
    print('Data received.')
    if r.status_code != 200:
        print(r.text)
        print(r.status_code)
        return 'Error'
    return r.text


def split_name(name):
    try:
        id_str = name.split(' ')[-1]
        id_str = id_str[1:len(id_str) - 1]
        river_name = name[:len(name) - len(id_str) - 3]
        return id_str, river_name
    except:
        return '0', name


def load_levels_table(url):
    # Store output in dictionary
    output = {}

    # Get data
    html_content = get_html(url)
    if html_content == 'Error':
        return {}

    # Convert data to python list
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find_all('table')[0]
    rows = table.find_all('tr')[3:]
    parsed_rows = [[td.contents[0]
                    for td in row.find_all('td')] for row in rows]

    # Handle bad values and stuff
    for river in parsed_rows:  # For every river downloaded
        river_id, river_name = split_name(river[0])
        if river_id != '0':  # Only keep real rivers
            observation_list = []
            # For every reading in the row convert the text to a numeric type
            for index, reading_text in enumerate(river[1:]):
                try:
                    # strip out comma character
                    val = float(reading_text.replace(',', ''))
                except:
                    # Use nan for bad values.
                    val = float('nan')
                observation_list.append(val)
            # add the list of values to the dictionary
            levels, discharge = observation_list[::2], observation_list[1::2]
            output[river_id] = {
                'levels': levels,
                'discharge': discharge,
                'name': river_name
            }
        else:
            print(river)  # for debugging
    return output

# Loop through all urls and load the rivers
all_rivers = {}
for url in urls:
    all_rivers.update(load_levels_table(url))

pprint(all_rivers)
