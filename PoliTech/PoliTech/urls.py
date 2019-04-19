"""
Definition of urls for PoliTech.
"""

from django.conf.urls import include, url
from rest_framework.authtoken import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', PoliTech.views.home, name='home'),
    # url(r'^PoliTech/', include('PoliTech.PoliTech.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', admin.site.urls),
    #url(r'^api-token-auth/', views.obtain_auth_token)
]
