from django.urls import path
from . import views

urlpatterns = [
    path('', views.news_home, name='news_home'),
    path('category/<str:category>/', views.news_category, name='news_category'),
    path('search/', views.news_search, name='news_search'),
    path('live-news/', views.live_news, name='live_news'),
]