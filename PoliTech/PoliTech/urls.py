"""
Definition of urls for PoliTech.
"""

from django.conf.urls import include, url
from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from api import views as user_views
from rest_framework.authtoken import views
from rest_framework import routers
from rest_framework.schemas import get_schema_view


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

schema_view = get_schema_view(title='PoliAPI')

router = routers.DefaultRouter(trailing_slash=False)

router.register(r'economic-data', user_views.EconomicViewSet)
router.register(r'vote-count', user_views.VoteCountViewSet)
router.register(r'adjacency', user_views.AdjacencyViewSet)
router.register(r'adjacency-type', user_views.AdjacencyTypeViewSet)
router.register(r'district', user_views.DistrictViewSet)
router.register(r'precinct', user_views.PrecinctViewSet)

urlpatterns = router.urls

urlpatterns += [
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', admin.site.urls),
    url(r'^api-token-auth/', views.obtain_auth_token),
    path('schema/', schema_view)

]

