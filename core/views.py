from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from core.models import Product, Category, Vendor, CartOrder, CartOrderItems, ProductImages, ProductReview, Wishlist, Address, Color, MyList
from userauths.models import Profile 
from django.db.models import Count, Avg
from core.forms import ProductReviewForm
from django.http import HttpResponse, JsonResponse
from taggit.models import Tag
from django.template.loader import render_to_string
from django.contrib import messages
from django.core import serializers
from django.contrib.auth.models import AnonymousUser

from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def index(request):
    products = Product.objects.filter(featured=True).order_by("-id") #this part will allow to list products in landing page, also ordered for latest products to be first shown

    context = {
        "products": products
    }

    return render(request, 'core/index.html', context)

def product_list_view(request):
    products = Product.objects.all().order_by("-id") 

    context = {
        "products": products
    }
    
    return render(request, 'core/product-list.html', context)

def aboutus(request):
    
    return render(request, 'core/aboutus.html')

def privacy(request):
    
    return render(request, 'core/privacy.html')

def contact(request):
    
    return render(request, 'core/contact.html')
def shipping(request):
    
    return render(request, 'core/shipping.html')
def payment(request):
    
    return render(request, 'core/payment.html')
def returns(request):
    
    return render(request, 'core/returns.html')
def career(request):
    
    return render(request, 'core/career.html')
def partnership(request):
    
    return render(request, 'core/partnership.html')
def details(request):
    
    return render(request, 'core/details.html')
def newseason(request):
    
    return render(request, 'core/newseason.html')
def recommended(request):
    
    return render(request, 'core/recommended.html')
def order(request):
    
    return render(request, 'core/order.html')
def services(request):
    
    return render(request, 'core/services.html')

def category_list_view(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    colors = Color.objects.all()
    tags = Product.tags.all()

    context = {
        "categories": categories,
        "products": products,
        "colors": colors, 
        "tags":tags
    }

    return render(request, 'core/category-list.html', context)

def category_product_list_view(request, cid):
    category = Category.objects.get(cid=cid)
    products = Product.objects.filter(product_status="published", category=category)

    context = {
        "category": category,
        "products": products,
    }

    return render(request, 'core/category-product-list.html', context)

def vendor_list_view(request):
    vendors = Vendor.objects.all()
    context = {
        "vendors" : vendors,
    }
    return render(request, "core/vendor-list.html",context)

def vendor_detail_view(request, vid):
    vendor = Vendor.objects.get(vid=vid)
    products = Product.objects.filter(vendor = vendor, product_status="published")
    context = {
        "vendor" : vendor,
        "products": products,
    }
    return render(request, "core/vendor-detail.html",context)


def product_detail_view(request, pid):
    product = Product.objects.get(pid=pid)
    variants = product.variants.all()


    products = Product.objects.filter(category = product.category).exclude(pid=pid)

    # ------->Getting all reviews related to a product<-------
    reviews = ProductReview.objects.filter(product = product).order_by("-date")

    # average reviews
    average_rating = ProductReview.objects.filter(product = product).aggregate(rating = Avg('rating'))

    #review form
    review_form = ProductReviewForm()
    
    # ↓ ↓ ↓ ↓ ↓ ↓ эту часть кода закомментила чтоб юзер мог оставлять несколько комментариев
    create_review = True
 
    # if request.user.is_authenticated:
    #     user_review_count = ProductReview.objects.filter(user = request.user,product=product).count()

    #     if user_review_count > 0:
    #         create_review = False

    p_image = product.p_images.all() #this line is used to access all the images of ONE PRODUCT

    context = {
        "p": product,
        "create_review": create_review,
        "review_form": review_form,
        "p_image": p_image,
        "average_rating": average_rating,
        "reviews": reviews,
        "products" : products,
        "variants": variants
    }

    return render(request, "core/product-detail.html", context)

def tag_list(request, tag_slug=None):
    products = Product.objects.filter(product_status="published").order_by("-id")
    tag = None
    tag_name = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])
        tag_name = tag.name

    context = {
        "products": products,
        "tag_name": tag_name
    }

    return render(request, "core/tag.html", context)



