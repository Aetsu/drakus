from django.forms import ModelForm
from django import forms
from .models import Project, Artifact, Url

class SearchHashForm(forms.Form):
    hash_query = forms.CharField(
        label='Hash', max_length=300, widget=forms.TextInput(attrs={'class': 'validate'}))


class SearchUrlForm(forms.Form):
    url_query = forms.CharField(
        label='Url', max_length=300, widget=forms.TextInput(attrs={'class': 'validate'}))


class CreateArtifactForm(ModelForm):
    class Meta:
        model = Artifact
        fields = ['name', 'hash_query']


class CreateUrlForm(ModelForm):
    class Meta:
        model = Url
        fields = ['name', 'url_query']


class CreateProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'vt_api', 'hybrid_api', 'otx_api']

class EditProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['id', 'name', 'vt_api', 'hybrid_api', 'otx_api']
