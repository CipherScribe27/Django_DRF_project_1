from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Product


def validate_title(value):
    # qs = Product.objects.filter(title_exact=value) # it look for case sensitive
    qs = Product.objects.filter(title_iexact=value) # it doesnt look for case sensitive
    if qs.exists():
        raise serializers.ValidationError(f"{value} is already a product name")
    return value


unique_product_title = UniqueValidator(queryset=Product.objects.all())

