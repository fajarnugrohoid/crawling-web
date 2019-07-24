from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    print(e.encode('utf-8'))

def get_names(link_url):
    """
    Downloads the page where the list is found
    and returns a list of strings
    """
    url = link_url
    response = simple_get(url)

    if response is not None:
        html = BeautifulSoup(response, 'html.parser')
        print(html)
        names = set()
        for li in html.select('li'):
            for name in li.text.split('\n'):
                if len(name) > 0:
                    names.add(name.strip())
        return list(names)

    # Raise an exception if we failed to get any data from the url
    raise Exception('Error retrieving contents at {}'.format(url))

def get_links(link_url):
    url = link_url
    response = simple_get(url)
    if response is not None:
        html = BeautifulSoup(response, 'html.parser')
        names = set()
        for a in html.select('a'):
            msg = 'url:%s -> href:%s ' % (a.text, a.get('href'))
            #print("xxx->" + msg.encode('utf-8'))
            print(link_url)
            names.add(link_url + a.get('href').encode('utf-8'))
            #if (link_url in a.get('href')):
            #    names.add(a.get('href'))

        print(list(names))
        return list(names)
    # Raise an exception if we failed to get any data from the url
    raise Exception('Error retrieving contents at {}'.format(url))

def get_hits_on_name(name):
    # url_root is a template string that is used to build a URL.
    url_root = 'URL_REMOVED_SEE_NOTICE_AT_START_OF_ARTICLE'
    response = simple_get(url_root.format(name))
    print('response:' + response)

    if response is not None:
        html = BeautifulSoup(response, 'html.parser')
        print(html)
        hit_link = [a for a in html.select('a')
		        if a['href'].find('latest-60') > -1]
        if len(hit_link) > 0:
            # Strip commas
            link_text = hit_link[0].text.replace(',', '')
            try:
                # Convert to integer
				return int(link_text)
            except:
                log_error("couldn't parse {} as an `int`".format(link_text))
				
    log_error('No pageviews found for {}'.format(name))
    return None