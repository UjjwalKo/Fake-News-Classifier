from django.urls import path
from . import views

urlpatterns = [
       path('news/', views.index, name='live_news'),
]