
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.authtoken.models import Token
from .models import Product


def get_user_from_request(request):

    auth_header = request.headers.get('Authorization')

    if auth_header and auth_header.startswith('Token '):
        token_key = auth_header.split(' ')[1]

        try:
            return Token.objects.get(key=token_key).user
        except Token.DoesNotExist:
            return None

    return None


@csrf_exempt
def product_list(request):
    if request.method == 'GET':
        category_query = request.GET.get('category')
        # Bonus: Creator filter capture karein
        creator_query = request.GET.get('creator')
        
        queryset = Product.objects.all()
        
        if category_query:
            queryset = queryset.filter(category__name__icontains=category_query)
        if creator_query:
            # Bonus: Creator ke username se filter karein
            queryset = queryset.filter(created_by__username__icontains=creator_query)
            
        # Bonus: 'created_by__username' ko list mein add kiya
        products = list(queryset.values(
            'id', 'name', 'sku', 'stock', 'category__name', 'supplier__name', 'created_by__username'
        ))
            
        return JsonResponse({'products': products})

    elif request.method == 'POST':
        user = get_user_from_request(request)
        if not user:
            return JsonResponse({'error': '401 Unauthorized'}, status=401)
        if not user.has_perm('inventory.add_product'):
            return JsonResponse({'error': '403 Forbidden'}, status=403)

        data = json.loads(request.body)
        product = Product.objects.create(
            name=data['name'],
            sku=data['sku'],
            stock=data.get('stock', 0),
            price=data['price'],
            category_id=data.get('category_id'),
            supplier_id=data.get('supplier_id'),
            created_by=user
        )
        return JsonResponse({'message': 'Product created successfully', 'id': product.id}, status=201)
@csrf_exempt
def product_detail(request, pk):

    try:
        product = Product.objects.get(pk=pk)

    except Product.DoesNotExist:
        return JsonResponse(
            {'error': 'Product not found'},
            status=404
        )
    if request.method == 'GET':

        data = {
            'id': product.id,
            'name': product.name,
            'sku': product.sku,
            'stock': product.stock,
            'price': str(product.price),
            'category': (
                product.category.name
                if product.category
                else 'No Category'
            ),
            'supplier': (
                product.supplier.name
                if product.supplier
                else 'No Supplier'
            ),
            'created_by': (
                product.created_by.username
                if product.created_by
                else 'Unknown'
            )
        }

        return JsonResponse(data)

    # PUT - Login + change permission required
    elif request.method == 'PUT':

        user = get_user_from_request(request)

        if not user:
            return JsonResponse(
                {'error': '401 Unauthorized'},
                status=401
            )

        if not user.has_perm('inventory.change_product'):
            return JsonResponse(
                {'error': '403 Forbidden: Cannot update'},
                status=403
            )

        try:
            data = json.loads(request.body)

            product.name = data.get('name', product.name)
            product.sku = data.get('sku', product.sku)
            product.stock = data.get('stock', product.stock)
            product.price = data.get('price', product.price)

            product.save()

            return JsonResponse(
                {'message': 'Product updated successfully'}
            )

        except json.JSONDecodeError:
            return JsonResponse(
                {'error': 'Invalid JSON'},
                status=400
            )

    # DELETE - Login + delete permission required
    elif request.method == 'DELETE':

        user = get_user_from_request(request)

        if not user:
            return JsonResponse(
                {'error': '401 Unauthorized'},
                status=401
            )

        if not user.has_perm('inventory.delete_product'):
            return JsonResponse(
                {'error': '403 Forbidden: Inventory Admin only'},
                status=403
            )

        product.delete()

        return JsonResponse(
            {'message': 'Product deleted successfully'}
        )

    else:
        return JsonResponse(
            {'error': 'Method not allowed'},
            status=405
        )

@csrf_exempt
def low_stock_list(request):

    if request.method == 'GET':

        low_stock_products = list(
            Product.objects
            .filter(stock__lt=10)
            .values(
                'id',
                'name',
                'stock'
            )
        )

        return JsonResponse(
            {'low_stock': low_stock_products}
        )

    return JsonResponse(
        {'error': 'Method not allowed'},
        status=405
    )



def product_list_html(request):

    products = Product.objects.all()

    return render(
        request,
        'inventory/product_list.html',
        {'products': products}
    )