from django.shortcuts import render, redirect, get_object_or_404
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from django.views.decorators.http import require_POST
from customer.forms import OrderCreateForm
from django.forms import formset_factory
from customer.models import OrderItem, Ticket


# def reserve_ticket(request):
#     number_of_ticket = 1
#     cart = Cart(request)
#     getNumberForm = getNumber(request.GET, request.FILES)
#     if getNumberForm.is_valid():  # cleaned_data['quantity']
#         number_of_ticket = getNumberForm.cleaned_data['number']
#
#         # cart.add(product=product,
#         #           quantity=cd['number'])
#     ticketFormSet = formset_factory(OrderCreateForm, extra=number_of_ticket)
#     formset = ticketFormSet()
#     if request.method == 'POST':
#         filled_formset = ticketFormSet(request.POST)
#         if filled_formset.is_valid():
#             for form in filled_formset:
#                 order = form.save()
#                 customer = request.user
#
#                 for item in cart:
#                     Ticket.objects.create(customer=customer,
#                                           order=order, product=item['product'])
#
#             cart.clear()
#             # order_created.delay(order.id)
#             # request.session['order_id']=order.id
#             # return redirect(reverce('process'))
#             return render(request, 'customer/order_created.html', {'order': order})
#     else:
#
#         return render(request, 'customer/reserve_ticket.html', {
#             'formset': formset
#         })


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
    cart.add(product=product,
             quantity=cd['quantity'],
             )
    return redirect('cart_detail')


# def cart_remove(request, product_id):
#     cart = Cart(request)
#     product = get_object_or_404(Product, id=product_id)
#     cart.remove(product)
#     return redirect('cart_detail')


def cart_detail(request):
    cart = Cart(request)
    cart_product_form = CartAddProductForm()
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
                                                                   'update': True})
    return render(request, 'cart/cart_detail.html',
                  {'cart': cart,'cart_product_form': cart_product_form, })

