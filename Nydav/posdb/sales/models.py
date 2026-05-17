# sales/models.py

from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('food',        'អាហារ និងភេសជ្ជៈ'),
        ('electronics', 'អេឡិចត្រូនិក'),
        ('clothing',    'សម្លៀកបំពាក់'),
        ('household',   'គ្រឿងសង្ហារឹម'),
        ('other',       'ផ្សេងៗ'),
    ]

    name      = models.CharField(max_length=200)
    category  = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    price     = models.DecimalField(max_digits=8, decimal_places=2)
    stock     = models.PositiveIntegerField(default=0)
    barcode   = models.CharField(max_length=50, unique=True, blank=True)
    is_active = models.BooleanField(default=True)
    # ✅ កិច្ចការទី៦ — Product Image
    image     = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return f"{self.name}  —  ${self.price}  (ស្តុក: {self.stock})"

    class Meta:
        ordering = ['name']


class Order(models.Model):
    STATUS_CHOICES = [
        ('open',      'បើក'),
        ('completed', 'បានបញ្ចប់'),
        ('cancelled', 'បានលុបចោល'),
    ]

    cashier    = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='orders', null=True)
    status     = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    notes      = models.TextField(blank=True)

    @property
    def total(self):
        return sum(item.subtotal for item in self.items.all())

    def __str__(self):
        return f"ការបញ្ជាទិញ #{self.pk}  [{self.status.upper()}]  —  ${self.total:.2f}"

    class Meta:
        ordering = ['-created_at']


class OrderItem(models.Model):
    order      = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product    = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity   = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)

    @property
    def subtotal(self):
        return self.unit_price * self.quantity

    def __str__(self):
        return f"{self.quantity} × {self.product.name}  @  ${self.unit_price}"