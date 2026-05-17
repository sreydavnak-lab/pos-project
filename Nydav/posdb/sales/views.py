# sales/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Order, OrderItem
from .forms import OrderItemForm, ProductForm
import anthropic
import os


@login_required
def product_list(request):
    products = Product.objects.filter(is_active=True)
    return render(request, 'sales/product_list.html', {'products': products})


@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'sales/add_product.html', {'form': form})


@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'sales/add_product.html', {'form': form, 'product': product})


@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    ai_text = None
    try:
        # ✅ ប្រើ environment variable — មិនដាក់ key នៅក្នុង code
        client  = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=200,
            messages=[{
                "role": "user",
                "content": (
                    f"សរសេរការពិពណ៌នាខ្លីៗជាភាសាខ្មែរ (២-៣ ប្រយោគ) "
                    f"សម្រាប់ផលិតផល: {product.name}, "
                    f"ប្រភេទ: {product.category}, "
                    f"តម្លៃ: ${product.price}"
                )
            }],
        )
        ai_text = message.content[0].text
    except Exception:
        ai_text = None
    return render(request, 'sales/product_detail.html', {
        'product': product,
        'ai_text': ai_text,
    })


@login_required
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'sales/order_list.html', {'orders': orders})


@login_required
def create_order(request):
    order = Order.objects.create(cashier=request.user, status='open')
    return redirect('add_item', pk=order.pk)


@login_required
def add_item(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        if 'mark_paid' in request.POST:
            order.status = 'paid'
            order.save()
            return redirect('order_list')
        form = OrderItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.order      = order
            item.unit_price = item.product.price
            item.save()
            return redirect('add_item', pk=order.pk)
    else:
        form = OrderItemForm()
    return render(request, 'sales/add_item.html', {'order': order, 'form': form})


@login_required
def my_orders(request):
    orders = Order.objects.filter(cashier=request.user)
    return render(request, 'sales/my_order.html', {'orders': orders})