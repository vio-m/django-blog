from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=False)
    stock = models.PositiveIntegerField(default=0)
    short_description = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)


    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = '/media/placeholder.png'
        return url

    def __str__(self):
        return f"Product: {self.name}, $ {self.price}"

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'pk': self.pk})


class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=None, related_name='images')
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media', blank=True, null=True)
    default = models.BooleanField(default=False) # default so that an image has to be shown among all the available images for a product

    def __str__(self):
        return f"Image: {self.name}"

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = '/media/placeholder.png'
        return url


class Rating(models.Model):
    RATING_RANGE = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5)
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='rates', null=True)
    rating = models.PositiveSmallIntegerField(choices=RATING_RANGE, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    date = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self):
        return f'{self.rating}'


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_total_discounted(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total_discounted for item in orderitems])
        return total

    @property
    def get_saved(self):
        saved = self.get_cart_total - self.get_cart_total_discounted
        return saved

    @property
    def get_discount(self):
        orderitems = self.orderitem_set.all()
        try:
            discount = max([item.get_discount for item in orderitems])
        except Exception:
            discount = 0
        return discount

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    def __str__(self):
        return f"Order: {self.id}"


class Coupon(models.Model):
    code = models.CharField(max_length=10, unique=True)
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    active = models.BooleanField()

    def __str__(self):
        return self.code


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

    @property
    def get_discount(self):
        try:
            discount = self.coupon.discount
        except Exception:
            discount = 0
        return discount

    @property
    def get_total_discounted(self):
        try:
            discount = self.coupon.discount
        except Exception:
            discount = 0
        total_discounted = (self.product.price - (self.product.price * (discount / 100))) * self.quantity
        return total_discounted

    def __str__(self):
        return f"OrderItem: {self.id}"


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Shipping Address: {self.address}"