def add_review(request, pid):
    product = Product.objects.get(pk=pid)
    user = request.user

    review = ProductReview.objects.create(
        user=user,
        product = product,
        review = request.POST['review'],
        rating = request.POST['rating'],
    )

    try:
        profile = Profile.objects.get(user=user)
        profile_image_url = profile.image.url
    except Profile.DoesNotExist:
        pass

    context = {
        'user': {
            'username': user.username,
            'profile_image_url': profile_image_url,
        },
        'review': request.POST['review'],
        'rating': request.POST['rating'],
    }

    average_reviews = ProductReview.objects.filter(product=product).aggregate(rating = Avg("rating"))
    
    return JsonResponse(
        {
        'bool': True,
        'context': context,
        'average_reviews' : average_reviews
        }
    )

def search_view(request):
    query = request.GET.get("q")

    products = Product.objects.filter(title__icontains=query).order_by("-date")

    context = {
        "products": products,
        "query": query
    }

    return render(request, "core/search.html", context)

def filter_product(request):
    categories = request.GET.getlist("category[]")
    vendors = request.GET.getlist("vendor[]")
    colors = request.GET.getlist("color[]")
    tags = request.GET.getlist("tag[]")

    min_price = request.GET['min_price']
    max_price = request.GET['max_price']

    # for products page
    products = Product.objects.all().order_by("-price")

    products = products.filter(price__gte=min_price)
    products = products.filter(price__lte=max_price)

    if len(categories) > 0:
        products = products.filter(category__id__in=categories).distinct()
    if len(vendors) > 0:
        products = products.filter(vendor__id__in=vendors).distinct()
    if len(colors) > 0:
        products = products.filter(color__id__in=colors).distinct()
    if len(tags) > 0:
        products = products.filter(tags__name__in=tags).distinct()
    
    data = render_to_string("core/async/product-list.html", {"products": products})
    return JsonResponse({"data": data})


def add_to_cart(request):
    product_in_cart = {
        'title': request.GET['title'], 
        'quantity': int(request.GET['quantity']),
        'price': request.GET['price'],
        'image': request.GET['image'],
        'pid': request.GET['pid'],
        'size': request.GET.get('size', 'N/A')
    }

    product_identifier = f"{request.GET['id']}_{product_in_cart['size']}"

    if 'cart_data_object' in request.session:
        cart_data = request.session['cart_data_object']

        if product_identifier in cart_data:
            cart_data[product_identifier]['quantity'] += int(request.GET['quantity'])  
        else:
            cart_data[product_identifier] = product_in_cart
    else:
        request.session['cart_data_object'] = {product_identifier: product_in_cart}

    request.session.modified = True
    
    return JsonResponse({"data": request.session['cart_data_object'], 'totalItemsInCart': len(request.session['cart_data_object'])})



def view_cart(request):
    cart_total = 0
    if 'cart_data_object' in request.session:
        for p_id, item in request.session['cart_data_object'].items():
            cart_total += int(item['quantity']) * float(item['price'])
        return render(request, "core/cart.html", {"cart_data":request.session['cart_data_object'], 'totalItemsInCart': len(request.session['cart_data_object']), 'cart_total': cart_total})
    messages.warning(request, "Cart is empty")
    return redirect(request.META.get('HTTP_REFERER', 'core:index'))

#UPDATE AND DELETE FROM CART
def delete_from_cart(request):
    product_id = str(request.GET['id'])
    if 'cart_data_object' in request.session:
        if product_id in request.session['cart_data_object']:
            cart_data = request.session['cart_data_object']
            del request.session['cart_data_object'][product_id]
            request.session['cart_data_object'] = cart_data
    cart_total = 0
    if 'cart_data_object' in request.session:
        for p_id, item in request.session['cart_data_object'].items():
            cart_total += int(item['quantity']) * float(item['price'])
    context = render_to_string("core/async/cart-list.html", {"cart_data":request.session['cart_data_object'], 'totalItemsInCart': len(request.session['cart_data_object']), 'cart_total': cart_total})
    return JsonResponse({"data":context, 'totalItemsInCart': len(request.session['cart_data_object'])})

