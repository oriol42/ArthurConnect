from django.urls import path
from . import views

urlpatterns = [
  path('home',views.index,name='index'),
  path('category',views.category,name='category'),
  path('contact',views.contact,name='contact'),
  path('cart',views.cart,name='cart'),
  path('checkout',views.checkout,name='checkout'),
  path('about',views.about,name='about'),
  path('service-client',views.service_client,name='service_client'),
]