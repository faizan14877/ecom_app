from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop, name='index'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('product/<int:myid>', views.productView, name='productView'),
    path('search', views.search, name='search'),
    path('checkout', views.checkout, name='checkout'),
    path('tracker', views.tracker, name='tracker')
]