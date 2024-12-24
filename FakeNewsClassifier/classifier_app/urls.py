from django.urls import path
from . import views

urlpatterns = [
       path('home/', views.classify_news, name='classify_news'),
]