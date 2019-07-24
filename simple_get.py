from lib_parse import simple_get, get_names, get_hits_on_name, is_good_response, log_error, get_links
from bs4 import BeautifulSoup
import sys

link_url = 'https://www.guru99.com/'
'''
raw_html = simple_get(link_url)
print(len(raw_html))

raw_html = open('index.html').read()
print(raw_html)get_hits_on_name
html = BeautifulSoup(raw_html, 'html.parser')
for p in html.select('p'):
	if p['id'] == 'walrus':
		print(p.text)
'''
print('Getting the list of lists....')
get_all_links = get_links(link_url)
print('... done.\n')
print(get_all_links)
for links in get_all_links:
	print(links)
	print('Getting the list of names....')
	names = get_names(links)
	results = []
	print('Getting stats for each name....\n')
	for name in names:
		try:
			hits = get_hits_on_name(name)
			if hits is None:
				hits = -1
			results.append((hits, name))
		except Exception as e:
			results.append((-1, name))
			log_error('error encountered while processing %s, skipping' %(name))
		else:
			pass
		finally:
			pass
	