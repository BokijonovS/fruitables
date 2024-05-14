from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="Kategoriya", unique=True)
    image = models.ImageField(upload_to='category/', null=True, blank=True)
    slug = models.SlugField(blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE,
                               null=True, blank=True,
                               related_name='subcategories')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name="Nomi")
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.FloatField()
    discount = models.IntegerField(default=0)
    image = models.ImageField(upload_to='products/')
    quantity = models.IntegerField(default=0)
    slug = models.SlugField(blank=True, null=True)

    def __str__(self):
        return self.name
    @property
    def final_price(self):
        if self.discount > 0:
            discount_price = self.price * self.discount / 100
            return round(self.price - discount_price, 2)
        else:
            return self.price

    @property
    def avg_rating(self):
        ratings = self.rating_set.all()
        if ratings:
            count = 0
            for rating in ratings:
                count += rating.rating
            return int(count / len(ratings))
        return 0


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.name}: {self.rating}"


class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='User')
    photo = models.ImageField(upload_to='users/', null=True, blank=True)
    phone = models.CharField(max_length=13, verbose_name='Phone number', null=True, blank=True)
    mobile = models.CharField(max_length=13, verbose_name='Mobile', null=True, blank=True)
    email = models.EmailField(max_length=50, verbose_name='Email')
    site = models.URLField(max_length=50, null=True, blank=True)
    job = models.CharField(max_length=50, null=True, blank=True)
    job2 = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)



    def __str__(self):
        return str(self.user.username)

    class Meta:
        verbose_name = 'Custom user'
        verbose_name_plural = 'Custom users'
        ordering = ['-pk']


class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=150, null=True)
    email = models.EmailField(max_length=50, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    rating = models.IntegerField(default=0)



