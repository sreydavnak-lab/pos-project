# sales/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # ── Part 1 views ──────────────────────────────────────
    path('products/',              views.product_list,   name='product_list'),
    path('products/<int:pk>/',     views.product_detail, name='product_detail'),
    path('orders/',                views.order_list,     name='order_list'),

    # ── Part 2 views ──────────────────────────────────────
    path('orders/new/',            views.create_order,   name='create_order'),
    path('orders/<int:pk>/items/', views.add_item,       name='add_item'),

    # ── Part 3 views ──────────────────────────────────────
    path('orders/mine/',           views.my_orders,      name='my_orders'),

    # ✅ Bonus Challenge — Product CRUD ────────────────────
    path('products/add/',          views.add_product,    name='add_product'),
    path('products/<int:pk>/edit/', views.edit_product,  name='edit_product'),
]