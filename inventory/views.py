from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *

def add_product(request):
    if request.method == "POST":
        form = ProductsInventoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success_page')  # Change to your success URL
    else:
        form = ProductsInventoryForm()
    
    return render(request, 'add_product.html', {'form': form})

def product_list(request):
    products = ProductsInventory.objects.filter(user=request.user)  # Fetch products for the logged-in user
    return render(request, 'product_list.html', {'products': products})

def delete_inventory(request, product_id):
    product = get_object_or_404(ProductsInventory, id=product_id, user=request.user)
    if request.method == "POST":
        product.delete()
        return redirect('product-list')  # Redirect to the inventory list