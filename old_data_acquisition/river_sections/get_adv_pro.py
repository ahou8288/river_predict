import requests
from bs4 import BeautifulSoup
from pprint import pprint
import json
from tqdm import tqdm

untitled_section_title = 'Desc'

url_start = 'https://www.adventurepro.com.au/paddleaustralia/pa.cgi?action=details&id='


def handle_soup(soup):
    # Find river name
    tag_info = {}


    try:
        river_name, section_name = soup.findAll('h4')
        tag_info['river_name'] = river_name.contents[0]
        tag_info['section_name'] = section_name.contents[0]
    except:
        tag_info['river_name'] = ''
        tag_info['section_name'] = ''

    section_tags = soup.findAll('section', {'class': 'row'})

    for section in section_tags:

        # Find the section title if it exists
        section_title = section.find('b')
        if section_title != None:
            section_title_str = section_title.string
            section_title.extract()
        else:
            section_title_str = untitled_section_title

        # Find the section content
        section_text = section.findAll('p')
        all_text = ''
        if section_text != None:
            for text_segment in section_text:
                all_text += text_segment.text.strip()

        if section_title_str and all_text:
            tag_info[section_title_str] = all_text

    return tag_info


def keep_valid_section(html_content):
    split_content = html_content.split('\n')
    end_ind, start_ind = 0, 0

    for index, line in enumerate(split_content):
        if '<!-- Details -->' in line:
            start_ind = index
        if '<!-- CGI Footer Split -->' in line:
            end_ind = index
            break

    cropped_content = '\n'.join(split_content[start_ind:end_ind])
    return cropped_content

# Get river list
with open('river_urls.txt', 'r') as handle:
    river_urls = handle.read().split('\n')
# Get list of finished rivers
import os
finished = os.listdir('adv_pro')
# Only download rivers that haven't already been downloaded
river_urls = [url for url in river_urls if url not in finished]

for river in tqdm(river_urls):
    r = requests.get(url_start + river)

    html_content = keep_valid_section(r.text)
    soup = BeautifulSoup(html_content, 'html.parser')
    data = handle_soup(soup)
    data['download_url'] = river

    # Save as json
    with open('adv_pro/{}.json'.format(river), 'w') as outfile:
        json.dump(data, outfile)
