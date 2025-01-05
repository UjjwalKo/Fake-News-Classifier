import requests
from django.shortcuts import render
from django.conf import settings
from django.core.paginator import Paginator
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from .models import Article

# Use a model optimized for English
model = SentenceTransformer('all-MiniLM-L6-v2')

def fetch_news(endpoint, params):
    api_key = settings.NEWS_API_KEY
    base_url = 'https://newsapi.org/v2/'
    
    params['apiKey'] = api_key
    response = requests.get(base_url + endpoint, params=params)
    return response.json()

def store_articles(articles):
    for article in articles:
        title = article.get('title', '')
        description = article.get('description', '')
        if not title and not description:
            continue

        text_for_embedding = title + ' ' + description
        try:
            embedding = model.encode([text_for_embedding])[0].tolist()
        except Exception as e:
            print(f"Error generating embedding: {e}")
            continue

        Article.objects.create(
            title=title,
            description=description,
            url=article.get('url', ''),
            url_to_image=article.get('urlToImage'),
            published_at=article.get('publishedAt'),
            source_name=article.get('source', {}).get('name', ''),
            embedding=embedding
        )

def semantic_search(query, top_k=100):
    try:
        query_embedding = model.encode([query])[0]
        articles = list(Article.objects.all())
        
        if not articles:
            return []
        
        embeddings = np.array([article.embedding for article in articles])
        
        if embeddings.size == 0:
            return []
        
        similarities = cosine_similarity([query_embedding], embeddings)[0]
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        # Filter results with similarity scores
        min_similarity_threshold = 0.3
        results = []
        for idx in top_indices:
            if similarities[idx] >= min_similarity_threshold:
                results.append((articles[int(idx)], similarities[idx]))
        
        return results
    except Exception as e:
        print(f"Error in semantic search: {e}")
        return []

def news_search(request):
    query = request.GET.get('q', '')
    if query:
        search_results = semantic_search(query)
        articles = [article for article, _ in sorted(search_results, key=lambda x: x[1], reverse=True)]
    else:
        articles = []
    
    paginator = Paginator(articles, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'news/search.html', {
        'page_obj': page_obj, 
        'query': query,
    })

def news_home(request):
    news_data = fetch_news('top-headlines', {'country': 'us', 'pageSize': 100})
    articles = news_data.get('articles', [])
    
    try:
        store_articles(articles)
    except Exception as e:
        print(f"Error storing articles: {e}")
    
    paginator = Paginator(articles, 12)  # Show 12 articles per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'news/home.html', {'page_obj': page_obj})

def news_category(request, category):
    news_data = fetch_news('top-headlines', {'country': 'us', 'category': category, 'pageSize': 100})
    articles = news_data.get('articles', [])
    
    try:
        store_articles(articles)
    except Exception as e:
        print(f"Error storing articles: {e}")
    
    paginator = Paginator(articles, 12)  # Show 12 articles per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'news/category.html', {'page_obj': page_obj, 'category': category})

def live_news(request):
    news_data = fetch_news('top-headlines', {'country': 'us', 'pageSize': 20})
    articles = news_data.get('articles', [])
    
    try:
        store_articles(articles)
    except Exception as e:
        print(f"Error storing articles: {e}")
    
    return render(request, 'news/live_news.html', {'articles': articles})