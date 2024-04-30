from core.models import Product, ProductImages
from django import forms

ProductImagesFormSet = forms.inlineformset_factory(
    parent_model=Product,
    model=ProductImages,
    fields=('images',),
    extra=3,
    can_delete=True,
    max_num=5 
)

class addProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = [
            'title',
            'image',
            'color',
            'description',
            'price',
            'old_price',
            'gender',
            'specifications',
            'tags',
            'product_status',
            'status',
            'in_stock',
            'featured',
            'digital',
            'sku',
            'category',
            'vendor',
        ]