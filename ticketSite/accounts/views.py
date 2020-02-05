from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .forms import PhonLoginForm
from random import randint
from kavenegar import *



def login(request):
    if request.method == 'POST':
        # login USER
        username = request.POST['username']
        Password = request.POST['Password']
        user = authenticate(request, username=username, password=Password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'you are logged in','success')
            return redirect('product_list')
        else:
            messages.error(request, 'نام کاریری یا رمزعبور اشتباه است','warning')
            return redirect('login')

    else:
        return render(request, 'accounts/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        #  messages.success(request,'you are logged out')
        return redirect('product_list')
    #  return render(request, 'accounts/logout.html')
    else:
        return redirect('logout')


def register(request):
    if request.method == 'POST':
        # GET FORM VALUES
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST[' password']
        password2 = request.POST[' password2']

        # CHECK IF PASSWORD MATCH
        if password == password2:

            # check username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'the username is token','warning')
                return redirect('register')

            else:
                # LOOKS GOOD
                user = User.objects.create_user(
                    username=username, password=password, last_name=last_name ,first_name=first_name)#
                # LOGIN AFTER REGISTER
                user.save()
                messages.success(request, 'you are register ','success')
                auth.login(request, user)
                return redirect('product_list')

        else:
            messages.error(request, 'passwords do not match')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')

def dashboard(request):
    return render(request, 'accounts/dashboard.html',)


def PhoneLogin(request):
    if request.method == 'POST':
        form=PhonLoginForm(request.POST)
        if form.is_valid():

            phone=form.cleaned_data['phone']
            randNum=randint(1000,9999)

            # try:
            #     api = KavenegarAPI('4B4C594D2B716F366F6938686B4165732B6D54564F3979476F70642F68706A7863365445762F7A75636A453D')
            #     params = {
            #         'sender': '',
            #         'receptor': phone,
            #         'message': randNum
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
        pass
    else:
        form=PhonLoginForm()
    return render(request,'accounts/PhoneLogin.html',{'form':form})
