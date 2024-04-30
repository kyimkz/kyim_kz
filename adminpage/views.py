from django.shortcuts import render, redirect
from core.models import CartOrder, Product, Category, CartOrderItems, Vendor
from django.db.models import Sum
from userauths.models import User
from adminpage.forms import addProductForm, ProductImagesFormSet
from django.db.models import Q
from django.contrib import messages

import datetime

def dashboard(request):
    revenue = CartOrder.objects.aggregate(price=Sum("price"))
    total_order = CartOrder.objects.all()
    all_products = Product.objects.all()
    all_categories = Category.objects.all()
    customers = User.objects.all().order_by("-id")
    best_sold_products = CartOrderItems.objects.values('item', 'size', 'image').annotate(total_sales=Sum('quantity')).order_by('-total_sales')[:10]
    vendor_sales = Vendor.objects.annotate(total_income=Sum('product__cartorderitems__total',filter=Q(product__cartorderitems__order__paid_status=True))).order_by('-total_income')
    month = datetime.datetime.now().month

    monthly_income = CartOrder.objects.filter(order_date__month=month).aggregate(price=Sum("price"))

    context = {
        "revenue":revenue,
        "total_order":total_order,
        "all_products":all_products,
        "all_categories":all_categories,
        "customers":customers,
        "monthly_income":monthly_income,
        "best_sold_products":best_sold_products,
        "vendor_sales":vendor_sales,
    }

    return render(request, "adminpage/dashboard.html", context)

def product(request):
    all_products = Product.objects.all().order_by("-id")
    all_categories = Category.objects.all()

    context = {
        "all_products":all_products,
        "all_categories":all_categories,
    }

    return render(request, "adminpage/products.html", context)


def add_product(request):
    if request.method == "POST":
        product_form = addProductForm(request.POST, request.FILES)
        formset = ProductImagesFormSet(request.POST, request.FILES, instance=None)
        if product_form.is_valid() and formset.is_valid():
            product = product_form.save(commit=False)
            product.user = request.user
            product.save()

            raw_tags = request.POST.get('tags', '')  # Get the raw tags string
            cleaned_tags = [tag.strip() for tag in raw_tags.split(',') if tag.strip()]  # Strip whitespace and remove empty tags
            product.tags.add(*cleaned_tags)

            formset.instance = product
            formset.save()
            return redirect("adminpage:dashboard")
    else:
        product_form = addProductForm()
        formset = ProductImagesFormSet(instance=None)

    context = {
        "product_form": product_form,
        "formset": formset
    }

    return render(request, "adminpage/add-product.html", context)

def edit_product(request, pid):
    product = Product.objects.get(pid=pid)
    if request.method == "POST":
        product_form = addProductForm(request.POST, request.FILES, instance=product)
        formset = ProductImagesFormSet(request.POST, request.FILES, instance=product)
        if product_form.is_valid() and formset.is_valid():
            product = product_form.save(commit=False)
            product.user = request.user
            product.save()

            raw_tags = request.POST.get('tags', '')  # Get the raw tags string
            cleaned_tags = [tag.strip() for tag in raw_tags.split(',') if tag.strip()]  # Strip whitespace and remove empty tags
            product.tags.add(*cleaned_tags)

            formset.instance = product
            formset.save()
            return redirect("adminpage:edit-product", product.pid)
    else:
        product_form = addProductForm(instance=product)
        formset = ProductImagesFormSet(instance=product)

    context = {
        "product_form": product_form,
        "formset": formset,
        'product':product
    }

    return render(request, "adminpage/edit-product.html", context)

def delete_product(request, pid):
    product = Product.objects.get(pid=pid)
    product.delete()
    return redirect("adminpage:products")

def order_detail(request, oid):
    order = CartOrder.objects.get(oid=oid)
    order_items = CartOrderItems.objects.filter(order=order)

    context = {
        "order":order,
        "order_items":order_items
    }

    return render(request, "adminpage/order-detail.html", context)

def change_order_status(request, oid):
    order = CartOrder.objects.get(oid=oid)
    if request.method == "POST":
        status = request.POST.get("status")
        order.product_status = status
        order.save()
        messages.success(request, f"Order status changed to {status}")

    return redirect('adminpage:order-detail', order.oid) 

