from django.urls import path
from . import views

urlpatterns = [
    # path('<int:pk>/',views.product_mixin_view),
    path('<int:pk>/',views.product_detail_view, name = 'product-detail'), # created as object for that class in view.py 
    # path('<int:pk>/',views.ProductDetailAPIView.as_view()), # directly calling the as_view here 
    # path('',views.product_create_view)
    path('',views.ProductListCreateAPIView.as_view(), name = 'product-list'),
    # path('',views.product_alt_view) # one single view for viewing,creating
    # path('',views.product_detail_view),
    # path('',views.product_mixin_view),
    path('<int:pk>/update/',views.ProductUpdateAPIView.as_view()),
    path('<int:pk>/delete/',views.product_delete_view)
    # path('<int:pk>/delete',views.product_detail_view)
]
