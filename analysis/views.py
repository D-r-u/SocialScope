from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from inventory.models import ProductsInventory
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView
from .models import UserFile
import pandas as pd
import os
from django.conf import settings
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from collections import Counter

# Create your views here.
@login_required
def upload_csv(request, product_id):
    product = get_object_or_404(ProductsInventory, item_id=product_id, user=request.user)
    
    if request.method == "POST" and request.FILES.get("csv_file"):
        file = request.FILES["csv_file"]
        UserFile.objects.create(product=product, uploaded_file=file)
        return redirect("sentiment-analysis", product_id=product.item_id)
    
    return redirect("sentiment-analysis", product_id=product.item_id)

@login_required
def select_keywords(request, product_id):
    product = get_object_or_404(ProductsInventory, item_id=product_id, user=request.user)
    
    if request.method == "POST":
        selected_keywords = request.POST.getlist("keywords")
        custom_keywords = request.POST.get("custom_keywords", "").strip()
        
        if custom_keywords:
            selected_keywords.append(custom_keywords)

        # Store in latest analysis entry
        analysis = UserFile.objects.filter(product=product).last()
        if analysis:
            analysis.keywords = selected_keywords
            analysis.save()

    return redirect("sentiment-analysis", product_id=product.item_id)

@login_required
def sentiment_analysis(request, product_id):
    product = get_object_or_404(ProductsInventory, item_id=product_id, user=request.user)
    previous_analyses = UserFile.objects.filter(product=product).order_by('-timestamp')

    return render(request, "sentiment_analysis.html", {
        "product": product,
        "previous_analyses": previous_analyses
    })

@login_required
def start_analysis(request, product_id):
    product = get_object_or_404(ProductsInventory, item_id=product_id, user=request.user)
    previous_analyses = UserFile.objects.filter(product=product).order_by('-timestamp')

    return render(request, "sentiment_analysis.html", {
        "product": product,
        "previous_analyses": previous_analyses
    })



# Download necessary NLTK resources
nltk.download('vader_lexicon')
nltk.download('stopwords')

# Initialize sentiment analysis and stop words
sia = SentimentIntensityAnalyzer()
stop_words = set(stopwords.words('english'))

def remove_stop_words(text):
    """Removes stop words from the given text."""
    words = text.split()
    filtered_words = [word for word in words if word.lower() not in stop_words]
    return ' '.join(filtered_words)

@login_required
def process_file(request, file_id):
    """Processes the uploaded file for sentiment analysis."""
    try:
        # Get the file uploaded by the user
        file_obj = UserFile.objects.get(id=file_id, user=request.user)
        file_path = file_obj.cleaned_file.path if file_obj.cleaned_file else file_obj.file.path

        try:
            df = pd.read_csv(file_path)  # Read CSV file into a DataFrame
        except pd.errors.ParserError as e:
            return render(request, 'files/error.html', {'error': f"Error reading CSV file: {e}"})

        # Get a list of column names
        column_list = df.columns.tolist()

        if request.method == 'POST':
            selected_columns = request.POST.getlist('columns')  # Get selected columns from user
            if not selected_columns:
                return render(request, 'files/select_columns.html', {'columns': column_list, 'error': "Please select at least one column."})

            # Sentiment analysis variables
            sentiment_results = []
            word_corpus_high = []
            positive_reviews = []
            neutral_reviews = []
            negative_reviews = []

            # Process each row in the selected columns
            for index, row in df.iterrows():
                text = ' '.join(str(row[col]) for col in selected_columns if pd.notna(row[col]))  # Combine text from selected columns
                text = remove_stop_words(text)  # Remove stop words
                sentiment = sia.polarity_scores(text)  # Perform sentiment analysis
                sentiment_results.append({"text": text, "sentiment": sentiment})

                # Categorize the text based on compound sentiment score
                if sentiment['compound'] > 0.5:
                    word_corpus_high.extend(text.split())
                    positive_reviews.append(text)
                elif sentiment['compound'] < -0.5:
                    negative_reviews.append(text)
                else:
                    neutral_reviews.append(text)

            # Limit the number of results to 10
            sentiment_results = sentiment_results[:10]

            # Prepare data for visualization
            texts = [result['text'] for result in sentiment_results]
            positives = [result['sentiment']['pos'] for result in sentiment_results]
            neutrals = [result['sentiment']['neu'] for result in sentiment_results]
            negatives = [result['sentiment']['neg'] for result in sentiment_results]
            compounds = [result['sentiment']['compound'] for result in sentiment_results]

            # Create various charts using Plotly
            # Line Chart
            line_chart = go.Figure()
            line_chart.add_trace(go.Scatter(x=texts, y=compounds, mode='lines+markers', name='Compound', hoverinfo='x+y+text', text=texts))
            line_chart.update_layout(title="Line Chart", xaxis_tickangle=-45)
            line_chart_html = line_chart.to_html(full_html=False)

            # Bar Chart
            bar_chart = go.Figure()
            bar_chart.add_trace(go.Bar(x=texts, y=positives, name='Positive', hoverinfo='x+y+text', text=texts))
            bar_chart.add_trace(go.Bar(x=texts, y=neutrals, name='Neutral', hoverinfo='x+y+text', text=texts))
            bar_chart.add_trace(go.Bar(x=texts, y=negatives, name='Negative', hoverinfo='x+y+text', text=texts))
            bar_chart.update_layout(title="Bar Chart", xaxis_tickangle=-45)
            bar_chart_html = bar_chart.to_html(full_html=False)

            # Pie Chart
            pie_chart = go.Figure()
            pie_chart.add_trace(go.Pie(labels=['Positive', 'Neutral', 'Negative'], values=[sum(positives), sum(neutrals), sum(negatives)], hoverinfo='label+percent+value'))
            pie_chart.update_layout(title="Pie Chart")
            pie_chart_html = pie_chart.to_html(full_html=False)

            # Scatter Plot
            scatter_plot = go.Figure()
            scatter_plot.add_trace(go.Scatter(x=texts, y=compounds, mode='markers', name='Compound', hoverinfo='x+y+text', text=texts))
            scatter_plot.update_layout(title="Scatter Plot", xaxis_tickangle=-45)
            scatter_plot_html = scatter_plot.to_html(full_html=False)

            # Bar chart for most frequent words in positive reviews
            positives_df = pd.DataFrame(Counter(word_corpus_high).most_common(20), columns=['word', 'frequency'])
            positive_words_chart = px.bar(positives_df, x='word', y='frequency', title='Most frequent words in Positive Reviews')
            positive_words_chart_html = positive_words_chart.to_html(full_html=False)

            return render(request, 'files/results.html', {
                'sentiment_results': sentiment_results,
                'line_chart_html': line_chart_html,
                'bar_chart_html': bar_chart_html,
                'pie_chart_html': pie_chart_html,
                'scatter_plot_html': scatter_plot_html,
                'positive_words_chart_html': positive_words_chart_html
            })

        return render(request, 'files/select_columns.html', {'columns': column_list})

    except UserFile.DoesNotExist:
        return redirect('file_list')

def clean_csv(file_path):
    """Cleans the CSV file by removing rows with missing values."""
    df = pd.read_csv(file_path)
    df_cleaned = df.dropna()  # Remove empty rows
    cleaned_file_path = os.path.join(settings.MEDIA_ROOT, 'cleaned', os.path.basename(file_path))
    df_cleaned.to_csv(cleaned_file_path, index=False)  # Save cleaned CSV file
    return cleaned_file_path  # Return cleaned file path
