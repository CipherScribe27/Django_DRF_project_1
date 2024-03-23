from rest_framework import serializers
from .models import Product
from rest_framework.reverse import reverse
from .validators import validate_title
    
class ProductSerializer(serializers.ModelSerializer):
    my_discount = serializers.SerializerMethodField(read_only=True)
    url = serializers.SerializerMethodField(read_only=True)
    # url = serializers.HyperlinkedIdentityField(
    #     view_name='product-detail',
    #     lookup_field = 'pk'
    # )
    # email = serializers.EmailField(write_only=True)
    title = serializers.CharField(validators=[validate_title]) # validating the title field by importing the validators i created ownly
    
    # name = serializers.CharField(source='title',read_only = True)
    class Meta:
        model = Product
        fields = [
            'user',
            'url',
            'pk',
            'title',
            # 'email',
            # 'name',
            'content',
            'price',
            'sale_price',
            'my_discount',
        ]
        
    # def validate_title(self,value):
    #     # qs = Product.objects.filter(title_exact=value) # it look for case sensitive
    #     qs = Product.objects.filter(title_iexact=value) # it doesnt look for case sensitive
    #     if qs.exists():
    #         raise serializers.ValidationError(f"{value} is already a product name")
    #     return value
    
    # def validate_title(self,value):
        # req = self.context.get('request')
        # user = req.user
        # qs = Product.objects.filter(user=user,title_iexact=value)
    #     # qs = Product.objects.filter(title_exact=value) # it look for case sensitive
    #     qs = Product.objects.filter(title_iexact=value) # it doesnt look for case sensitive
    #     if qs.exists():
    #         raise serializers.ValidationError(f"{value} is already a product name")
    #     return value
    
    # def create(self, validated_data):
    #     return Product.objects.create(**validated_data)
    #   return super().create(validated_data)
        # email = validated_data.pop('email')
        # obj = super().create(validated_data)
        # print(email,obj)
        # return obj
        
    # def update(self, instance, validated_data):
        # email = validated_data.pop('email')
    #     instance.title = validated_data.get('title')
    #     return instance
        # return super().update(instance, validated_data)
        
    def get_url(self,obj):
        # return f"/api/v2/products/{obj.pk}/"
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("product-detail", kwargs={"pk":obj.pk}, request=request)
        
    def get_my_discount(self,obj):
        if not hasattr(obj,'id'):
            return None
        if not isinstance(obj, Product):
            return None
        return obj.get_discount()
        # try:
        #     return obj.get_discount()
        # except:
        #     return None
