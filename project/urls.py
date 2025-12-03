"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home" ),
    path('about/', views.about, name="about" ),
    path('contact/', views.contact, name="contact" ),

    path('login/', views.login_user , name="login" ),
    path('logout/', views.logout_user , name="logout" ),
    path('signup/', views.signup_user , name="signup" ),
    path('profile/', views.profile, name='profile'),

    path('profile_update/', views.profile_update, name='profile_update'),

    path('seller_dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('register_seller/', views.register_seller, name='register_seller'),
    path('seller_product/', views.seller_product, name='seller_product'),
    path('seller/orders/', views.seller_orders, name='seller_orders'),
    path('seller/orders/<int:order_id>/', views.seller_order_detail, name='seller_order_detail'),
    path('seller/customers/', views.seller_customer, name='seller_customers'),


    path('delete-painting/<int:painting_id>/', views.delete_painting, name='delete_painting'),



    path('search/', views.search_paintings , name="search_paintings" ),

    path('base/', views.base, name="base" ),

    path('product/<int:pk>/', views.product, name="product" ),

    path('category/<int:pk>/', views.category, name="category" ),

    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:painting_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('clearall/', views.clearall, name='clearall'),

    path('checkout/', views.checkout, name='checkout'),
    path('order_confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('order_confirmation_list/', views.order_confirmation_list, name='order_confirmation_list'),

    path('seller/order/<int:order_id>/shipped/', views.mark_as_shipped, name='mark_as_shipped'),
    path('seller/order/<int:order_id>/delivered/', views.mark_as_delivered, name='mark_as_delivered'),


    path('orders/', views.view_orders, name='view_orders'),
    path('buy-now/<int:painting_id>/', views.direct_order, name='direct_buy'),
    path('order/cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),

    path('orders/<str:order_id>/invoice/', views.generate_invoice, name='generate_invoice'),

    # path('dashboard/monthly-revenue/', views.monthly_revenue_data, name='monthly_revenue_data'),

    
    
]+ static(settings. MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG is False:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)