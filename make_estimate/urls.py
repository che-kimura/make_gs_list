from django.urls import path
from . import views

#app_name = 'make_estimate'
urlpatterns = [
    path('', views.index, name='index'),
    path('estimate_mp', views.estimate_mp, name='estimate_mp')
]