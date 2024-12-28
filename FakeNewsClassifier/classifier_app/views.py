import joblib
import pandas as pd
import re
import string
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

load_vector = joblib.load(open('embeddings/vect.joblib', 'rb'))
load_model = joblib.load(open('embeddings/DTC.joblib', 'rb'))

def regularExp(text):
    text = text.lower()
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(f'[{re.escape(string.punctuation)}]', '', text)
    text = re.sub(r'\n', '', text)
    text = re.sub(r'\w*\d\w*', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def output_label(n):
    if n == 0:
        return "Fake News"
    elif n == 1:
        return "Not A Fake News"

@login_required
def classify_news(request):
    result = ""
    confidence_score = 0
    if request.method == 'POST':
        news = request.POST.get('news')
        if news:
            testing_news = {"text": [news]}
            new_def_test = pd.DataFrame(testing_news)
            new_def_test["text"] = new_def_test["text"].apply(regularExp)
            new_x_test = new_def_test["text"]
            new_xv_test = load_vector.transform(new_x_test)
            prediction = load_model.predict(new_xv_test)
            probabilities = load_model.predict_proba(new_xv_test)
            confidence_score = max(probabilities[0]) * 100
            result = output_label(prediction[0])
    return render(request, 'classifier/index.html', {'result': result, 'confidence_score': confidence_score})