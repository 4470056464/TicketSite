from django.shortcuts import render

# -*- coding: utf-8 -*-
# Github.com/Rasooll
from django.http import HttpResponse
from django.shortcuts import redirect,get_object_or_404
from zeep import Client
from customer.models import Order
from kavenegar import *



MERCHANT = '656b9330-8de3-11e9-b4f2-000c29344814'
client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
# amount = 100  # Toman / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
email = 'email@example.com'  # Optional
mobile = '09135290676'  # Optional
CallbackURL = 'http://127.0.0.1:8000/zarinpal/verify/' # Important: need to edit for realy server#

def send_request(request):
    order_id=request.session.get('order_id')
    order=get_object_or_404(Order,pk=order_id)
    amount=order.get_total_cost()
    result = client.service.PaymentRequest(MERCHANT,amount, description, email, mobile, CallbackURL)
    if result.Status == 100:
        return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
    else:
        return HttpResponse('Error code: ' + str(result.Status))

def verify(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, pk=order_id)
    amount = order.get_total_cost()
    if request.GET.get('Status') == 'OK':
        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], amount)
        if result.Status == 100:

            api = KavenegarAPI('4B4C594D2B716F366F6938686B4165732B6D54564F3979476F70642F68706A7863365445762F7A75636A453D')
            params = {
                    'sender': '',
                    'receptor': f"{order.phone}",
                    'message': f"{order.id} \n میلاد زینلی \n 456156 "
                        }
            response = api.sms_send(params)
            print
            str(response)
            return render(request, 'customer/order_created.html', {'order': order})


            # except APIException as e:
            #     print
            #     str(e)
            # except HTTPException as e:
            #     print
            #     str(e)
            #  return HttpResponse('Transaction success.\nRefID: ' + str(result.RefID))
        elif result.Status == 101:
            return HttpResponse('Transaction submitted : ' + str(result.Status))
        else:
            return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))
    else:
        return HttpResponse('Transaction failed or canceled by user')
