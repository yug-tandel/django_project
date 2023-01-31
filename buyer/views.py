import random
from django.shortcuts import render,redirect
from django.http import HttpResponse
from buyer.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.conf import settings
from seller.models import *
# Create your views here.
def index(request):
    all_products = Product.objects.all()
    try:
        user_row = BuyerDemo.objects.get(email = request.session['email'])
        return render(request, 'index.html', {'user_data': user_row , 'all_products': all_products})
    except:
        return render(request, 'index.html' , {'all_products': all_products})

def main(request):
    return render(request, 'main.html')

def faqs(request):
    return render(request, 'faqs.html')

def contact(request):
    return render(request, 'contact.html')

def icons(request):
    return render(request, 'icons.html')

def about(request):
    return render(request, 'about.html')

def checkout(request):
    return render(request, 'checkout.html')

def payment(request):
    return render(request, 'payment.html')

def privacy(request):
    return render(request, 'privacy.html')

def product(request):
    return render(request, 'product.html')

def product2(request):
    return render(request, 'product2.html')

def single(request):
    return render(request, 'single.html')

def single2(request):
    return render(request, 'single2.html')

def terms(request):
    return render(request, 'terms.html')

def typography(request):
    return render(request, 'typography.html')

def create_row(request):
    BuyerDemo.objects.create(
        first_name = 'yug',
        last_name = 'tandel',
        email = 'yugtandel05@gmail.com',
        password = 123
    )
    return HttpResponse('row created successfully')
#------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------



# registeration process
def register(request):
    if request.method == 'POST':
        
        try:
            BuyerDemo.objects.get(email = request.POST['email'])
            return render(request, 'register.html',{'msg':'Email is already registered'})

        except ObjectDoesNotExist:
            if request.POST['password'] == request.POST['repassword']:
                global user_dict
                user_dict = {
                    'first_name' : request.POST['first_name'],
                    'last_name': request.POST['last_name'],
                    'mobile' : request.POST['phone'],
                    'email' : request.POST['email'],
                    'password' : request.POST['password'],
                }
                global c_otp
                c_otp = random.randint(1000,9999)
                subject = 'Email Verification'
                message = f'Hello {request.POST["first_name"]},\nYour OTP is {c_otp}'
                from_mail = settings.EMAIL_HOST_USER
                r_list = [(request.POST['email'])]
                send_mail(subject,message,from_mail,r_list)
                return render(request, 'otp.html')
            else:
                return render(request, 'register.html',{'say': 'Both password does not match'})
    else:
        return render(request, 'register.html')
    
def otp(request):
    if str(c_otp) == str(request.POST['u_otp']):
        BuyerDemo.objects.create(
            first_name = user_dict['first_name'],
            last_name = user_dict['last_name'],
            mobile =  user_dict['mobile'],
            email = user_dict['email'],
            password = user_dict['password']
        )
        return HttpResponse('HURRAY !!! Your account has been')
    else:
        return render(request, 'otp.html', {'msg':'otp does not match'})

def login(request):
    if request.method == 'POST':
        try:
            user_row = BuyerDemo.objects.get(email = request.POST['email'])
            if request.POST['password'] == user_row.password:
                request.session['email'] = user_row.email
                print(user_row)
                return redirect('index')
            else:
                return render(request, 'login.html', {'msg':'password is incorrect'})
        except:
            return render(request, 'login.html', {'msg':'Email not registered'})
    else:
        try:
            request.session['email']
            return redirect('index')
        except:
            return render(request, 'login.html')

def forgot_password(request):
    if request.method == 'POST':
        try:
            user_row = BuyerDemo.objects.get(email = request.POST['email'])
    
            subject = 'Get Your Password!!!'
            message = f'hello, {user_row.first_name},\nYour password is {user_row.password}.'
            from_email = settings.EMAIL_HOST_USER
            list1 = [request.POST['email']]
            send_mail(subject,message,from_email,list1)
            return render(request, 'login.html', {'say': 'We have sent your password to your MailBox'})
        except:
            return render(request, 'forgot_pass.html',{'say': 'Email not registered'})
        
    else:
        return render(request, 'forgot_pass.html')

def logout(request):
    del request.session['email']
    return redirect('index')

def buyer_edit_profile(request):
    if request.method == 'POST':
        user_data = BuyerDemo.objects.get(email = request.session['email'])
        user_data.first_name = request.POST['first_name']
        user_data.last_name = request.POST['last_name']
        user_data.mobile = request.POST['mobile']
        user_data.address = request.POST['address']
        try:
            user_data.pic = request.FILES['pic']
            user_data.save()
            return render(request, 'buyer_edit_profile.html',{'user_data':user_data})
        except:
            user_data.save()
            return render(request, 'buyer_edit_profile.html',{'user_data':user_data})
    else:
        try:
            user_data = BuyerDemo.objects.get(email = request.session['email'])
            return render(request, 'buyer_edit_profile.html',{'user_data':user_data})
        except:
            return render(request, 'login.html',{'user_data':user_data})
        return render(request, 'buyer_edit_profile.html')
