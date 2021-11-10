from django.urls import path, include

urlpatterns = [
    path('', include('clock_app.urls')),
]
