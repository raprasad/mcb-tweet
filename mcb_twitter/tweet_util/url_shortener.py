import httplib
import json

ST_OK_200 = 200
def shorten_url(long_url):
    """
    in: full url
    out: shortened url or None
    
    Shorten a google  url. Expected response from google:
    {
     "kind": "urlshortener#url",
     "id": "http://goo.gl/KZEFb",
     "longUrl": "https://www.mcb.harvard.edu/mcb/news/news-detail/3669/how-does-e-coli-segregate-its-sisters-without-a-spindle-kleckner-lab/"
    }
    """
    if long_url is None:
        return None

    if not long_url.startswith('http') and long_url.find('www.mcb.harvard.edu') > -1:
        long_url = 'https://%s' % long_url
        
    google_server_address = 'www.googleapis.com'
    google_url_shortener = '/urlshortener/v1/url'

    data = json.dumps({"longUrl": long_url})
    headers = {"Content-type": "application/json"}

    try:
        server_conn = httplib.HTTPSConnection(google_server_address)
        server_conn.request('POST', google_url_shortener, data, headers)
        response = server_conn.getresponse()
        if not response.status == ST_OK_200:
            return None
        data = response.read()
        data_dict = json.loads(data)
    except:
        return None
    
    returned_long_url = data_dict.get('longUrl', '')
    if returned_long_url.endswith(long_url):
        return data_dict.get('id', None)
    return None

if __name__=='__main__':
    ns_url = 'https://www.mcb.harvard.edu/mcb/news/news-detail/3669/how-does-e-coli-segregate-its-sisters-without-a-spindle-kleckner-lab/'
    print shorten_url(ns_url)
