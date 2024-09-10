from django.urls import path
from . import views

urlpatterns = [
    path('',views.Index,name="index"),
    path('login/',views.Login,name='login'),
    path('register/',views.Register,name='register'),
    path('change_password',views.change_password,name="change_password"),
    path('logout/',views.Logout,name="logout"),
    #path('userr',views.userr)
    path('rentals/',views.my_rentals,name="my rentals"),
    #path('booking',views.booking,name="booking")
]