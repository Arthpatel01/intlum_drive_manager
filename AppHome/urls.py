from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path

from AppHome import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('download-file/<file_id>', views.DownloadFileView.as_view(), name='download-file'),

]
