from django.urls import path
from . import views

# app_name = 'make_gs_list'

urlpatterns = [
    path('', views.index, name='index'),
    path('download', views.download, name='download'),
    path('nofind', views.nofind, name='nofind'),
]