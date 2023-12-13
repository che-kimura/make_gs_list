from django.urls import path
from . import views

#app_name = 'make_estimate'
urlpatterns = [
    path('', views.index, name='index')
]