def update_cart(request):
    product_id = str(request.GET['id'])
    product_quantity = int(request.GET['quantity'])
    product_size = request.GET['size']  # Assuming size is always provided
    if 'cart_data_object' in request.session:
        if product_id in request.session['cart_data_object']:
            cart_data = request.session['cart_data_object']
            
            # Check if the product size is different from the current size
            if product_size != cart_data[product_id]['size']:
                # Generate new product identifier with updated size
                new_product_id = f"{product_id.split('_')[0]}_{product_size}"
                
                # Move product data to new identifier and remove old one
                cart_data[new_product_id] = cart_data.pop(product_id)
                product_id = new_product_id

            # Update quantity and size
            cart_data[product_id]['quantity'] = product_quantity
            cart_data[product_id]['size'] = product_size
            
            request.session['cart_data_object'] = cart_data
    
    # Calculate cart total
    cart_total = sum(int(item['quantity']) * float(item['price']) for item in request.session.get('cart_data_object', {}).values())
    
    # Render updated cart data asynchronously
    context = render_to_string("core/async/cart-list.html", {"cart_data": request.session.get('cart_data_object', {}), 'totalItemsInCart': len(request.session.get('cart_data_object', {})), 'cart_total': cart_total})
    
    return JsonResponse({"data": context, 'totalItemsInCart': len(request.session.get('cart_data_object', {}))})


def save_checkout_info(request):
    cart_total = 0
    total_amount = 0

    if request.method=="POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        country = request.POST.get("country")
        city = request.POST.get("city")
        index = request.POST.get("index")
        address = request.POST.get("address")

        request.session['full_name'] = full_name
        request.session['email'] = email
        request.session['mobile'] = mobile
        request.session['country'] = country
        request.session['city'] = city
        request.session['index'] = index
        request.session['address'] = address

        if 'cart_data_object' not in request.session or not request.session['cart_data_object']:
            messages.warning(request, "Your cart is empty. Please add items to your cart before proceeding to checkout.")
            return redirect('core:cart')

        for p_id, item in request.session['cart_data_object'].items():
            total_amount += int(item['quantity']) * float(item['price'])

        user = request.user if request.user.is_authenticated else None

        order = CartOrder.objects.create(
            user=user,
            price=total_amount,
            full_name=full_name,
            email=email,
            phone=mobile,
            country=country,
            city=city,
            index=index,
            address=address,

        )

        del request.session['email']
        del request.session['full_name']
        del request.session['mobile']
        del request.session['country']
        del request.session['city']
        del request.session['index']
        del request.session['address']

        for p_id, item in request.session['cart_data_object'].items():
            cart_total += int(item['quantity']) * float(item['price'])

            if user is not None:
                product_pid = item['pid']
                existing_entry = MyList.objects.filter(user=user, product__pid=product_pid).exists()

                if not existing_entry:
                    product = Product.objects.get(pid=product_pid)
                    my_list = MyList.objects.create(user=user, product=product)


            cart_order_products = CartOrderItems.objects.create(
                order=order, 
                invoice_no="INVOICE_NO" + str(order.id),
                item=item['title'],
                image=item['image'],
                quantity=item['quantity'],
                size=item['size'],
                price=item['price'],
                total=float(item['quantity']) * float(item['price']),
                product = Product.objects.get(pid=item['pid'])
            )

        return redirect("core:checkout", order.oid)
    return redirect("core:checkout", order.oid)

def checkout(request, oid):
    order = CartOrder.objects.get(oid=oid)
    order_items = CartOrderItems.objects.filter(order=order)

    cart_total = order.price

    host = request.get_host()
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': cart_total,
        'item_name': "Order-Item-No-" + str(order.id),
        'invoice': "INV_NO-" + str(order.id),
        'currency_code': "USD",
        'notify_url': 'http://{}{}'.format(host, reverse("core:paypal-ipn")),
        'return_url': 'http://{}{}'.format(host, reverse("core:payment-completed", args=[order.oid])),
        'cancel_url': 'http://{}{}'.format(host, reverse("core:payment-failed")),
    }

    paypal_payment_button = PayPalPaymentsForm(initial=paypal_dict)

    context = {
        "order":order,
        "order_items":order_items,
        'paypal_payment_button': paypal_payment_button
    }

    return render(request, "core/checkout.html", context)
    # return render(request, "core/checkout.html", context)

# @login_required
# def checkout_view(request):
#     cart_total = 0
#     total_amount = 0

#     if 'cart_data_object' not in request.session or not request.session['cart_data_object']:
#         messages.warning(request, "Your cart is empty. Please add items to your cart before proceeding to checkout.")
#         return redirect('core:cart')  # Assuming 'core:cart' is the URL name for your cart view

#     for p_id, item in request.session['cart_data_object'].items():
#         total_amount += int(item['quantity']) * float(item['price'])

#     order = CartOrder.objects.create(
#         user=request.user,
#         price=total_amount
#     )

