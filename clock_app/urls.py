from django.urls import path

from . import views
urlpatterns = [
    path('', views.index),
    path('process_reg', views.process_reg),
    path('process_login', views.process_login),
    path('register', views.render_register),
    path('home', views.render_home),
    path('logout', views.logout),
]
