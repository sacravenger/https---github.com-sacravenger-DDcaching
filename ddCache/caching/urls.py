from django.conf.urls import include, url
from .import views

urlpatterns = [
    url(r'^caching/', views.view_cash.catche_DD, name='get_url'),
    url(r'^outputweb/', views.view_cash.printtoweb, name='outputweb'),
]
