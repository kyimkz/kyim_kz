from django.contrib import admin
from django.utils.safestring import mark_safe
from core.models import Product, Category, CategoryImages, Vendor, CartOrder, CartOrderItems, ProductImages, ProductReview, Wishlist, Address, Color, MyList

class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages

class CategoryImagesAdmin(admin.TabularInline):
    model = CategoryImages

#list_display specifies the fields to display in the list view of the model in admin panel
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = ['title', 'id', 'user', 'product_image', 'price', 'category', 'vendor', 'featured', 'product_status', 'gender', 'color'] 

class CategoryAdmin(admin.ModelAdmin):
    inlines = [CategoryImagesAdmin]
    list_display = ['title', 'category_image']

class VendorAdmin(admin.ModelAdmin):
    list_display = ['title', 'vendor_image']

class CartOrderAdmin(admin.ModelAdmin):
    list_editable = ['paid_status', 'product_status']
    list_display = ['user', 'email', 'price', 'paid_status', 'order_date', 'product_status', 'get_active']

    def get_active(self, obj):
        return obj.user.is_active if obj.user else None

    get_active.boolean = True
    get_active.short_description = 'Verified'

class CartOrderItemsAdmin(admin.ModelAdmin):
    list_display = ['order', 'invoice_no', 'item', 'order_image', 'quantity', 'size', 'price', 'total', 'vendor_title']

    def vendor_title(self, obj):
        return obj.product.vendor.title if obj.product else None

    vendor_title.short_description = 'Vendor'

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'review', 'rating']

class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'date']

class AddressAdmin(admin.ModelAdmin):
    list_editable = ['address', 'status']
    list_display = ['user', 'address', 'status']

class ColorAdmin(admin.ModelAdmin):
    list_display = ['title', 'code', 'color_display']

class MyListAdmin(admin.ModelAdmin):
    list_display = ['user', 'product']

#allows models to be managed via admin panel
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(CartOrder, CartOrderAdmin)
admin.site.register(CartOrderItems, CartOrderItemsAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(MyList, MyListAdmin)
