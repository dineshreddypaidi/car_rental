from django.contrib import admin
from . import models

class vechileAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]

#admin.site.register(models., CarAdmin)#vechiles    
admin.site.register(models.Cars, vechileAdmin)
admin.site.register(models.Bikes, vechileAdmin)

#images
admin.site.register(models.carimages,vechileAdmin)
admin.site.register(models.bikeimages,vechileAdmin)

#booking
admin.site.register(models.carBooking, vechileAdmin)
admin.site.register(models.bikeBooking, vechileAdmin)

#reviews
admin.site.register(models.carReview, vechileAdmin)
admin.site.register(models.bikeReview, vechileAdmin)

#stats
admin.site.register(models.car_stats, vechileAdmin)
admin.site.register(models.bike_stats, vechileAdmin)