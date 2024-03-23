import json
from products.models import Product
from django.forms.models import model_to_dict
from rest_framework.response import Response
from rest_framework.decorators import api_view
from products.serializers import ProductSerializer
from django.http import JsonResponse

    
@api_view(["POST"])
def api_home(request,*args,**kwargs):
    serializer = ProductSerializer(data = request.data)
    # if serializer.is_valid(raise_exception=True): we can create the error message too
    if serializer.is_valid():
        # instance = serializer.save()
        # instance = forms.save()
        # print(instance)
        print(serializer.data)
        # data = serializer.data
        return Response(serializer.data)
    else:
        return Response({"Invalid":"Not a good data"},status=400)
