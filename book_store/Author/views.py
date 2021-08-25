from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from Author.forms import RegistrationForm
from Author.forms import LogInForm
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import User

def index(request):
    return render(request,'index.html')

def registration_view(request):
    # form = RegistrationForm()

    if request.method =='POST':
        print("-->",request.POST.get('firstname'))
        fname = request.POST.get('firstname')
        lname = request.POST.get('lastname')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')


        user = User.objects.create_user(first_name = fname,last_name = lname,email = email, password =  password1,)
        User.is_staff = True
        login(request,user)
        subject = 'Welcome to Book Store'
        message = f'Hi {user.email},Thankyou for registering in Book Store'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email,]
        send_mail(subject, message, email_from, recipient_list)
        return redirect("login")

    return render(request,"author/registration.html",{"form":"Registration"})

def login_view(request):
    if request.method =='POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        request.session['user_id'] = user.id
        request.session['user_email'] = user.email
        #print(user)
        user_data = User.objects.filter(email = username)
        return render(request,'author/userhome.html',{"user":user_data , "loginUser" : user})
    return render(request,'author/login.html')

def home_page(request):
    return render(request,'author/home.html')


def logout_link(request):
    logout(request)
    loginUser = None
    return render(request,'author/login.html', {"loginUser" : loginUser})
