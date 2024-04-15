

from django.urls import path

from .views import HomeView


app_name = "JO_app"

urlpatterns = [
    path('home/',HomeView, name='home'),
]
