from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name = 'home' ),
    path('category/<slug:val>/', views.CategoryView.as_view(), name='category'),
    path('all_gadgets/', views.all_gadgets, name='all_gadgets'),
    path('create_gadget/', views.create_gadget, name='create_gadget'),
    path('gadget_detail/<int:pk>/',views.gadget_detail, name='gadget_detail'),
    path('search/',views.search_results, name='search_results'),
    path('edit_gadget/<int:id>/', views.edit_gadget, name='edit_gadget'),
    path('delete_gadget/<int:id>/', views.delete_gadget, name='delete_gadget'),
    path('add_to_cart/gadget/<int:pk>/', views.add_to_cart, name = 'add_to_cart'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name = 'remove_from_cart'),
    path('cart/', views.cart_view, name = 'cart'),
    path('proceed_to_pay/', views.proceed_to_pay, name='proceed_to_pay'),
    path('payment_confirmation/', views.payment_confirmation, name='payment_confirmation'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/',views.user_logout, name='logout'),
    path('newsletter/',views.newsletter, name='newsletter')

]