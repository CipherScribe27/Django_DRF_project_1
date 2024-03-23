# from rest_framework import generics,mixins,permissions,authentication  # the permissions allow only the admins
# can do crud operations on product model in localhost port, the staffs cant be able to see the product model untill unless i give the permissions in /admin as super user
from rest_framework import generics,mixins
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from .models import Product
from .serializers import ProductSerializer
# from api.permissions import IsStaffEditorPermission because i created as mixins
# from api import authentication
# from api.authentication import TokenAuthentication
from api.mixins import StaffEditorPermissionMixin

# create mixins for serializerclass,authentication and i created for permissions


# Retrieveapiview
class ProductDetailAPIView(StaffEditorPermissionMixin,generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [permissions.IsAdminUser,IsStaffEditorPermission]

    
    def perform_create(self,serializer):
        # print(serializer)
        # serializer.save(user=self.request.user)
        # email = serializer.validated_data.pop('email')
        # print(email)
        print(serializer.validated_data)
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content')
        if content is None:
            content = title
        serializer.save(content=content) # same as form.save() and model.save()

product_detail_view = ProductDetailAPIView.as_view()

class ProductListCreateAPIView(StaffEditorPermissionMixin,generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = [authentication.SessionAuthentication] # we can also do that in function based views too but some inbuilt decorators needed
    # session authentication will allow only the admins can create new datas before going to that the user must have to be an admin and 
    # must created an superuser account to login and create or update the datas
    # this will be done in port of server with logging in admin or by running create.py file
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly] # we cant send post data like we cant create any user but we can use get method to view the datas only
    # permission_classes = [permissions.DjangoModelPermissions] # this DjangoModelPermissions only look for the admins permissions for staffs in /admin panel
    # it will work depends on what permisions that the admin gave to staff
    # we must have to give the permission_classes to all the classes doing crud operations otherwise it will not work properly
    # authentication_classes = [authentication.SessionAuthentication,
    #                           authentication.TokenAuthentication]
    # authentication_classes = [authentication.SessionAuthentication,
    #                           TokenAuthentication] # we dont need this becoz we give that in settings.py file as auth_classes
    # permission_classes = [permissions.IsAdminUser,IsStaffEditorPermission] we created a mixin and imported that so we dont need this
    def perform_create(self,serializer):
        # print(serializer)
        # serializer.save(user=self.request.user)
        print(serializer.validated_data)
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content')
        if content is None:
            content = title
        serializer.save(content=content)
        
    def get_queryset(self,*args, **kwargs):
        request = self.request
        print(request.user)
        return super().get_queryset()
        
    
product_list__create_view = ProductListCreateAPIView.as_view()
    
# class ProductCreateAPIView(generics.CreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
    
# product_create_view = ProductCreateAPIView.as_view()


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

product_List_view = ProductListAPIView.as_view()

@api_view(['GET','POST'])
def product_alt_view(request,pk = None,*args,**kwargs):
    method = request.method # put to update and delete to delete using http methods also
    if method == "GET":
        if pk is not None:
            #detail view
            obj = get_object_or_404(Product,pk=pk)
            data = ProductSerializer(obj, many=False).data
            return Response(data)            
            # queryset = Product.objects.filter(pk=pk)
            # if not queryset.exist():
            #     raise Http404
            # return Response
        # pass # get request detail view => list view
        
        queryset = Product.objects.all()
        data = ProductSerializer(queryset,many = True).data
        return Response(data)
    if method == "POST":
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # print(serializer.data)
            title = serializer.validated_data.get('title')
            content = serializer.validated_data.get('content') or None
            if content is None:
                content = title
            serializer.save(content=content)
            return Response(serializer.data)
        return Response({"Invalid data": "Not a Good Data"},status=400) 
 
class CreateApiView(mixins.CreateModelMixin, generics.GenericAPIView):
    pass 

class ProductMixinView(mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.CreateModelMixin,
                       generics.GenericAPIView): # this mixins will do all the crud operations we just want to change the request methods in the endpoint
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "pk"
    
    def get(self,request,*args,**kwargs): # this method will give the output of list.py when its get method
        # when the method is post we can run the create.py without errors
        print(args,kwargs)
        pk = kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request,*args,**kwargs) 
        return self.list(request, *args,**kwargs)
    
    def post(self,request, *args, **kwargs):
        return self.create(request,*args,**kwargs)        
    
product_mixin_view = ProductMixinView.as_view()
 
class ProductUpdateAPIView(StaffEditorPermissionMixin,generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    # permission_classes = [permissions.IsAdminUser,IsStaffEditorPermission]

    
    def perform_update(self,serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title

product_update_view = ProductUpdateAPIView.as_view()


class ProductDeleteAPIView(StaffEditorPermissionMixin,generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    # permission_classes = [permissions.IsAdminUser,IsStaffEditorPermission]

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
    
product_delete_view = ProductDeleteAPIView.as_view()