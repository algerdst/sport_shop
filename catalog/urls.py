from django.urls import path, include
from rest_framework import routers

from . import views


router=routers.SimpleRouter()
router.register(r'productlist', views.ProductsViewSet)

urlpatterns = [
    path('', views.index, name='home'),
    # path('api/productlist', views.ProductsApiView.as_view()),
    # path('api/productlist/<int:pk>', views.ProductApiUpdateView.as_view()),
    # path('api/detailproduct/<int:pk>', views.ProductDetailView.as_view()),
    # path('api/categorylist', views.CategoriesApiView.as_view()),
    # path('api/productlist', views.ProductsViewSet.as_view({'get':'list'})),
    path('api/', include(router.urls)),
    path('api/productlist/<int:pk>', views.ProductsViewSet.as_view({'put':'update'})),
    path('category/<slug:slug>', views.category_filter, name='filter'),
    path('mark/<int:mark_id>/<int:product_id>', views.get_mark, name='get_mark'),
    path('product/<slug:slug>', views.product, name='product'),
    path('types/<slug:slug>', views.item_types_filter, name='item_type_filter'),
    path('brands/<slug:slug>', views.brand_filter, name='brand_filter'),
    path('basket/add/<int:product_id>', views.basket_add, name='basket_add'),
    path('basket/remove/<int:basket_id>', views.basket_remove, name='basket_remove'),
    path('basket/makepdf/', views.make_order, name='make_order'),
    path('return_order/<int:order_id>', views.return_order, name='return_order'),
    path('save_pdf/<int:order_id>', views.save_pdf, name='save_pdf'),
]
