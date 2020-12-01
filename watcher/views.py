from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import SearchHashForm, SearchUrlForm, CreateArtifactForm, CreateProjectForm, EditProjectForm, CreateUrlForm
from .libs.project_helpers import create_project_helper, get_projects_helper, get_project_info_helper, delete_project_helper
from .libs.search_helpers import search_artifact_helper, search_project_artifact_helper, search_project_url_helper, search_enabled_artifacts_helper, search_enabled_url_helper
from .libs.artifact_helpers import create_artifact_helper, get_artifacts_helper, delete_artifact_helper
from .libs.url_helpers import get_urls_helper, create_url_helper, delete_url_helper
import logging

log_info = logging.getLogger('drakus.info')
log_error = logging.getLogger('drakus.error')

# projects
@login_required
def create_project(request, *args, **kwargs):
    if request.method == 'POST':
        form = CreateProjectForm(request.POST)
        if form.is_valid():
            project_data = {
                'name': form.cleaned_data['name'],
                'vt_api': form.cleaned_data['vt_api'],
                'hybrid_api': form.cleaned_data['hybrid_api'],
                'otx_api': form.cleaned_data['otx_api']
            }
            create_project_helper(project_data)
        return HttpResponseRedirect('/watcher/projects')
    else:
        createProjectForm = CreateProjectForm()
        return render(request, 'watcher/create_project.html', {'createProjectForm': createProjectForm})

@login_required
def edit_project(request,  project_id):
    p = get_project_info_helper(project_id)
    if request.method == 'POST':
        form = EditProjectForm(request.POST, instance=p)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/watcher/projects')
    else:
        # p = get_project_info_helper(project_id)
        editProjectForm = EditProjectForm(instance=p)
        return render(request, 'watcher/edit_project.html', {'editProjectForm': editProjectForm})

@login_required
def delete_project(request,  *args, **kwargs):
    if request.method == 'GET':
        p_id = kwargs['project_id']
        delete_project_helper(p_id)
        return HttpResponseRedirect('/watcher/projects')

@login_required
def get_projects(request):
    project_l = get_projects_helper()
    context = {'project_l': project_l}
    return render(request, 'watcher/project_list.html', context)

@login_required
def set_project(request, *args, **kwargs):
    if request.method == 'POST':
        project_id = request.POST.get('project_id', None)
        response = HttpResponseRedirect('/watcher/artifacts')
        response.set_cookie('current_project', int(project_id))
        return response
    return HttpResponseRedirect('/watcher/projects')


# artifacts
@login_required
def get_artifacts(request):
    if not 'current_project' in request.COOKIES:
        c_project = 0
    else:
        c_project = request.COOKIES['current_project']
    try:
        artifact_l = get_artifacts_helper(c_project)
        context = {'artifact_l': artifact_l}
        return render(request, 'watcher/artifact_list.html', context)
    except Exception as e:
        print(e)
        return HttpResponseRedirect('/watcher/')

@login_required
def create_artifact(request, *args, **kwargs):
    if not 'current_project' in request.COOKIES or request.COOKIES['current_project'] == 0:
        return HttpResponseRedirect('/watcher/')
    if request.method == 'POST':
        form = CreateArtifactForm(request.POST)
        if form.is_valid():
            artifact_data = {
                'name': form.cleaned_data['name'],
                'hash_query': form.cleaned_data['hash_query'],
                'c_project': request.COOKIES['current_project']
            }
            create_artifact_helper(artifact_data)
            return HttpResponseRedirect('/watcher/artifacts')
    else:
        createArtifact = CreateArtifactForm()
        return render(request, 'watcher/create_artifact.html', {'createArtifact': createArtifact})

@login_required
def delete_artifact(request,  *args, **kwargs):
    if request.method == 'GET':
        a_id = kwargs['artifact_id']
        delete_artifact_helper(a_id)
        return HttpResponseRedirect('/watcher/artifacts')

@login_required
def search(request):
    if not 'current_project' in request.COOKIES or request.COOKIES['current_project'] == 0:
        return HttpResponseRedirect('/watcher/')
    hash_form = SearchHashForm()
    url_form = SearchUrlForm()
    return render(request, 'watcher/search_form.html', {'hash_form': hash_form, 'url_form': url_form})

@login_required
def search_hash(request):
    if not 'current_project' in request.COOKIES or request.COOKIES['current_project'] == 0:
        return HttpResponseRedirect('/watcher/')
    if request.method == 'POST':
        form = SearchHashForm(request.POST)
        if form.is_valid():
            hash_query = form.cleaned_data['hash_query']
            d_search = search_artifact_helper(
                hash_query, request.COOKIES['current_project'])
            context = {
                'hash_query': hash_query,
                'artefact_vt_info': d_search['artefact_vt_info'],
                'artefact_hybrid_info': d_search['artefact_hybrid_info'],
                'artefact_otx_info': d_search['artefact_otx_info']
            }
            return render(request, 'watcher/hash_info.html', context)
    else:
        return HttpResponseRedirect('/watcher/search')

@login_required
def search_artifact(request, *args, **kwargs):
    artifact_id = request.POST.get('artifact_id', None)
    search_project_artifact_helper(artifact_id)
    return HttpResponseRedirect('/watcher/artifacts')

@login_required
def search_all_artifacts(request):
    if not 'current_project' in request.COOKIES or request.COOKIES['current_project'] == 0:
        return HttpResponseRedirect('/watcher/')
    search_enabled_artifacts_helper(request.COOKIES['current_project'])
    return HttpResponseRedirect('/watcher/artifacts')


# urls
@login_required
def get_urls(request):
    if not 'current_project' in request.COOKIES:
        c_project = 0
    else:
        c_project = request.COOKIES['current_project']
    try:
        url_l = get_urls_helper(c_project)
        context = {'url_l': url_l}
        return render(request, 'watcher/url_list.html', context)
    except Exception as e:
        log_error.error('get_urls <' + str(e) + '>')
        return HttpResponseRedirect('/watcher/')

@login_required
def create_url(request, *args, **kwargs):
    if not 'current_project' in request.COOKIES or request.COOKIES['current_project'] == 0:
        return HttpResponseRedirect('/watcher/')
    if request.method == 'POST':
        form = CreateUrlForm(request.POST)
        if form.is_valid():
            url_data = {
                'name': form.cleaned_data['name'],
                'url_query': form.cleaned_data['url_query'],
                'c_project': request.COOKIES['current_project']
            }
            create_url_helper(url_data)
            return HttpResponseRedirect('/watcher/urls')
    else:
        createUrl = CreateUrlForm()
        return render(request, 'watcher/create_url.html', {'createUrl': createUrl})

@login_required
def delete_url(request,  *args, **kwargs):
    if request.method == 'GET':
        u_id = kwargs['url_id']
        delete_url_helper(u_id)
        return HttpResponseRedirect('/watcher/urls')

@login_required
def search_url(request, *args, **kwargs):
    url_id = request.POST.get('url_id', None)
    search_project_url_helper(url_id)
    return HttpResponseRedirect('/watcher/urls')

@login_required
def search_all_urls(request):
    if not 'current_project' in request.COOKIES or request.COOKIES['current_project'] == 0:
        return HttpResponseRedirect('/watcher/')
    search_enabled_url_helper(request.COOKIES['current_project'])
    return HttpResponseRedirect('/watcher/urls')
