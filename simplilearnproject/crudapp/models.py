from django.db import models


class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    password = models.CharField(max_length=128)  # Store hashed passwords
    last_login = models.DateTimeField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Category(models.Model):
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.type


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    condition = models.CharField(max_length=100)
    noofdays = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    color = models.CharField(max_length=100)
    size = models.CharField(max_length=100)
    imageurl = models.URLField()
    rentaloptions = models.JSONField()

    def __str__(self):
        return self.name


class Invoice(models.Model):
    STATUS_CHOICES = (
        ('ORDERED', 'Ordered'),
        ('CANCELLED', 'Cancelled'),
        ('DELIVERED', 'Delivered'),
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    items = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ORDERED')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice #{self.id}"
