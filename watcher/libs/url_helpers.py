from django.utils.timezone import make_aware
from datetime import datetime

from ..models import Url
from .project_helpers import get_project_info_helper
import logging

log_info = logging.getLogger('drakus.info')
log_error = logging.getLogger('drakus.error')


def create_url_helper(url_data):
    try:
        c_project_obj = get_project_info_helper(url_data['c_project'])
        a = Url(name=url_data['name'], url_query=url_data['url_query'],
                project=c_project_obj)
        a.save()
    except Exception as e:
        log_error.error("create_url_helper <" + str(e) + '>')


def get_urls_helper(c_project):
    url_l = []
    try:
        url_l = Url.objects.filter(project=c_project).all()
    except Exception as e:
        log_error.error("get_urls_helper <" + str(e) +'>')
    return url_l


def update_url_date_helper(object_id):
    url_obj = Url.objects.get(pk=object_id)
    url_obj.last_check = make_aware(datetime.now())
    url_obj.save()


def delete_url_helper(object_id):
    try:
        url_obj = Url.objects.get(pk=object_id)
        url_obj.delete()
    except Exception as e:
        log_error.error("delete_url_helper <" + str(e) +'>')
