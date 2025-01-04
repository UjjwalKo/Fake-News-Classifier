import requests
from django.shortcuts import render
from django.conf import settings
from django.core.paginator import Paginator
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from langdetect import detect 
from .models import Article

model = SentenceTransformer('distiluse-base-multilingual-cased-v1')

def fetch_news(endpoint, params):
    api_key = settings.NEWS_API_KEY
    base_url = 'https://newsapi.org/v2/'
    
    params['apiKey'] = api_key
    response = requests.get(base_url + endpoint, params=params)
    return response.json()

def store_articles(articles):
    for article in articles:
        try:
            language = detect(article['title'] + ' ' + article['description'])
        except:
            language = 'en'

        embedding = model.encode([article['title'] + ' ' + article['description']])[0].tolist()

        Article.objects.create(
            title=article['title'],
            description=article['description'],
            url=article['url'],
            url_to_image=article.get('urlToImage'),
            published_at=article['publishedAt'],
            source_name=article['source']['name'],
            embedding=embedding,
            language=language
        )

def news_home(request):
    news_data = fetch_news('top-headlines', {'country': 'us', 'pageSize': 100})
    articles = news_data.get('articles', [])
    
    store_articles(articles)
    
    paginator = Paginator(articles, 12)  # Show 12 articles per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'news/home.html', {'page_obj': page_obj})

def news_category(request, category):
    news_data = fetch_news('top-headlines', {'country': 'us', 'category': category, 'pageSize': 100})
    articles = news_data.get('articles', [])
    
    store_articles(articles)
    
    paginator = Paginator(articles, 12)  # Show 12 articles per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'news/category.html', {'page_obj': page_obj, 'category': category})

def semantic_search(query, language, top_k=100):
    query_embedding = model.encode([query])[0]
    articles = Article.objects.filter(language=language)
    embeddings = np.array([article.embedding for article in articles])
    
    similarities = cosine_similarity([query_embedding], embeddings)[0]
    top_indices = np.argsort(similarities)[::-1][:top_k]
    
    return [articles[i] for i in top_indices]

def news_search(request):
    query = request.GET.get('q', '')
    if query:
        try:
            language = detect(query)
        except:
            language = 'en'
        
        articles = semantic_search(query, language)
    else:
        articles = []
    
    paginator = Paginator(articles, 12)  # Show 12 articles per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'news/search.html', {'page_obj': page_obj, 'query': query})

def live_news(request):
    news_data = fetch_news('top-headlines', {'country': 'us', 'pageSize': 20})
    articles = news_data.get('articles', [])
    store_articles(articles)
    return render(request, 'news/live_news.html', {'articles': articles})