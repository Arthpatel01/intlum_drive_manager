from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from AppUser.models import CustomUser


class File(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    link = models.CharField(max_length=50, blank=True, null=True)
    extension = models.CharField(max_length=50, blank=True, null=True)
    document = models.FileField(upload_to="files", null=True)
    doc_name = models.CharField(max_length=100, null=True)
    parent = models.ForeignKey('Folder', on_delete=models.CASCADE, related_name="files", blank=True, null=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=timezone.now, null=True, blank=True)
    is_del = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Folder(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="folders")
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=timezone.now, null=True, blank=True)
    is_del = models.BooleanField(default=False)


    def __str__(self):
        return self.name
