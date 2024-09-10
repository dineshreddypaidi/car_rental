from django.urls import path
from . import views
# Create your tests here.
urlpatterns = [
    path('cars/',views.cars_view,name="cars_view"),
    path('bikes/',views.bikes_view,name="bikes_view"),
    
    path('car/<str:car_id>',views.car_details,name="car_details"),
    path('bike/<str:bike_id>',views.bike_details,name="car_details"),
]
