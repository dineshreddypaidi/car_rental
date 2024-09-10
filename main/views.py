from django.template import loader
from django.http import HttpResponse

import vechiles.models
from . import models
from django.contrib import messages
from django.shortcuts import redirect
import vechiles

class audit_management:
    def add_audit(user_obj,action):
        audit = models.AuditLog(user_name=user_obj,action=action)
        audit.save()
    def get_audit():
        return models.AuditLog.objects.all()[10]
        
def index(request):
    template = loader.get_template('home/index.html')
    
    bikes_obj = vechiles.models.Bikes.objects.order_by('availability_status')[:5]
    cars_obj = vechiles.models.Cars.objects.order_by('availability_status')[:5]
    promotion = models.promotion.objects.filter(is_active=True).all()
    
    bikes ={}
    for bike in bikes_obj:
        images = vechiles.models.bikeimages.objects.filter(bike=bike).first()
        bikes[bike]= images
        
    cars = {} 
    for car in cars_obj:
        images = vechiles.models.carimages.objects.filter(car=car).first()
        cars[car] = images
        
    data = {
        'cars' :cars,
        'bikes' : bikes,
        'promotions' : promotion,
    }

    return HttpResponse(template.render(data,request))

def contact(request):
    template = loader.get_template('home/contact.html')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        number = request.POST.get('phone')
        message = request.POST.get('message')
        
        contact = models.contact(name=name,number=number,message=message)
        contact.save()

        messages.success(request,"we got your query.. ..  we will get back to you soon..")
        return redirect('contact')
        
    return HttpResponse(template.render(request=request))

#robots.txt seo
def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /private/",
        "Disallow: /default/admin/",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

def terms(request):
    template = loader.get_template('booking/terms.html')

    return HttpResponse(template.render(request=request))

def about(request):
    template = loader.get_template('home/about.html')
    
    return HttpResponse(template.render(request=request))

def car_booking(request,car_id):
    user = request.user
    car_obj = vechiles.models.Cars.objects.get(vechile_id=car_id)
    id = car_obj.vechile_id
    
    if not user.is_authenticated:
        messages.error(request, "login to book the car")
        return redirect('carbook',car_id=id)
    
    if car_obj.availability_status != 'Available':
        messages.error(request, "car is not available for booking")
        return redirect('carbook',car_id=id)
    
    if request.method == "POST":
        book_obj = vechiles.models.carBooking(user=user,vechile=car_obj,)
        book_obj.save()
        
        audit_management.add_audit(user,f'booked car {car_obj}')
        car_obj.availability_status = 'Rented'
        car_obj.save()
        
        messages.success(request, f"This booking confirmed for you @{user.username}")
        return redirect('carbook',car_id=id)

def carbooking(request,car_id):
    template = loader.get_template('booking/car.html')
    car_obj = vechiles.models.Cars.objects.get(vechile_id=car_id)
    image = vechiles.models.carimages.objects.filter(car=car_obj).first()
    
    data = {
        'car' : car_obj,
        'image' : image,
        'is_booked' : False,
    }
    
    user = request.user
    if user.is_authenticated:
        book_obj = vechiles.models.carBooking.objects.filter(user=user, vechile=car_obj, is_active=True).order_by('-booking_date').first()
        data['is_booked'] = book_obj.is_active if book_obj is not None else False
          
    return HttpResponse(template.render(data,request))

def bike_booking(request,bike_id):
    user = request.user
    bike_obj = vechiles.models.Bikes.objects.get(vechile_id=bike_id)
    id = bike_obj.vechile_id
    
    if not user.is_authenticated:
        messages.error(request, "Login to book the bike")
        return redirect('bikebook',bike_id=id)
    
    if bike_obj.availability_status != 'Available':
        messages.error(request, "This bike is not available for booking ")
        return redirect('bikebook',bike_id=id)
    
    if request.method == "POST":
        book_obj = vechiles.models.bikeBooking(user=user,vechile=bike_obj,)
        book_obj.save()
          
        audit_management.add_audit(user,f'booked bike {bike_obj}')    
        bike_obj.availability_status = 'Rented'
        bike_obj.save()
        
        messages.success(request, f"This booking confirmed for you @{user.username}")
        return redirect('bikebook',bike_id=id)

def bikebooking(request,bike_id):
    template = loader.get_template('booking/bike.html')
    bike_obj = vechiles.models.Bikes.objects.get(vechile_id=bike_id)
    image = vechiles.models.bikeimages.objects.filter(bike=bike_obj).first()
    
    data = {
        'bike' : bike_obj,
        'image' : image,
        'is_booked' : False,
    }
    
    user = request.user
    if user.is_authenticated:
        book_obj = vechiles.models.bikeBooking.objects.filter(user=user, vechile=bike_obj, is_active=True).order_by('-booking_date').first()
        data['is_booked'] = book_obj.is_active if book_obj is not None else False
           
    return HttpResponse(template.render(data,request))