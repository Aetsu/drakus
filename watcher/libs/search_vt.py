import requests
from ..models import Artifact
import logging

log_info = logging.getLogger('drakus.info')
log_error = logging.getLogger('drakus.error')


def search_vt_hash(hash, api_key):
    url = 'https://www.virustotal.com/vtapi/v2/file/report'
    params = {'apikey': api_key, 'resource': hash}
    response = requests.get(url, params=params)
    d_res = {}
    if response.status_code == 200:
        vt_data = response.json()
        l_tags = ['response_code', 'scan_date', 'permalink',
                  'total', 'positives', 'md5', 'sha256', 'sha1']
        for tag in l_tags:
            if tag in vt_data:
                d_res[tag] = vt_data[tag]
            else:
                d_res[tag] = '-'
    else:
        d_res['ERROR'] = 'VT Status code: ' + str(response.status_code)
        log_error.error('search_vt_hash <VT Status code: ' + str(response.status_code) + '>')
    return d_res


def update_artifact_vt(object_id, vt_data):
    artifact_obj = Artifact.objects.get(pk=object_id)
    artifact_obj.vt_exists = vt_data['response_code']
    artifact_obj.vt_link = vt_data['permalink']
    artifact_obj.hash_md5 = vt_data['md5']
    artifact_obj.hash_sha1 = vt_data['sha1']
    artifact_obj.hash_sha256 = vt_data['sha256']
    artifact_obj.save()
