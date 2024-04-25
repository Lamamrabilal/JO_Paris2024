

from django.urls import path

from .views import HomePageView


app_name = "JO_app"

urlpatterns = [
    path('home/', HomePageView.as_view(), name='home'),
]
