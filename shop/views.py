from django.contrib import messages
from django.contrib.auth import logout, login
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import RegisterForm, LoginForm
from .models import Category, Product, Rating


# Create your views here.




# index page all products getter
class ProductList(ListView):
    model = Product
    template_name = 'shop/index.html'
    context_object_name = 'products'
    extra_context = {
        'categories': Category.objects.filter(parent=None),
        'page_name': "Shop"
    }



# shop page
class AllProductList(ProductList):
    template_name = 'shop/all_products.html'


# Category dealer
def all_products_by_category(request, category_slug):
    categories = Category.objects.all()
    category = Category.objects.get(slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, 'shop/all_products.html', {'products': products, 'categories': categories, 'title': 'Shop'})


# Product detail page
def detail(request, slug):
    product = Product.objects.get(slug=slug)
    rating = Rating.objects.filter(product=product, user=request.user).first()
    product.user_rating = rating.rating if rating else 0

    context = {
        'product': product,
        'page_name': 'Shop Detail',
        'categories': Category.objects.all(),
    }
    return render(request, 'shop/product_detail.html', context=context)



# rating with stars section
def rate(request: HttpRequest, product_id: int, rating: int) -> HttpResponse:
    product = Product.objects.get(id=product_id)
    Rating.objects.filter(product=product, user=request.user).delete()
    product.rating_set.create(user=request.user, rating=rating)
    return detail(request, product.slug)


# user login
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
        if form.errors:
            for error in form.error_messages.values():
                messages.error(request, f'{error}')

    form = LoginForm()
    return render(request, 'shop/login.html', {'form': form})


# user logout

def user_logout(request):
    logout(request)
    return redirect('login')


# user creator
def user_register(request):
    form = RegisterForm(data=request.POST)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('index')

    form = RegisterForm()
    context = {
        'form': form,
        'title': 'Register'
    }
    return render(request, 'shop/register.html', context)






