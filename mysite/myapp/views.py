from urllib import request
from django.views.generic import ListView,DetailView,TemplateView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import product
from django.contrib.auth.decorators import login_required
from django.urls import reverse,reverse_lazy
from django.core.paginator import Paginator

from django.http.response import HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
from .models import OrderDetail
import stripe

# Create your views here.
def index(request):
    return HttpResponse("Hello world")

# def products(request):
#     products = product.objects.all()
#     context = {'products':products}
#     # return HttpResponse(prod)
#     return render(request,'myapp/index.html',context)

# Listview - Products
def products(request):

    page_obj = products = product.objects.all()
    
    product_name = request.GET.get('product_name')
    if product_name!='' and product_name is not None:
        page_obj = products.filter(name__icontains=product_name)
    
    paginator = Paginator(page_obj,6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context ={
        'page_obj':page_obj
    }
    return render(request, 'myapp/index.html',context)
class ProductListView(ListView):
    model = product
    context_object_name = 'products'
    template_name = 'myapp/index.html'
    paginate_by = 3

# DetailView - Product
def product_detail(request,id):
    product = product.objects.get(id=id)
    context={
        'product':product
    }
    return render(request,'myapp/detail.html',context)
class ProductDetailView(DetailView):
    model = product
    context_object_name = 'product'
    template_name = 'myapp/details.html'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs) :
        context = super(ProductDetailView,self).get_context_data(**kwargs)
        context['stripe_publishable_key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context

# CreateView - Product
@login_required
def add_product(request):
    if request.method == 'POST' :
        name = request.POST.get('name')
        price = request.POST.get('price')
        desc = request.POST.get('desc')
        image = request.FILES['upload']
        seller_name = request.user
        prod = product(name=name,price=price,desc=desc,image=image,seller_name=seller_name)
        prod.save()
    return render(request,'myapp/addproduct.html')
class ProductCreateView(CreateView):
    model = product
    fields = ['name','price','desc','image','seller_name']
    
# UpdateView - Product
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
class ProductUpdateView(UpdateView):
    model = product
    fields = ['name','price','desc','image','seller_name']
    template_name_suffix = '_update_form'

# DeleteView - product
def delete_product(request,id):
    products = product.objects.get(id=id)
    if request.method == 'POST':
        products.delete()
        return redirect('/myapp/products')
    context = {'product':products}
    return render(request,'myapp/delete.html',context)
class DeleteProductView(DeleteView):
    model = product
    success_url = reverse_lazy('myapp:products')

def my_listings(request):
    products = product.objects.filter(seller_name=request.user)
    context = {'products':products}
    return render(request,'myapp/mylistings.html',context)
    
@csrf_exempt
def create_checkout_session(request,id):
    prod = get_object_or_404(product,pk=id)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session = stripe.checkout.Session.create(
        customer_email = request.user.email,
        
        payment_method_types=['card'],
        line_items=[
            {
                'price_data':{
                    'currency':'usd',
                    'product_data':{
                        'name':prod.name,
                    },
                    'unit_amount':int(prod.price *100),
                },
                'quantity':1,
            }
        ],
        mode='payment',
        success_url = request.build_absolute_uri(reverse('myapp:success'))+"?session_id={CHECKOUT_SESSION_ID}",
        cancel_url= request.build_absolute_uri(reverse('myapp:failed')),
    )
    
    order = OrderDetail()
    order.customer_username = request.user.username
    order.prod = prod
    order.stripe_payment_intent = checkout_session['payment_intent']
    order.checkout_session_id = checkout_session['id']
    order.amount = int(prod.price*100)
    order.save()
    return JsonResponse({'sessionId':checkout_session.id})

class PaymentSuccessView(TemplateView):
    template_name = 'myapp/payment_success.html'
    def get(self, request, *args, **kwargs):
        sessionId = request.GET.get('session_id')         
        if not sessionId:
            return HttpResponseNotFound()        
        session = stripe.checkout.Session.retrieve(sessionId)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        order = get_object_or_404(OrderDetail,checkout_session_id=sessionId) 
        order.has_paid = True
        order.payment_intent = session.payment_intent
        order.save()
        return render(request, self.template_name)
    
class PaymentFailedView(TemplateView):
    template_name = 'myapp/payment_failed.html'
# def fail(request):
#     return render(request,'myapp/payment_failed.html')