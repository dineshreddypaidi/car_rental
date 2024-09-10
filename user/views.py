from django.template import loader
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . import models
from main.views import audit_management
import vechiles
# Create your views here.

def Index(request):
    template = loader.get_template('user/index.html')
    user = request.user
    context = {}
    if user.is_authenticated:
        try:
            profile = models.userprofile.objects.get(username=user)
            context = {
                'profile': profile,
            }
        except models.userprofile.DoesNotExist:
            context = {
                'data': None,
                'error': 'Profile not found',
            }
    else:
        context = {
                'error': 'user not logged in',
            }
    return HttpResponse(template.render(context,request))
    
def Login(request):
    template = loader.get_template('user/login.html')
    
    if request.method == 'POST':
        user_input = request.POST.get('username')
        password = request.POST.get('password')
            
        try:
            user = User.objects.get(
                Q(email=user_input) | 
                Q(username=user_input) |
                Q(userprofile__phone_number=user_input)
            )
        except User.DoesNotExist:
            user = None
            messages.error(request, "user doesn't exist")
            return redirect('login')
           
        user = authenticate(username=user.username, password=password)
            
        if user is not None:
            login(request, user)
            audit_management.add_audit(user,"logged in")
            return redirect('/')
        else:
            messages.error(request, "password wrong..")
            return redirect('login')
        
    return HttpResponse(template.render(request=request))

def Register(request):
    template = loader.get_template('user/register.html')
    
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        phone_number = request.POST.get('phone_number')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('register')
        
        if models.userprofile.objects.filter(phone_number=phone_number).exists():
            messages.error(request, "phone number is already registerd")
            return redirect('register')
        
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register') 
        
        user_obj = {
            'username' : username,
            'password' : password,
            'email' : email,
        }
        
        user_obj = User.objects.create_user(**user_obj)
        user_obj.save()
        
        profile_obj = models.userprofile(username=user_obj,phone_number=phone_number)
        profile_obj.save()
        
        audit_management.add_audit(user_obj,"account created")
        
        login(request, user_obj)
        return redirect('/')

    return HttpResponse(template.render(request=request))

@login_required(login_url='/user/login')
def change_password(request):
    template = loader.get_template('user/change_password.html')
    if request.method == "POST":
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('/user/change_password') 
        
        user_name = request.user
        user_obj = User.objects.get(username=user_name)
        user_obj.set_password(password)
        user_obj.save()
        
        messages.success(request, "Password changed successfully.")
        logout(request)
        return redirect('/user/login')
    
    return HttpResponse(template.render(request=request))

def Logout(request):
    logout(request)
    return redirect('/')

def my_rentals(request):
    template = loader.get_template('user/bookings.html')
    user = request.user
    
    if not user.is_authenticated:
        messages.error(request, "login to view your rentals..")
        return redirect('login')
    
    bike_bookings = vechiles.models.bikeBooking.objects.filter(user=user).order_by('-booking_date').all()
    car_bookings = vechiles.models.carBooking.objects.filter(user=user).order_by('-booking_date').all()
    
    data = {
        'cars' : car_bookings,
        'bikes' : bike_bookings,
    }
    return HttpResponse(template.render(data,request))
