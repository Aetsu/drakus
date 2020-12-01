from ..models import Project, Artifact, Url
from django.db.models import Q
import logging

log_info = logging.getLogger('drakus.info')
log_error = logging.getLogger('drakus.error')

def create_project_helper(project_data):
    try:
        p = Project(name=project_data['name'], vt_api=project_data['vt_api'],
                    hybrid_api=project_data['hybrid_api'], otx_api=project_data['otx_api'])
        p.save()
    except Exception as e:
        log_error.error('create_project_helper <' + str(e) + '>')


def delete_project_helper(project_id):
    try:
        p = Project.objects.get(pk=project_id)
        p.delete()
    except Exception as e:
        log_error.error("delete_project_helper <" + str(e) + '>')


def get_project_info_helper(project_id):
    r = None
    try:
        p = Project.objects.get(pk=project_id)
    except Exception as e:
        log_error.error('get_project_info_helper <' + str(e) + '>')
    return p


def get_projects_helper():
    project_q = Project.objects.all()
    project_l = []
    for p in project_q:
        d_aux = {}
        d_aux['id'] = p.id
        d_aux['name'] = p.name
        d_aux['creation_date'] = p.creation_date
        d_aux['artifacts'] = Artifact.objects.filter(project=p.id).count()
        artifact_l = Artifact.objects.filter(
            Q(project=p.id), (Q(vt_exists=1) | Q(hybrid_exists=1) | Q(otx_exists=1)))
        d_aux['identified_artifacts'] = len(artifact_l)
        d_aux['urls'] = Url.objects.filter(project=p.id).count()
        url_l = Url.objects.filter(
            Q(project=p.id), (Q(urlscan_exists=1)))
        d_aux['identified_urls'] = len(url_l)
        project_l.append(d_aux)
    return project_l
