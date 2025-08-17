from django.urls import path
from . import views

urlpatterns = [
  path('home',views.index,name='index'),
  path('article',views.article,name='article'),
  path('contact',views.contact,name='contact'),
  path('cart',views.cart,name='cart'),
  path('checkout',views.checkout,name='checkout'),
  path('about',views.about,name='about'),
  path('service-client',views.service_client,name='service_client'),
  path('formation',views.formation,name='formation'),
  path('formation/<int:formation_id>/', views.formation_detail, name='formation_detail'),
  path('article/<int:article_id>/', views.article_detail, name='article_detail'),
]