from django.contrib import admin
from .models import Cargo, CargoImage, Invoice, Quotation

# Register your models here.
admin.site.register(Cargo)
admin.site.register(CargoImage)
admin.site.register(Invoice)
admin.site.register(Quotation)