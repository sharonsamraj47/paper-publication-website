# accounts/admin.py

from django.contrib import admin
from .models import UserProfile, UploadedFile

admin.site.register(UserProfile)
admin.site.register(UploadedFile)
