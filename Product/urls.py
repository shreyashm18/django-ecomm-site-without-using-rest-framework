from django.urls import path,include
from . import views


urlpatterns = [
    
    # path('product_list/',views.product_list,name='all_products' ),
    # # path('product_detail/',views.product_detail,name='product_detail' ),
    # path('add/',views.add,name='add-product'),
    # path('add-category/',views.add_category,name='add-category'),
    # path('update/<int:prod_id>/',views.update_prod,name = "update_prod"),
    # path('delete/<int:prod_id>/',views.delete_prod,name ="delete_prod" ),
    # path('by_category/<int:category_id>',views.by_category,name ="by_category" ),
    # path('cart/<int:prod_id>/',views.add_to_cart,name ="add_to_cart"),
    # path('remove_cart/<int:prod_id>/',views.remove_from_cart,name ="remove_from_cart"),
    # path('mycart/',views.cart_list,name ="my_cart"),
    # path('all_carts/',views.all_carts,name ="all_carts"),
    # path('detail/<int:prod_id>/',views.detail_prod,name ="detail_prod" ),

    path('',views.ProductCRUDSingleEndpoint.as_view()),
    path('category/',views.CategoryCRUDSingleEndpoint.as_view()),
    path('prod-by-category/',views.ProductByCategoryId.as_view()),
    path('add-remove-cart/',views.CartAddRemove.as_view()),
    path('cart_bill/',views.cart_bill.as_view()),
]
