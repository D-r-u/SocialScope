from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from inventory.models import ProductsInventory

# Create your views here.
@login_required
def upload_csv(request, product_id):
    product = get_object_or_404(ProductsInventory, item_id=product_id, user=request.user)
    
    if request.method == "POST" and request.FILES.get("csv_file"):
        file = request.FILES["csv_file"]
        SentimentAnalysis.objects.create(product=product, uploaded_file=file)
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
        analysis = SentimentAnalysis.objects.filter(product=product).last()
        if analysis:
            analysis.keywords = selected_keywords
            analysis.save()

    return redirect("sentiment-analysis", product_id=product.item_id)

@login_required
def sentiment_analysis(request, product_id):
    product = get_object_or_404(ProductsInventory, item_id=product_id, user=request.user)
    previous_analyses = SentimentAnalysis.objects.filter(product=product).order_by('-timestamp')

    return render(request, "sentiment_analysis.html", {
        "product": product,
        "previous_analyses": previous_analyses
    })

@login_required
def start_analysis(request, product_id):
    product = get_object_or_404(ProductsInventory, item_id=product_id, user=request.user)
    previous_analyses = SentimentAnalysis.objects.filter(product=product).order_by('-timestamp')

    return render(request, "sentiment_analysis.html", {
        "product": product,
        "previous_analyses": previous_analyses
    })