from django.shortcuts import render, redirect
from .forms import ProductsInventoryForm

def add_product(request):
    if request.method == "POST":
        form = ProductsInventoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success_page')  # Change to your success URL
    else:
        form = ProductsInventoryForm()
    
    return render(request, 'add_product.html', {'form': form})
