from datetime import datetime
from django.conf import settings

from ..models import Artifact, Url, Config
from ..libs.search_vt import search_vt_hash, update_artifact_vt
from ..libs.search_hybrid import search_hybdrid_hash, update_artifact_hybrid
from ..libs.search_otx import search_otx_hash, update_artifact_otx
from ..libs.search_urlscan import search_urlscan_url, update_url_urlscan
from ..libs.project_helpers import get_project_info_helper
from ..libs.artifact_helpers import update_artifact_date_helper
from ..libs.url_helpers import update_url_date_helper

from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import logging

log_info = logging.getLogger('drakus.info')
log_error = logging.getLogger('drakus.error')


def updater():
    # artifacts_time = Config.objects.get('')
    scheduler = BackgroundScheduler()
    scheduler.add_job(search_enabled_artifacts_helper, 'interval', minutes=settings.ARTIFACTS_TIMER)
    scheduler.add_job(search_enabled_url_helper, 'interval', minutes=settings.DOMAINS_TIMER)
    scheduler.start()


def search_artifact_helper(hash_query, c_project_id):
    d_response = {
        'artefact_vt_info': {},
        'artefact_hybrid_info': {},
        'artefact_otx_info': {}
    }
    c_project = get_project_info_helper(c_project_id)
    try:
        vt_response = search_vt_hash(hash_query, c_project.vt_api)
        if not 'ERROR' in vt_response:
            d_response['artefact_vt_info'] = vt_response
            log_info.info('search_vt_hash: <' + hash_query + ': ' + str(vt_response['positives']) + '/' + str(vt_response['total']) + '>')
    except Exception as e:
        log_error.error('search_artifact_helper VT <' + str(e) + '>')
    try:
        hybrid_response = search_hybdrid_hash(hash_query, c_project.hybrid_api)
        if not 'ERROR' in hybrid_response:
            d_response['artefact_hybrid_info'] = hybrid_response
            log_info.info('search_hybrid_hash: <' + hash_query + ': ' + str(hybrid_response['av_detect']) + '% (' + str(hybrid_response['verdict']) + ')>')
    except Exception as e:
        log_error.error('search_artifact_helper Hybrid <' + str(e) + '>')
    try:
        otx_response = search_otx_hash(hash_query, c_project.otx_api)
        if not 'ERROR' in otx_response:
            d_response['artefact_otx_info'] = otx_response
            if otx_response['otx_link'] != '-':
                log_info.info('search_otx_hash: <' + hash_query + ': 1>')
            else:
                log_info.info('search_otx_hash: <' + hash_query + ': 0>')
    except Exception as e:
        log_error.error('search_artifact_helper OTX <' + str(e) + '>')
    return d_response


def search_project_artifact_helper(artifact_id):
    artifact_obj = Artifact.objects.get(id=artifact_id)
    update_artifact_date_helper(artifact_id)
    c_project = artifact_obj.project
    try:
        vt_response = search_vt_hash(artifact_obj.hash_query, c_project.vt_api)
        if not 'ERROR' in vt_response:
            log_info.info('VT:' + artifact_obj.hash_query +
                          ': ' + str(vt_response['response_code']))
            update_artifact_vt(artifact_id, vt_response)
        else:
            log_error.error('search_project_artifact_helper <' +
                            vt_response['ERROR'] + '>')
    except Exception as e:
        log_error.error(
            'search_project_artifact_helper <VT search/update DB ' + str(e) + '>')

    try:
        hybrid_response = search_hybdrid_hash(
            artifact_obj.hash_query, c_project.hybrid_api)
        if not 'ERROR' in hybrid_response:
            log_info.info('Hybrid:' + artifact_obj.hash_query +
                          ': ' + str(hybrid_response['hybrid_exists']))
            update_artifact_hybrid(artifact_id, hybrid_response)
        else:
            log_error.error('search_project_artifact_helper <' +
                            hybrid_response['ERROR'] + '>')
    except Exception as e:
        log_error.error(
            'search_project_artifact_helper <Hybrid search/update DB ' + str(e) + '>')

    try:
        otx_response = search_otx_hash(
            artifact_obj.hash_query, c_project.otx_api)
        if not 'ERROR' in otx_response:
            log_info.info('Otx:' + artifact_obj.hash_query +
                          ': ' + str(otx_response['otx_exists']))
            update_artifact_otx(artifact_id, otx_response)
        else:
            log_error.error('search_project_artifact_helper <' +
                            otx_response['ERROR'] + '>')
    except Exception as e:
        log_error.error(
            'search_project_artifact_helper <Error: OTX search/update DB ' + str(e) + '>')


