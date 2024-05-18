from django.contrib import messages
from django.contrib.auth import logout, login
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


from .forms import RegisterForm, LoginForm, ReviewForm
from .models import Category, Product, Rating, Review
from .utils import CartAuthenticatedUser


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

    def get_queryset(self):
        return Product.objects.filter(discount=0)



# shop page
class AllProductList(ProductList):
    template_name = 'shop/all_products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.exclude(discount=0).order_by('-discount')[:3]
        context['sale_products'] = products
        return context


class ByDiscount(AllProductList):
    def get_queryset(self):
        return Product.objects.exclude(discount=0)


# Category dealer
def all_products_by_category(request, category_slug):
    categories = Category.objects.all()
    category = Category.objects.get(slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, 'shop/all_products.html', {'products': products, 'categories': categories, 'title': 'Shop'})


# Product detail page
def detail(request, slug):
    product = Product.objects.get(slug=slug)

    context = {
        'product': product,
        'page_name': 'Shop Detail',
        'categories': Category.objects.all(),
        'products': Product.objects.exclude(discount=0).order_by('-discount')[:6]
    }
    if request.user.is_authenticated:
        rating = Rating.objects.filter(product=product, user=request.user).first()
        context['user_rating'] = rating.rating if rating else 0
        context['reviews'] = Review.objects.filter(product=product)
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


def save_review(request: HttpRequest, product_slug):
    form = ReviewForm(data=request.POST)
    if request.user.is_authenticated:
        if form.is_valid():
            product = Product.objects.get(slug=product_slug)
            review = form.save(commit=False)
            review.product = product
            review.author = request.user
            review.save()
        return redirect('detail', slug=product_slug)
    else:
        return redirect('login')



def cart(request):
    if request.user.is_authenticated:
        cart_info = CartAuthenticatedUser(request).get_cart_info()
        context = {
            'order_products': cart_info['order_products'],
            'cart_total_price': cart_info['cart_total_price'],
            'page_name': 'Cart',
        }
        return render(request, 'shop/cart.html', context)
    else:
        return redirect('login')


def to_cart(request, product_id, action):
    if request.user.is_authenticated:
        CartAuthenticatedUser(request, product_id, action)
        page = request.META.get('HTTP_REFERER')
        return redirect(page)
    else:
        return redirect('login')



def checkout(request):
    if request.user.is_authenticated:
        cart_info = CartAuthenticatedUser(request).get_cart_info()
        context = {
            'order_products': cart_info['order_products'],
            'cart_total_price': cart_info['cart_total_price'],
            'page_name': 'Checkout',
        }
        return render(request, 'shop/checkout.html', context)
    else:
        return redirect('login')





