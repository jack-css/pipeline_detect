from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("work", views.first_page, name="page1"),
    path("d", views.digital_map, name="map"),
    path("upload", views.upload_data, name="upload"),
    path('upload/load', views.download_excel, name="load"),
    path('login', views.login, name="login"),
    # path("", views.index_first, name='first_index')
]