#     for p_id, item in request.session['cart_data_object'].items():
#         cart_total += int(item['quantity']) * float(item['price'])

#         cart_order_products = CartOrderItems.objects.create(
#             order=order, 
#             invoice_no="INVOICE_NO" + str(order.id),
#             item=item['title'],
#             image=item['image'],
#             quantity=item['quantity'],
#             price=item['price'],
#             total=float(item['quantity']) * float(item['price'])
#         )

    # host = request.get_host()
    # paypal_dict = {
    #     'business': settings.PAYPAL_RECEIVER_EMAIL,
    #     'amount': cart_total,
    #     'item_name': "Order-Item-No-" + str(order.id),
    #     'invoice': "INV_NO-" + str(order.id),
    #     'currency_code': "USD",
    #     'notify_url': 'http://{}{}'.format(host, reverse("core:paypal-ipn")),
    #     'return_url': 'http://{}{}'.format(host, reverse("core:payment-completed")),
    #     'cancel_url': 'http://{}{}'.format(host, reverse("core:payment-failed")),
    # }

    # paypal_payment_button = PayPalPaymentsForm(initial=paypal_dict)

    # return render(request, "core/checkout.html", {"cart_data": request.session['cart_data_object'], 'totalItemsInCart': len(request.session['cart_data_object']), 'cart_total': cart_total, 'paypal_payment_button': paypal_payment_button})



#Payment Completed
def payment_completed_view(request, oid):
    order = CartOrder.objects.get(oid=oid)
    if order.paid_status==False:
        order.paid_status=True
        order.save()

    

    context = {
        "order":order,
        "cart_data":request.session['cart_data_object']
    } 
    return render(request, "core/payment-completed.html", context)


def payment_failed_view(request):
    return render(request, 'core/payment-failed.html')

@login_required
def dashboard(request):
    orders = CartOrder.objects.filter(user=request.user).order_by("-id")
    user_items = CartOrderItems.objects.filter(order__user=request.user)
    address = Address.objects.filter(user=request.user)
    profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        address = request.POST.get("address")
        mobile = request.POST.get("mobile")
        new_address = Address.objects.create(
            user  = request.user,
            address = address,
            mobile = mobile,
        )
        messages.success(request, "Address saved")
        return redirect("core:dashboard")

    context = {
        "profile":profile,
        "orders":orders,
        "address":address,
        "user_items": user_items,
    }
    return render(request, 'core/dashboard.html', context)


def order_detail(request, id):
    order = CartOrder.objects.get(user=request.user, id=id)
    order_items = CartOrderItems.objects.filter(order=order)

    context = {
        "order_items": order_items,
    }
    return render(request, 'core/order-detail.html', context)



def add_to_wishlist(request):
    product_id = request.GET['id']
    product = Product.objects.get(id=product_id)

    context ={}
    wishlist_count = Wishlist.objects.filter(product=product, user = request.user).count()
    print(wishlist_count)

    if wishlist_count > 0:
        context = {
            "bool":True
        }
    else:
        new_wishlist = Wishlist.objects.create(
            product = product,
            user = request.user
        )
        context = {
            "bool":True
        }
    return JsonResponse(context)

def get_wishlist_count(request):
    wishlist_count = Wishlist.objects.filter(user=request.user).count()

    return JsonResponse({'wishlist_count': wishlist_count})

def check_product_in_wishlist(request):
    product_id = request.GET.get('id')
    # Assuming WishlistItem model has a field for product_id
    if Wishlist.objects.filter(product_id=product_id, user=request.user).exists():
        return JsonResponse({'in_wishlist': True})
    else:
        return JsonResponse({'in_wishlist': False})


@login_required
def view_wishlist(request):
    wishlist = Wishlist.objects.all()
    
    context = {
        "w" :wishlist
    }
    return render (request, "core/wishlist.html", context)

def remove_from_wishlist(request):
    pid = request.GET['id']
    wishlist = Wishlist.objects.filter(user=request.user)

    wishlist_delete = Wishlist.objects.get(id = pid)
    delete_product = wishlist_delete.delete()

    context = {
        "bool":  True,
        "w": wishlist
    }
    wishlist_json = serializers.serialize('json',wishlist)
    d = render_to_string("core/async/wishlist-list.html", context)
    return JsonResponse({'data': d, 'w': wishlist_json})

    
    


