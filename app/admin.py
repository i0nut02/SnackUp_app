from django.contrib import admin

from .models import *
# Register your models here.

admin.site.register(School)
admin.site.register(Classroom)
admin.site.register(Student)
admin.site.register(Company)
admin.site.register(Food)
admin.site.register(Category)
admin.site.register(Payment_Method)
admin.site.register(Order)
admin.site.register(Food_Order)
admin.site.register(Cart)