from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Product

@csrf_exempt
def product_list(request):
    if request.method == 'GET':
        # Read All: List every product (sirf useful details)
        products = list(Product.objects.values('id', 'name', 'sku', 'stock'))
        return JsonResponse({'products': products})

    elif request.method == 'POST':
        # Create: Add a new product
        data = json.loads(request.body)
        product = Product.objects.create(
            name=data['name'],
            sku=data['sku'],
            stock=data.get('stock', 0),
            price=data['price']
        )
        return JsonResponse({'id': product.id, 'message': 'Product created successfully'}, status=201)

@csrf_exempt
def product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)

    if request.method == 'GET':
        # Read One: See one product by ID, full details
        data = {
            'id': product.id,
            'name': product.name,
            'sku': product.sku,
            'stock': product.stock,
            'price': str(product.price)
        }
        return JsonResponse(data)

    elif request.method == 'PUT':
        # Update: Change a product
        data = json.loads(request.body)
        product.name = data.get('name', product.name)
        product.sku = data.get('sku', product.sku)
        product.stock = data.get('stock', product.stock)
        product.price = data.get('price', product.price)
        product.save()
        return JsonResponse({'message': 'Product updated successfully'})

    elif request.method == 'DELETE':
        # Delete: Remove a product
        product.delete()
        return JsonResponse({'message': 'Product deleted successfully'})

@csrf_exempt
def low_stock_list(request):
    if request.method == 'GET':
    
        low_stock_products = list(Product.objects.filter(stock__lt=10).values('id', 'name', 'stock'))
        return JsonResponse({'low_stock': low_stock_products})


def product_list_html(request):
    products = Product.objects.all()
    return render(request, 'inventory/product_list.html', {'products': products})

@csrf_exempt
def product_list(request):
    if request.method == 'GET':
        # Check karein agar URL mein '?category=' likha hai
        category_query = request.GET.get('category')
        
        if category_query:
            # Sirf wahi products layein jo search ki hui category se match karein
            products = list(Product.objects.filter(category__name__icontains=category_query).values('id', 'name', 'sku', 'stock', 'category__name', 'supplier__name'))
        else:
            # Agar koi filter nahi hai, toh sab kuch layein
            products = list(Product.objects.values('id', 'name', 'sku', 'stock', 'category__name', 'supplier__name'))
            
        return JsonResponse({'products': products})

    elif request.method == 'POST':
        # Create: Add a new product
        data = json.loads(request.body)
        product = Product.objects.create(
            name=data['name'],
            sku=data['sku'],
            stock=data.get('stock', 0),
            price=data['price'],
            category_id=data.get('category_id'),
            supplier_id=data.get('supplier_id')
        )
        return JsonResponse({'id': product.id, 'message': 'Product created successfully'}, status=201)

def product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)

    if request.method == 'GET':
        data = {
            'id': product.id,
            'name': product.name,
            'sku': product.sku,
            'stock': product.stock,
            'price': str(product.price),
            # Nayi lines:
            'category': product.category.name if product.category else 'No Category',
            'supplier': product.supplier.name if product.supplier else 'No Supplier'
        }
        return JsonResponse(data)

   