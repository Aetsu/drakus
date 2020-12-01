from django.contrib import admin

from .models import Project, Artifact, Url


class ArtifactInline(admin.StackedInline):
    model = Artifact
    extra = 1

class UrlInline(admin.StackedInline):
    model = Url
    extra = 1

class ProjectAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
        ('Creation Date', {'fields': ['creation_date']}),
        ('VT API key', {'fields': ['vt_api']}),
        ('Hybrid Analysis API key', {'fields': ['hybrid_api']}),
        ('OTX Alienvault',{'fields': ['otx_api']}),
    ]
    inlines = [ArtifactInline, UrlInline]
    list_display = ('name', 'creation_date')
    list_filter = ['creation_date']
    search_fields = ['name']


admin.site.register(Project, ProjectAdmin)
