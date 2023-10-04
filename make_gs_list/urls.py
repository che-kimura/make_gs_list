from django.urls import path
from . import views

# app_name = 'make_gs_list'

urlpatterns = [
    path('', views.index, name='index'),
    path('download', views.download, name='download'),
    path('nofind', views.nofind, name='nofind'),
    # 以下を追記(views.pyのtest()にデータを送信できるようにする)
    path("ajax/", views.test, name="test"),
    path("test_page", views.test_page, name='test_page'),
]