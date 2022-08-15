from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import product

# Create your views here.
def index(request):
    return HttpResponse("Hello world")

def products(request):
    products = product.objects.all()
    context = {'products':products}
    # return HttpResponse(prod)
    return render(request,'myapp/index.html',context)

def product_details(request,id):
    products = product.objects.get(id=id)
    context = { 'product' : products}
    return render (request,'myapp/details.html',context)

def add_product(request):
    if request.method == 'POST' :
        name = request.POST.get('name')
        price = request.POST.get('price')
        desc = request.POST.get('desc')
        image = request.FILES['upload']
        prod = product(name=name,price=price,desc=desc,image=image)
        prod.save()
    return render(request,'myapp/addproduct.html')

def update_product(request,id):
    products = product.objects.get(id=id)
    if request.method == 'POST':

        if request.POST.get('name'):
            products.name = request.POST.get('name')
        if request.POST.get('price'):
            products.price = request.POST.get('price')
        if request.POST.get('desc'):
            products.desc = request.POST.get('desc')
        if request.POST.get('upload'):
            products.image = request.FILES['upload']
        products.save()
        return redirect('/myapp/products')

    context = {'product':products}
    return render(request,'myapp/updateproduct.html',context)

def delete_product(request,id):
    products = product.objects.get(id=id)
    if request.method == 'POST':
        products.delete()
        return redirect('/myapp/products')
    context = {'product':products}
    return render(request,'myapp/delete.html',context)