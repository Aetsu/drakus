from django.urls import path

from . import views

app_name = 'watcher'
urlpatterns = [
    path('', views.get_projects, name='projects'),
    path('projects', views.get_projects, name='projects'),
    path('create_project', views.create_project, name='create_project'),
    path('edit_project/<int:project_id>', views.edit_project, name='edit_project'),
    path('delete_project/<int:project_id>', views.delete_project, name='delete_project'),
    path('set_project', views.set_project, name='set_project'),
    path('artifacts', views.get_artifacts, name='artifacts'),
    path('delete_artifact/<int:artifact_id>', views.delete_artifact, name='delete_artifact'),
    path('create_artifact', views.create_artifact, name='create_artifact'),
    path('search_artifact', views.search_artifact, name='search_artifact'),
    path('search_all_artifacts', views.search_all_artifacts, name='search_all_artifacts'),
    path('urls', views.get_urls, name='urls'),
    path('delete_url/<int:url_id>', views.delete_url, name='delete_url'),
    path('create_url', views.create_url, name='create_url'),
    path('search_url', views.search_url, name='search_url'),
    path('search_all_urls', views.search_all_urls, name='search_all_urls'),
    path('search', views.search, name='search'),
    path('search_hash', views.search_hash, name='search_hash'),
]
