from binascii import Error
from django.db import transaction, IntegrityError
from django.db.models import F
from django.shortcuts import render, get_object_or_404,redirect
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
        # last_name = request.POST['last_name']
        phone = request.POST['phone']
        national = request.POST['national']


        # form = OrderCreateForm(request.POST)
        # if form.is_valid():
        order=Order.objects.create(name=name,phone=phone,national=national)
        order.save()
            # order = form.save()
        user=request.user
        for item in cart:
            try:
                with transaction.atomic():
                    product = item['product']
                    product.capacity = F('capacity') - item['quantity']
                    product.save(update_fields=['capacity'])
            except IntegrityError:
                raise Error
                #  return redirect('product_detail')
            OrderItem.objects.create( order=order,price=item['price'], quantity=item['quantity'])
            Ticket.objects.create(user=user,
                                      order=order, product=item['product'],quantity=item['quantity'])
            # Phone=f"0{phone}"
            #
            # try:
            #     api = KavenegarAPI('4B4C594D2B716F366F6938686B4165732B6D54564F3979476F70642F68706A7863365445762F7A75636A453D')
            #     params = {
            #         'sender': '',
            #         'receptor': f"{phone}",
            #         'message': f"بلیط کنسرت {product.name}   \n شماره بلیط:{order.id} \n میلاد زینلی \n 456156 "
            #             }
            #     response = api.sms_send(params)
            #     print
            #     str(response)
            #
            # except APIException as e:
            #     print
            #     str(e)
            # except HTTPException as e:
            #     print
            #     str(e)

        cart.clear()
        # order_created.delay(order.id)
        # request.session['order_id']=order.id
        # return redirect(reverse('request'))

        return render(request, 'customer/order_created.html', {'order': order, 'cart': cart})

            #

    else:
        return render(request, 'customer/create.html', {
        'cart': cart, })
        # 'form': form

class ticket_pdf(View):
    template='pdf.html' # the template

    def get(self, request,*args, **kwargs):
        order = get_object_or_404(Order, pk=kwargs['order_id'])
        context = {'order': order}
        return render(request,'pdf.html',context)
        # response = PDFTemplateResponse(request=request,
        #                                template=self.template,
        #                                filename="hello.pdf",
        #                                context=context,
        #                                show_content_in_browser=False,
        #                                cmd_options={'margin-top': 10,
        #                                             "zoom": 1,
        #                                             "viewport-size": "1366 x 513",
        #                                             'javascript-delay': 1000,
        #                                             'footer-center': '[page]/[topage]',
        #                                             "no-stop-slow-scripts": True},
        #                                )
        # return response





