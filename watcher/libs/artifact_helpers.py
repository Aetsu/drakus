from datetime import datetime
from django.utils.timezone import make_aware

from ..models import Artifact
from .project_helpers import get_project_info_helper
import logging

log_info = logging.getLogger('drakus.info')
log_error = logging.getLogger('drakus.error')

def create_artifact_helper(artifact_data):
    try:
        c_project_obj = get_project_info_helper(artifact_data['c_project'])
        a = Artifact(name=artifact_data['name'], hash_query=artifact_data['hash_query'],
                     project=c_project_obj)
        a.save()
    except Exception as e:
        log_error.error("create_artifact_helper <" + str(e) + '>')


def get_artifacts_helper(c_project):
    artifact_l = []
    try:
        artifact_l = Artifact.objects.filter(project=c_project).all()
    except Exception as e:
        log_error.error("get_artifacts_helper <" + str(e) + '>')
    return artifact_l


def update_artifact_date_helper(object_id):
    artifact_obj = Artifact.objects.get(pk=object_id)
    artifact_obj.last_check = make_aware(datetime.now())
    artifact_obj.save()


def delete_artifact_helper(object_id):
    try:
        artifact_obj = Artifact.objects.get(pk=object_id)
        artifact_obj.delete()
    except Exception as e:
        log_error.error("delete_artifact_helper <" + str(e) + '>')
