from django.contrib import admin
from .models import Measures,Venders,Customers,Items,Store,Buy,Sell 

admin.site.register(Venders)
admin.site.register(Customers)
admin.site.register(Items)
admin.site.register(Store)
admin.site.register(Buy)
admin.site.register(Measures)
admin.site.register(Sell)
#admin.site.register(Shifts)