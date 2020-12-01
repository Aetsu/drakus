import requests
from ..models import Url
import logging

log_info = logging.getLogger('drakus.info')
log_error = logging.getLogger('drakus.error')

def search_urlscan_url(query):
    query = query.replace('https://','').replace('http://','')
    d_res = {
        'urlscan_exists':0,
        'urlscan_link':'https://urlscan.io/result/',
        'first_search': '-',
    }
    url = 'https://urlscan.io/api/v1/search/'
    payload = {'q': 'domain:' + query}
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }
    try:
        r = requests.get(url, params=payload, headers=headers)
        if r.status_code == 200:
            urlscan_data = r.json()
            if len(urlscan_data['results']) > 0:
                urlscan_data = urlscan_data['results'][0]
                d_res['urlscan_exists'] = 1
                d_res['first_search'] = urlscan_data['task']['time']
                d_res['urlscan_link'] += urlscan_data['_id']
    except Exception as e:
        d_res['ERROR'] = 'Urlscan.io query: ' + str(e)
        log_error.error('search_urlscan_url <Urlscan.io query: ' + str(e) +'>')
    return d_res

def update_url_urlscan(object_id, urlscan_data):
    url_obj = Url.objects.get(pk=object_id)
    url_obj.urlscan_exists = urlscan_data['urlscan_exists']
    url_obj.urlscan_link = urlscan_data['urlscan_link']
    url_obj.save()