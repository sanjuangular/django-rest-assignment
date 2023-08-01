# crudapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Existing URLs...
    path('categories/', views.view_categories, name='view_categories'),
    path('category/<str:categoryname>/', views.view_products_by_category, name='view_products_by_category'),
    path('category/', views.create_category, name='create_category'),
    path('product/', views.create_product, name='create_product'),
    path('invoices/', views.view_invoices, name='view_invoices'),
    path('invoice/', views.create_invoice, name='create_invoice'),
]
