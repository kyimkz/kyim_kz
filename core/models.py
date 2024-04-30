from django.db import models
from shortuuid.django_fields import ShortUUIDField
# from shortuuidfield import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User
from taggit.managers import TaggableManager
#tuples(ordered sequence of values) containing choices for different fields in the models

STATUS_CHOICE = (
    ("processing", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
) 
STATUS = (
    ("draft", "Draft"),
    ("disabled", "Disabled"),
    ("rejected", "Rejected"),
    ("in_review", "In Review"),
    ("published", "Published"),
)

RATING = (
    (1, "★☆☆☆☆"),
    (2, "★★☆☆☆"),
    (3, "★★★☆☆"),
    (4, "★★★★☆"),
    (5, "★★★★★"),
)

def user_directory_path(instance, filename): #generates path(in our case example/website/media/user_1*folder_for_each_user_who_uploads_products)
    return 'user_{0}/{1}'.format(instance.user.id, filename)

#Each class represents a database table, that will be represented in admin panel through admin.py

class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="cat", alphabet="abcdefgh12345")
    title = models.CharField(max_length=100, default="clothes")
    image = models.ImageField (upload_to="category", default="category.jpg")
    
    class Meta:
        verbose_name_plural = "Categories"
        
    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url)) 

    def __str__(self):
        return self.title
    
class CategoryImages (models.Model):
    images = models. ImageField(upload_to="category-images", default="category.jpg")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Category Images"
    
class Tags(models.Model):
    pass

class Vendor(models.Model):
    vid = ShortUUIDField (unique=True, length=10, max_length=20, prefix="ven", alphabet="abcdefgh12345")

    title = models.CharField(max_length=100, default="Prava")
    image = models.ImageField (upload_to=user_directory_path, default="vendor.jpg")
    cover_image = models.ImageField (upload_to=user_directory_path, default="vendor.jpg")
    description = models.CharField(null=True, blank=True, default="I am an amazing vendor", max_length=100)

    address = models.CharField (max_length=100, default="123 Main Street.")
    contact = models.CharField(max_length=100, default="+123 (456) 789")
    chat_resp_time = models.CharField(max_length=100, default="100")
    shipping_on_time = models.CharField (max_length=100, default="100")
    authentic_rating = models.CharField (max_length=100, default="100")
    days_return = models.CharField (max_length=100, default="100")
    warranty_period = models.CharField(max_length=100, default="100")

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add =True, null = True, blank = True)

    class Meta:
        verbose_name_plural = "Vendors"
        
    def vendor_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url)) 

    def __str__(self):
        return self.title
    
class Color(models.Model):
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.title
    
    def color_display(self):
        if self.code is not None:
            return mark_safe('<div style="width: 20px; height: 20px; border: 1px solid var(--color-fg); border-radius: 50%; background-color: {}"></div>'.format(self.code))
        else:
            return ""
    
class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefgh12345")

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=1)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="category", default=4)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, related_name = "product", default=7)

    title = models.CharField(max_length=100)
    image = models.ImageField (upload_to=user_directory_path, default="product.jpg")
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, related_name="color")
    variants = models.ManyToManyField('self', blank=True) #checking
    description = models.CharField(null=True, blank=True, max_length=100)

    price = models.DecimalField (max_digits=12, decimal_places=0, default="50")#could be changed in future
    old_price = models.DecimalField (max_digits=12, decimal_places=0, default="80")#could be changed in future
    gender = models.CharField(max_length=100, default="Female")
    specifications = models.CharField(null=True, blank=True, max_length=100)

    tags = TaggableManager(blank=True)
    #tags = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True)

    product_status = models.CharField (choices=STATUS, max_length=10, default="published")
    
    status = models. BooleanField(default=True)
    in_stock = models. BooleanField (default=True) 
    featured = models. BooleanField (default=False)
    digital = models. BooleanField (default=False)

    sku = ShortUUIDField(unique=True, length=4, max_length=10, prefix="sku", alphabet="1234567890", null=True)
    
    date = models.DateTimeField (auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Products"
        
    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def __str__(self): 
        return self.title
    
    def get_percentage(self):
        new_price =(self.price / self.old_price) * 100
        return new_price
    
class ProductImages (models.Model):
    images = models. ImageField(upload_to="product-images", default="product.jpg")
    product = models.ForeignKey(Product, related_name="p_images", on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Product Images"


##################################### CartOrder, OrderITems and Address ####################################
##################################### CartOrder, OrderITems and Address ####################################
##################################### CartOrder, OrderITems and Address ####################################



class CartOrder (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)

    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    index = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)

    delivery_method = models.CharField(max_length=100, null=True, blank=True)
    tracking_id = models.CharField(max_length=100, null=True, blank=True)
    tracking_website_address = models.CharField(max_length=100, null=True, blank=True)

    price = models. DecimalField(max_digits=12, decimal_places=2, default="0.00")
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS_CHOICE, max_length=30, default="processing")
    oid = ShortUUIDField(length=5, max_length=20, alphabet="1234567890", null=True, blank=True)
    payment_method = models.CharField(max_length=100, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Cart Order"

class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=200)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.ImageField(upload_to=user_directory_path)
    quantity = models.IntegerField(default=0)
    size = models.CharField(max_length=20, blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default="0.00")
    total = models.DecimalField(max_digits=12, decimal_places=2, default="0.00")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Cart Order Items"

    def order_image(self):
        # Generate HTML for displaying the image with correct URL
        url = self.image.url
        if url.startswith('/media/media/'):
            url = url.replace('/media/media/', '/media/')
        return mark_safe('<img src="%s" width="50" height="50" />' % url)
    
class MyList(models.Model):#will be used in recommender function
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    paid_status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "My Lists"
    

        
########################### ProductReview, Wishlist and Address ###################################    
########################### ProductReview, Wishlist and Address ###################################    
########################### ProductReview, Wishlist and Address ###################################    


class ProductReview(models.Model): #will be used in recommender function
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name = "reviews")
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = "Product Reviews"

    def _str_(self):
        return self.product.title
    
    def get_rating(self):
        return self.rating
    

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Wishlists"

    def _str_(self):
        return self.product.title
    

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=100, null=True)
    mobile = models.CharField(max_length=300, null=True)
    status = models.BooleanField(default=False)
    

    class Meta:
        verbose_name_plural = "Address"