from core.models import Product, Category, Vendor, CartOrder, CartOrderItems, ProductImages, ProductReview, Wishlist, Address
from django.db.models import Min, Max
from django.contrib import messages
def default(request):
    categories = Category.objects.all()
    vendors = Vendor.objects.all()

    min_to_max_price = Product.objects.aggregate(Min("price"), Max("price"))


    return {
        'categories': categories,
        'vendors': vendors,
        'min_to_max_price': min_to_max_price,
    }
