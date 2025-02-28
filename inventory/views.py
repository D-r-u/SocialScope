from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *

@login_required
def add_product(request):
    if request.method == "POST":
        form = ProductsInventoryForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)  # Don't save yet
            product.user = request.user  # Assign logged-in user
            product.save()  # Now save with user
            return redirect('product-list')  # Redirect after saving
    else:
        form = ProductsInventoryForm()
    
    return render(request, 'add_product.html', {'form': form})

@login_required
def product_list(request):
    products = ProductsInventory.objects.filter(user=request.user)  # Fetch products for the logged-in user
    return render(request, 'product_list.html', {'products': products})

@login_required
def delete_inventory(request, product_id):
    product = get_object_or_404(ProductsInventory, item_id=product_id, user=request.user)
    if request.method == "POST":
        product.delete()
        return redirect('product-list')  # Redirect to the inventory list
