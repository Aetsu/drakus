from OTXv2 import OTXv2
import IndicatorTypes
from ..models import Artifact, Url
import logging

log_info = logging.getLogger('drakus.info')
log_error = logging.getLogger('drakus.error')

def search_otx_hash(query, api_key):
    d_res = {
        'otx_exists': 0,
        'otx_link': '-',
        'analysis_start_time': '-',
        'md5': '-', 
        'sha1': '-',
        'sha256': '-'
    }
    l_tags = ['md5', 'sha1', 'sha256']
    otx_analysis = None
    otx = OTXv2(api_key)
    try:
        if len(query) == 32:
            otx_res = otx.get_indicator_details_full(
                IndicatorTypes.FILE_HASH_MD5, query)
        elif len(query) == 40:
            otx_res = otx.get_indicator_details_full(
                IndicatorTypes.FILE_HASH_SHA1, query)
        elif len(query) == 64:
            otx_res = otx.get_indicator_details_full(
                IndicatorTypes.FILE_HASH_SHA256, query)
        else:
            d_res['ERROR'] = 'OTX query: INVALID HASH'
            log_error.error('search_otx_hash <OTX query: INVALID HASH' + '>')
            return d_res
        if 'analysis' in otx_res:
            if 'analysis' in otx_res['analysis']:
                otx_analysis = otx_res['analysis']['analysis']
                if otx_analysis is not None:
                    d_res['otx_exists'] = 1
                    if 'datetime_int' in otx_analysis:
                        d_res['analysis_start_time'] = otx_analysis['datetime_int']
                        d_res['otx_link'] = 'https://otx.alienvault.com/indicator/file/' + query
                        if 'info' in otx_analysis and 'results' in otx_analysis['info']:
                            otx_results = otx_analysis['info']['results']
                            for tag in l_tags:
                                if tag in otx_results:
                                    d_res[tag] = otx_results[tag]
                                else:
                                    d_res[tag] = '-'
    except Exception as e:
        d_res['ERROR'] = 'OTX artifact query: ' + str(e)
        log_error.error('search_otx_hash <OTX artifact query: ' + str(e) + '>')
    return d_res


def update_artifact_otx(object_id, otx_data):
    artifact_obj = Artifact.objects.get(pk=object_id)
    artifact_obj.otx_exists = otx_data['otx_exists']
    artifact_obj.otx_link = otx_data['otx_link']
    artifact_obj.hash_md5 = otx_data['md5']
    artifact_obj.hash_sha1 = otx_data['sha1']
    artifact_obj.hash_sha256 = otx_data['sha256']
    artifact_obj.save()


# def search_otx_url(query, api_key):
#     d_res = {
#         'otx_exists': 0,
#         'otx_link': 'https://otx.alienvault.com/indicator/url/' + query,
#         'analysis_start_time': '-',
#     }
#     otx_analysis = None
#     otx = OTXv2(api_key)
#     try:
#         otx_res = otx.get_indicator_details_full(IndicatorTypes.URL, query)
#         pulse_info = otx_res['general']['pulse_info']
#         d_res['otx_exists'] = int(pulse_info['count'])
#         url_list = otx_res['url_list']['url_list']
#         d_res['analysis_start_time'] = url_list[0]['date']
#     except Exception as e:
#         d_res['ERROR'] = 'OTX url query: ' + str(e)
#     return d_res

# def update_url_otx(object_id, otx_data):
#     url_obj = Url.objects.get(pk=object_id)
#     url_obj.otx_exists = otx_data['otx_exists']
#     url_obj.otx_link = otx_data['otx_link']
#     url_obj.save()
