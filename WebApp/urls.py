from django.urls import path
from WebApp import views

urlpatterns = [
        path('home/',views.home_page,name="home"),
        path('about/',views.about_page,name="about"),
        path('all_products/',views.all_products,name="all_products"),
        path('cart/',views.cart_page,name="cart"),
        path('save_cart/',views.save_cart,name="save_cart"),
        path('delete_cart_item/<int:pro_id>',views.delete_cart_item,name="delete_cart_item"),
        path('filtered_product/<cat_name>',views.filtered_product,name="filtered_product"),
        path('single_product/<int:pro_id>',views.single_product,name="single_product"),
        path('contact/',views.contact_page,name="contact"),
        path('checkout/',views.checkout_page,name="checkout"),

        path('register/',views.register_page,name="register"),
        path('login/',views.login_page,name="login"),
        path('save_user/',views.save_user,name="save_user"),
        path('user_login/',views.user_login,name="user_login"),
        path('user_logout/',views.user_logout,name="user_logout")

]