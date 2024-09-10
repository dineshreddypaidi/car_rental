from django.template import loader
from django.http import HttpResponse
from . import models
# Create your views here.
def cars_view(request):
    template = loader.get_template('vechiles/cars.html')
    
    brands = models.Cars.objects.values_list('brand', flat=True).distinct()
    availbility_status = models.Cars.objects.values_list('availability_status', flat=True).distinct()
    fuels =  models.Cars.objects.values_list('fuel_type', flat=True).distinct()
    years =  models.Cars.objects.values_list('year', flat=True).distinct()
    colors =  models.Cars.objects.values_list('color', flat=True).distinct()
    rents = [130,120,110,100,80,90]
    
    cars_obj = models.Cars.objects.filter(availability_status='Available').order_by('updated_at')[:12]
    cars = {}
    for car in cars_obj:
        image = models.carimages.objects.filter(car=car).first()
        cars[car] = image
        
    data = {
        #filters options
        'brands' : brands,
        'statuses' : availbility_status,
        'fuels' : fuels,
        'years' : years,
        'colors' : colors,
        'rents' : rents,
        
        'cars' : cars,  
    }
    if request.method == 'GET':
        brand = request.GET.get('brand')
        status = request.GET.get('status')
        fuel = request.GET.get('fuel')
        rent = request.GET.get('rent')
        year = request.GET.get('year')
        color = request.GET.get('color')
        
        filter_criteria = {}
        
        if brand:
            filter_criteria['brand'] = brand
        if status:
            filter_criteria['availability_status'] = status
        if fuel:
            filter_criteria['fuel_type'] = fuel
        if year:
            filter_criteria['year'] = year
        if color:
            filter_criteria['color'] = color
        if rent:
            try:
                rent = int(rent) 
                filter_criteria['rental_rate_per_hour__lt'] = rent
            except ValueError:
                pass 
            
        cars_obj = models.Cars.objects.filter(**filter_criteria)
        cars = {} 
        for car in cars_obj:
            image = models.carimages.objects.filter(car=car).first()
            cars[car] = image
        data['cars'] = cars
        
    return HttpResponse(template.render(data,request))
    
def bikes_view(request):
    template = loader.get_template('vechiles/bikes.html')
    
    brands = models.Bikes.objects.values_list('brand', flat=True).distinct()
    availbility_status = models.Bikes.objects.values_list('availability_status', flat=True).distinct()
    fuels =  models.Bikes.objects.values_list('fuel_type', flat=True).distinct()
    years =  models.Bikes.objects.values_list('year', flat=True).distinct()
    colors =  models.Bikes.objects.values_list('color', flat=True).distinct()
    rents = [130,120,110,100,80,90]
    
    bikes_obj = models.Bikes.objects.filter(availability_status='Available').order_by('-updated_at')[:12]
    bikes = {} 
    for bike in bikes_obj:
        images = models.bikeimages.objects.filter(bike=bike).first()
        bikes[bike] = images
        
    data = {
        #filters options
        'brands' : brands,
        'statuses' : availbility_status,
        'fuels' : fuels,
        'years' : years,
        'colors' : colors,
        'rents' : rents,
        
        'bikes' : bikes,  
    }
    if request.method == 'GET':
        brand = request.GET.get('brand')
        status = request.GET.get('status')
        fuel = request.GET.get('fuel')
        rent = request.GET.get('rent')
        year = request.GET.get('year')
        color = request.GET.get('color')
        
        filter_criteria = {}
        
        if brand:
            filter_criteria['brand'] = brand
        if status:
            filter_criteria['availability_status'] = status
        if fuel:
            filter_criteria['fuel_type'] = fuel
        if year:
            filter_criteria['year'] = year
        if color:
            filter_criteria['color'] = color
        if rent:
            try:
                rent = int(rent) 
                filter_criteria['rental_rate_per_hour__lt'] = rent
            except ValueError:
                pass
        
        bikes_obj = models.Bikes.objects.filter(**filter_criteria)
        bikes = {} 
        for bike in bikes_obj:
            images = models.bikeimages.objects.filter(bike=bike).first()
            bikes[bike] = images
        data['bikes'] = bikes
        
    return HttpResponse(template.render(data,request))

def car_details(request,car_id):
    template = loader.get_template('vechiles/car.html')
    user = request.user
    car_obj = models.Cars.objects.filter(vechile_id=car_id).get()
    images = models.carimages.objects.filter(car=car_obj).all()
    
    data = {
        'vechile' : car_obj,
        'images' : images,
        'is_booked' : False,
    }
    if user.is_authenticated:
        book_obj = models.carBooking.objects.filter(user=user, vechile=car_obj, is_active=True).order_by('-booking_date').first()
        data['is_booked'] = book_obj.is_active if book_obj is not None else False
        
    return HttpResponse(template.render(data,request))
    
def bike_details(request,bike_id):
    template = loader.get_template('vechiles/bike.html')
    user = request.user
    bike_obj = models.Bikes.objects.filter(vechile_id=bike_id).get()
    images = models.bikeimages.objects.filter(bike=bike_obj).all()
    
    data = {
        'vechile' : bike_obj,
        'images' : images,
        'is_booked' : False,
    }
    if user.is_authenticated:
        book_obj = models.bikeBooking.objects.filter(user=user, vechile=bike_obj, is_active=True).order_by('-booking_date').first()
        data['is_booked'] = book_obj.is_active if book_obj is not None else False
        
    return HttpResponse(template.render(data,request))    