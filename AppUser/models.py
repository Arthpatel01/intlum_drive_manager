from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

# type_choices = (
#     ('folder', 'folder'),
#     ('File', 'File'),
# )

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)

