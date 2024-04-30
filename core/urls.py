from django.urls import path, include
from core.views import check_product_in_wishlist, get_wishlist_count, save_checkout_info, checkout, index, view_wishlist, recommended, newseason, remove_from_wishlist, add_to_wishlist,product_list_view, category_list_view, details, services, order, returns, career, partnership, payment, category_product_list_view, shipping, product_detail_view, add_review, vendor_list_view, contact, vendor_detail_view, tag_list, aboutus, privacy, search_view, filter_product, add_to_cart, payment_completed_view, payment_failed_view, view_cart, delete_from_cart, update_cart, dashboard, order_detail

app_name = "core"

urlpatterns = [
    path("", index, name="index"),
    path("product/<pid>/", product_detail_view, name="product-detail"),
    path("products/", category_list_view, name="category-list"),
    path("category/<cid>/", category_product_list_view, name="category-product-list"),

    path("aboutus/", aboutus, name='aboutus'),
    path("privacy/", privacy, name='privacy'),
    path("contact/", contact, name='contact'),
    path("shipping/", shipping, name='shipping'),
    path("returns/", returns, name='returns'),
    path("payment/", payment, name='payment'),
    path("details/", details, name='details'),
    path("partnership/", partnership, name='partnership'),
    path("career/", career, name='career'),
    path("order/", order, name='order'),
    path("services/", services, name='services'),
    path("newseason/", newseason, name='newseason'),
    path("recommended/", recommended, name='recommended'),
    path("sale/", product_list_view, name="product-list"),

    #Add Review
    path("add-review/<int:pid>/", add_review, name = "add-review"),

    #Vendor
    path("vendor/", vendor_list_view, name = "vendor-list"),
    path("vendor/<vid>", vendor_detail_view, name = "vendor-detail"),

    #Tags
    path("products/tag/<slug:tag_slug>/", tag_list, name="tags"),

    #Search
    path("search/", search_view, name="search"),

    #Filter
    path("filter-products/", filter_product, name="filter-product"),

    #Cart
    path("cart/", view_cart, name="cart"),
    path("add-to-cart/", add_to_cart, name="filter-product"),
    path("update-cart/", update_cart, name="update-cart"),
    path("delete-from-cart/", delete_from_cart, name="delete-from-cart"),

    #Wishlist
    path('wishlist/', view_wishlist, name="wishlist"),
    path('add-to-wishlist/', add_to_wishlist, name="add-to-wishlist"),
    path('get-wishlist-count/', get_wishlist_count, name='get-wishlist-count'),
    path('check-product-in-wishlist/', check_product_in_wishlist, name='check-product-in-wishlist'),
    path('remove-from-wishlist/', remove_from_wishlist, name="remove-from-wishlist"),

    #Paypal
    path('paypal/', include('paypal.standard.ipn.urls')),

    #Success Payment
    path('payment-completed/<int:oid>/', payment_completed_view, name="payment-completed"), 
    
    #Faied Payment
    path('payment-failed/', payment_failed_view, name="payment-failed"),

    #Dashboard
    path('dashboard/', dashboard, name="dashboard"),

    path('dashboard/order/<int:id>/', order_detail, name="order-detail"),

    #Checkout
    path('checkout/<oid>', checkout, name="checkout"),
    path('save_checkout_info/', save_checkout_info, name="save_checkout_info"),
]