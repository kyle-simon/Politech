from django.contrib import admin
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf.urls import url

# Register your models here.
admin.site.site_header = 'PoliTech'
admin.site.site_title = 'PoliTech'
admin.site.site_url = 'http://127.0.0.1:8000/'
admin.site.index_title = 'PoliTech Admin'
admin.empty_value_display = '**Empty**'

# Token authentication
# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)