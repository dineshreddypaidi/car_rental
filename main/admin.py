from django.contrib import admin
from . import models
# Register your models here.

class Admin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]

admin.site.register(models.AuditLog,Admin)
admin.site.register(models.promotion,Admin)
admin.site.register(models.contact,Admin)