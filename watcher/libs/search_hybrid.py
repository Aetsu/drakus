import requests
from ..models import Artifact
import logging

log_info = logging.getLogger('drakus.info')
log_error = logging.getLogger('drakus.error')


def search_hybdrid_hash(query, api_key):
    d_res = {}
    url = 'https://www.hybrid-analysis.com/api/v2/search/hash'
    payload = {'hash': query}
    headers = {
        'accept': 'application/json',
        'user-agent': 'Falcon Sandbox',
        'Content-Type': 'application/x-www-form-urlencoded',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        'api-key': api_key
    }
    try:
        r = requests.post(url, data=payload, headers=headers)
        if r.status_code == 200:
            hybrid_data = r.json()
            l_tags = ['verdict', 'analysis_start_time',
                      'threat_score', 'av_detect', 'md5', 'sha256', 'sha1']
            if len(hybrid_data) == 0:
                d_res['hybrid_exists'] = 0
                d_res['hybrid_link'] = '-'
            else:
                hybrid_data = hybrid_data[0]
                d_res['hybrid_exists'] = 1
                d_res['hybrid_link'] = 'https://www.hybrid-analysis.com/sample/' + \
                    hybrid_data['sha256']
            for tag in l_tags:
                if tag in hybrid_data:
                    d_res[tag] = hybrid_data[tag]
                else:
                    d_res[tag] = '-'
        else:
            log_error.error('search_hybdrid_hash <Hybrid query: ' + str(e) + '>')
    except Exception as e:
        d_res['ERROR'] = 'Hybrid query: ' + str(e)
        log_error.error('search_hybdrid_hash <Hybrid query: ' + str(e) + '>')
    return d_res


def update_artifact_hybrid(object_id, hybrid_data):
    artifact_obj = Artifact.objects.get(pk=object_id)
    artifact_obj.hybrid_exists = hybrid_data['hybrid_exists']
    artifact_obj.hybrid_link = hybrid_data['hybrid_link']
    artifact_obj.hash_md5 = hybrid_data['md5']
    artifact_obj.hash_sha1 = hybrid_data['sha1']
    artifact_obj.hash_sha256 = hybrid_data['sha256']
    artifact_obj.save()