def search_enabled_artifacts_helper(project_id=None):
    if project_id is None:
        artifact_l = Artifact.objects.filter(enabled=1).all()
    else:
        artifact_l = Artifact.objects.filter(
            enabled=1).filter(project=project_id).all()
    for artifact_obj in artifact_l:
        update_artifact_date_helper(artifact_obj.id)
        artifact_project = artifact_obj.project
        try:
            vt_response = search_vt_hash(
                artifact_obj.hash_query, artifact_project.vt_api)
            if not 'ERROR' in vt_response:
                log_info.info('VT:' + artifact_obj.hash_query +
                              ': ' + str(vt_response['response_code']))
                update_artifact_vt(artifact_obj.id, vt_response)
            else:
                log_error.error(
                    'search_enabled_artifacts_helper <' + vt_response['ERROR'] + '>')
        except Exception as e:
            log_error.error(
                'search_enabled_artifacts_helper <VT search/update DB ' + str(e) + '>')
        try:
            hybrid_response = search_hybdrid_hash(
                artifact_obj.hash_query, artifact_project.hybrid_api)
            if not 'ERROR' in hybrid_response:
                log_info.info('Hybrid:' + artifact_obj.hash_query +
                              ': ' + str(hybrid_response['hybrid_exists']))
                update_artifact_hybrid(artifact_obj.id, hybrid_response)
            else:
                log_error.error(
                    'search_enabled_artifacts_helper <' + hybrid_response['ERROR'] + '>')
        except Exception as e:
            log_error.error(
                'search_enabled_artifacts_helper <Hybrid search/update DB ' + str(e) + '>')
        try:
            otx_response = search_otx_hash(
                artifact_obj.hash_query, artifact_project.otx_api)
            if not 'ERROR' in otx_response:
                log_info.info('Otx:' + artifact_obj.hash_query +
                              ': ' + str(otx_response['otx_exists']))
                update_artifact_otx(artifact_obj.id, otx_response)
            else:
                log_error.error(
                    'search_enabled_artifacts_helper <' + otx_response['ERROR'] + '>')
        except Exception as e:
            log_error.error(
                'search_enabled_artifacts_helper <OTX search/update DB' + str(e) + '>')


def search_project_url_helper(url_id):
    url_obj = Url.objects.get(id=url_id)
    update_url_date_helper(url_id)
    c_project = url_obj.project
    # try:
    #     otx_response = search_otx_url(
    #         url_obj.url_query, c_project.otx_api)
    #     if not 'ERROR' in otx_response:
    #         print('Otx url:' + url_obj.url_query +
    #               ': ' + str(otx_response['otx_exists']))
    #         update_url_otx(url_id, otx_response)
    #     else:
    #         print(otx_response['ERROR'])
    # except Exception as e:
    #     print('Error: OTX search/update DB' + str(e))
    try:
        urlscan_response = search_urlscan_url(
            url_obj.url_query)
        if not 'ERROR' in urlscan_response:
            log_info.info('Urlscan.io url:' + url_obj.url_query +
                          ': ' + str(urlscan_response['urlscan_exists']))
            update_url_urlscan(url_id, urlscan_response)
        else:
            log_error.error('search_project_url_helper <' +
                            urlscan_response['ERROR'] + '>')
    except Exception as e:
        log_error.error(
            'search_project_url_helper <Urlscan.io search/update DB ' + str(e) + '>')


def search_enabled_url_helper(project_id=None):
    if project_id is None:
        url_l = Url.objects.filter(enabled=1).all()
    else:
        url_l = Url.objects.filter(enabled=1).filter(project=project_id).all()
    for url_obj in url_l:
        url_obj = Url.objects.get(id=url_obj.id)
        update_url_date_helper(url_obj.id)
        c_project = url_obj.project
        # try:
        #     otx_response = search_otx_url(
        #         url_obj.url_query, c_project.otx_api)
        #     if not 'ERROR' in otx_response:
        #         print('Otx url:' + url_obj.url_query +
        #               ': ' + str(otx_response['otx_exists']))
        #         update_url_otx(url_obj.id, otx_response)
        #     else:
        #         print(otx_response['ERROR'])
        # except Exception as e:
        #     print('Error: OTX search/update DB' + str(e))
        try:
            urlscan_response = search_urlscan_url(
                url_obj.url_query)
            if not 'ERROR' in urlscan_response:
                log_info.info('Urlscan.io url:' + url_obj.url_query +
                              ': ' + str(urlscan_response['urlscan_exists']))
                update_url_urlscan(url_obj.id, urlscan_response)
            else:
                log_error.error('search_enabled_url_helper <' +
                                urlscan_response['ERROR'] + '>')
        except Exception as e:
            log_error.error(
                'search_enabled_url_helper <Urlscan.io search/update DB ' + str(e) + '>')
