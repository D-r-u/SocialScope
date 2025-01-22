from django.urls import path
from . import views

# URLconf of brand
urlpatterns = [
    path('home', views.hello)
]