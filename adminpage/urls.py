from django.urls import path
from adminpage import views

app_name = "adminpage"

urlpatterns = [
path('dashboard/', views.dashboard, name="dashboard"),
path('products/', views.product, name='products'),
path('add-product/', views.add_product, name='add-product'),
path('edit-product/<pid>/', views.edit_product, name='edit-product'),
path('delete-product/<pid>/', views.delete_product, name='delete-product'),
path('order-detail/<oid>/', views.order_detail, name='order-detail'),
path('change_order_status/<oid>/', views.change_order_status, name='change_order_status'),
]
