from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('contact/',views.contact,name="contact"),
    path('about/',views.about,name="about"),
    path('robots.txt', views.robots_txt),

    path('terms',views.terms,name='terms'),
    path('book/car/<str:car_id>',views.carbooking,name="carbook"),
    path('booking/car/<str:car_id>',views.car_booking,name="car_booking"),
    
    path('book/bike/<str:bike_id>',views.bikebooking,name="bikebook"),
    path('booking/bike/<str:bike_id>',views.bike_booking,name="bike_booking"),    
]