from django.conf.urls import url,include
from django.urls import path
from . import views

urlpatterns = [
  path('', views.cart_detail,name='cart_detail'),
  path('add/<int:product_id>', views.cart_add,name='cart_add'),
  # path('reserve/', views.reserve_ticket,name='reserve_ticket')
  path('remove/<int:product_id>', views.cart_remove,name='cart_remove'),
]