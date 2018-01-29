import requests
# Get the list of guides
f = open('waterways_ids.txt','r')
ids = f.read()

def get_one_page(river_id):
    base_url_str = 'http://www.waterwaysguide.org.au/waterwaysguide/section/{}/partial'
    r = requests.get(base_url_str.format(river_id))
    return r.text

print(get_one_page('6361'))
