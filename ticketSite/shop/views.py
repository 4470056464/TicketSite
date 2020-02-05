from django.shortcuts import render,get_object_or_404
from .models import Product
from cart.cart import Cart

from cart.forms import CartAddProductForm


def product_list(request):
    products=Product.objects.filter(available=True)
    return render(request,'shop/product_list.html',{
        'products':products
    })

def product_detail(request,id,slug):
    product=get_object_or_404(Product,id=id,slug=slug,available=True)
    if  product.capacity < 3:
        return render(request,'shop/complete_capacity.html',{'product':product})
        # raise ValueError("Capacity exceeded")
    cart_product_form=CartAddProductForm()
    cart=Cart(request)
    return render(request,'shop/product_detail.html',{
        'product':product,
        'cart_product_form':cart_product_form,
         'cart':cart
    })
