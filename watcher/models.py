from django.db import models
from django.utils import timezone


class Project(models.Model):
    name = models.CharField(max_length=100)
    creation_date = models.DateTimeField(default=timezone.now)
    vt_api = models.CharField(max_length=200, null=True)
    hybrid_api = models.CharField(max_length=200, null=True)
    otx_api = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Artifact(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    hash_query = models.CharField(max_length=64, null=True)
    hash_md5 = models.CharField(max_length=32, blank=True, null=True)
    hash_sha1 = models.CharField(max_length=40, blank=True, null=True)
    hash_sha256 = models.CharField(max_length=64, blank=True, null=True)
    vt_exists = models.IntegerField(blank=True, default=0)
    vt_link = models.CharField(max_length=300, blank=True, null=True)
    hybrid_exists = models.IntegerField(blank=True, default=0)
    hybrid_link = models.CharField(max_length=300, blank=True, null=True)
    otx_exists = models.IntegerField(blank=True, default=0)
    otx_link = models.CharField(max_length=300, blank=True, null=True)
    last_check = models.DateTimeField(default=timezone.now)
    enabled = models.IntegerField(blank=True, default=1)

    def __str__(self):
        return self.name

class Url(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    url_query = models.CharField(max_length=300, null=True)
    urlscan_exists = models.IntegerField(blank=True, default=0)
    urlscan_link = models.CharField(max_length=300, blank=True, null=True)
    # otx_exists = models.IntegerField(blank=True, default=0)
    # otx_link = models.CharField(max_length=300, blank=True, null=True)
    last_check = models.DateTimeField(default=timezone.now)
    enabled = models.IntegerField(blank=True, default=1)

    def __str__(self):
        return self.name

class Config(models.Model):
    name = models.CharField(max_length=100)
    value = models.IntegerField(default=180)

    def __str__(self):
        return self.name