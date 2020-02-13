import re
from binascii import Error
from django.contrib import messages
from django.db import transaction, IntegrityError
from django.db.models import F
from django.shortcuts import render, get_object_or_404,redirect
from django.template.loader import get_template
from django.urls import reverse
from django.views.generic.base import View
from wkhtmltopdf.views import PDFTemplateResponse
from .models import OrderItem, Ticket, Order
from kavenegar import *

# from .tasks import order_created
from cart.cart import Cart



def order_create(request):
    cart = Cart(request)

    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        national = request.POST['national']
        rule = re.compile(r'(^09)[\d]{9}$')
        rule2= re.compile(r'^[\d]{10}$')
        if not rule.search(phone):
            messages.error(request, 'شماره موبایل معتبر نیسست', 'warning')
            return redirect('order_create')
        elif not rule2.search(national):
            messages.error(request, 'شماره ملی معتبر نیسست', 'warning')
            return redirect('order_create')

        order=Order.objects.create(name=name,phone=phone,national=national)
        order.save()
            # order = form.save()
        user=request.user
        for item in cart:
            try:
                with transaction.atomic():
                    product = item['product']
                    product.capacity = F('capacity') - 1
                    product.save(update_fields=['capacity'])
            except IntegrityError:
                raise Error
                #  return redirect('product_detail')
            OrderItem.objects.create( order=order,price=item['price'], quantity=item['quantity'])
            Ticket.objects.create(user=user,
                                    order=order, product=item['product'],quantity=item['quantity'])
        cart.clear()
        # order_created.delay(order.id)
        # request.session['order_id']=order.id
        # return redirect(reverse('request'))
        return render(request, 'customer/order_created.html', {'order': order, 'cart': cart})
    else:
        return render(request, 'customer/create.html', {
        'cart': cart})

class ticket_pdf(View):
    template='pdf.html' # the template

    def get(self, request,*args, **kwargs):
        order = get_object_or_404(Order, pk=kwargs['order_id'])
        context = {'order': order}
        # return render(request,'pdf.html',context)
        response = PDFTemplateResponse(request=request,
                                       template=self.template,
                                       filename="hello.pdf",
                                       context=context,
                                       show_content_in_browser=False,
                                       cmd_options={'margin-top': 10,
                                                    "zoom": 1,
                                                    "viewport-size": "1366 x 513",
                                                    'javascript-delay': 1000,
                                                    'footer-center': '[page]/[topage]',
                                                    "no-stop-slow-scripts": True},
                                       )
        return response




