from django.contrib.auth.hashers import make_password
from django.shortcuts import render, get_object_or_404

# Create your views here.


from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from .models import Customer, Invoice
from .serializers import CustomerSerializer, CategorySerializer, ProductSerializer, InvoiceSerializer
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer

from django.contrib.auth.hashers import make_password


@api_view(['POST'])
def register_customer(request):
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        # Hash the password before saving it in the database
        serializer.save(password=make_password(request.data['password']))
        return Response({"message": "Registration successful"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_customer(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        serializer = CustomerSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def create_category(request):
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_product(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def view_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def view_products_by_category(request, categoryname):
    try:
        category_obj = Category.objects.get(type=categoryname)
        products = Product.objects.filter(category=category_obj)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Category.DoesNotExist:
        return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def view_invoices(request):
    status_param = request.GET.get('status')
    customer_id = request.GET.get('customer')

    if customer_id:
        customer = get_object_or_404(Customer, id=customer_id)
        if status_param:
            invoices = Invoice.objects.filter(customer=customer, status=status_param)
        else:
            invoices = Invoice.objects.filter(customer=customer)
    elif status_param:
        invoices = Invoice.objects.filter(status=status_param)
    else:
        invoices = Invoice.objects.all()

    serializer = InvoiceSerializer(invoices, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_invoice(request):
    serializer = InvoiceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
