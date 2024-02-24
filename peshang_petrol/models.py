from django.db import models
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User 


# class UserProfile(models.Model):
#     user = models.OneToOneField(User,on_delete=models.CASCADE)
#     age = models.PositiveSmallIntegerField(default=0)
#     nickname = models.CharField(max_length=30)


class Shifts(models.Model):
    name = models.CharField(max_length=15)
     

class UnitsSelect(models.TextChoices):
        LITER = 'Lt', _('لیتر')
        TON = 'Tn', _('تۆن')  

class Measures(models.Model):
     name = models.CharField(max_length=2,choices=UnitsSelect.choices)
     to_liter  = models.DecimalField(default=1,max_digits=10,decimal_places=2)
     def __str__(self):
        return self.name  
     #get_name_display()
     
class Items(models.Model):
    name = models.CharField(max_length=20,unique=True)
    buy_unit = models.ForeignKey(Measures,on_delete=models.CASCADE)
    tank_size = models.DecimalField(max_digits=10,decimal_places=2)
    sell_unit = models.CharField(max_length=2,choices=UnitsSelect.choices,default=UnitsSelect.LITER)
    buy_price = models.DecimalField(default=0,max_digits=10,decimal_places=0)
    sell_price = models.DecimalField(default=0,max_digits=10,decimal_places=0)    
    warning_amount = models.PositiveSmallIntegerField(default=0)

    @property
    def convert_Lt_to_Ton(self):
        return self.tank_size / self.buy_unit.to_liter
    
    @property
    def convert_Ton_to_Lt(self):
        return self.tank_size * self.buy_unit.to_liter
    
    @property
    def convert_warning_amount_to_Ton(self):
        return self.warning_amount / self.buy_unit.to_liter
    
    @property
    def convert_warning_amount_to_Lt(self):
        return self.warning_amount * self.buy_unit.to_liter
        
    def __str__(self):
        return self.name 

class SellShift(models.Model):
    shift = models.ForeignKey(Shifts,on_delete=models.CASCADE)
    item = models.ForeignKey(Items,on_delete=models.CASCADE)
    user = models.CharField(max_length=30)

class Venders(models.Model):
    fullName = models.CharField(max_length=30,unique=True)
    address = models.CharField(max_length=50)
    tel = models.CharField(max_length=20)
   

    def __str__(self):
        return self.fullName
    
class Customers(models.Model):
    fullName = models.CharField(max_length=30,unique=True)
    temporary = models.BooleanField(default=False)
    address = models.CharField(max_length=50)
    tel = models.CharField(max_length=20)

    def __str__(self):
        return self.fullName    


class Store(models.Model):
    item = models.ForeignKey(Items,on_delete=models.CASCADE)
    amount = models.DecimalField(default=0,max_digits=10,decimal_places=2)

    @property
    def convert_Lt_to_Ton(self):
        measure = Measures.objects.get(item = self.item)
        return self.amount / measure.ton_to_liter
    
    @property
    def convert_Ton_to_Lt(self):
        measure = Measures.objects.get(item = self.item)
        return self.amount * measure.ton_to_liter
    
    def __str__(self):
        return f' amount: {self.amount}'   

class Buy(models.Model):
     vender = models.ForeignKey(Venders,on_delete=models.CASCADE)
     bill_no = models.PositiveSmallIntegerField(default=0)
     item = models.ForeignKey(Items,blank=True, null=True, on_delete=models.SET_NULL)
     amount = models.DecimalField(max_digits=10,decimal_places=2)
     buy_unit = models.CharField(max_length=2,choices=UnitsSelect.choices,default=UnitsSelect.LITER)
     buy_price = models.DecimalField(max_digits=10,decimal_places=0)
     sell_price = models.DecimalField(max_digits=10,decimal_places=0)
     lost_amount = models.DecimalField(default=0,max_digits=10,decimal_places=2)
     clear_amount = models.DecimalField(default=0,max_digits=10,decimal_places=2)
     buy_date = models.DateField()
     total_money = models.DecimalField(default=0,max_digits=10,decimal_places=0)
     paid_money = models.DecimalField(default=0,max_digits=10,decimal_places=0)
     loan_money = models.DecimalField(default=0,max_digits=10,decimal_places=0)
     last_account = models.DecimalField(default=0,max_digits=10,decimal_places=0)
     note = models.CharField(max_length=50)
     entry_date = models.DateTimeField(auto_now_add=True)
     #entry_user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)

     @property
     def convert_Lt_to_Ton(self):
        measure = Measures.objects.get(item = self.item)
        return self.amount / measure.ton_to_liter
     @property
     def convert_Ton_to_Lt(self):
        measure = Measures.objects.get(item = self.item)
        return self.amount * measure.ton_to_liter  
    
     def __str__(self):
          return f" {self.id}:{self.vender}, {self.item}, {self.amount}, {self.buy_unit}, {self.buy_price},{self.lost_amount},{self.clear_amount},{self.buy_date},{self.total_money},{self.paid_money},{self.loan_money},{self.note},,{self.sell_price} "

     def save(self, *args, **kwargs):
          self.clear_amount = self.amount - self.lost_amount  
          self.total_money = self.amount * self.buy_price
          self.loan_money = self.total_money - self.paid_money
          
          check_records = Buy.objects.filter(vender=self.vender).count()

          if check_records > 0 : 
              #latest_id = Buy.objects.latest('id').id
              sum_totals = Buy.objects.filter(vender=self.vender).aggregate(Sum("total_money"))
              sum_paids = Buy.objects.filter(vender=self.vender).aggregate(Sum("paid_money"))
              totals = sum_totals['total_money__sum']
              paids = sum_paids['paid_money__sum']

              self.last_account = (totals - paids) + self.total_money - self.paid_money               
          else:
              self.last_account = self.total_money - self.paid_money

          super().save(*args, **kwargs)


class Sell(models.Model):
     customer = models.ForeignKey(Customers,on_delete=models.CASCADE)
     item = models.ForeignKey(Items,blank=True, null=True, on_delete=models.SET_NULL)
     amount = models.DecimalField(max_digits=10,decimal_places=2)
     sell_unit = models.CharField(max_length=2,choices=UnitsSelect.choices,default=UnitsSelect.LITER)
     buy_price = models.DecimalField(max_digits=10,decimal_places=0)
     sell_price = models.DecimalField(max_digits=10,decimal_places=0)
     lost_amount = models.DecimalField(default=0,max_digits=10,decimal_places=2)
     clear_amount = models.DecimalField(default=0,max_digits=10,decimal_places=2)
     sell_date = models.DateField()
     total_money = models.DecimalField(default=0,max_digits=10,decimal_places=0)
     paid_money = models.DecimalField(default=0,max_digits=10,decimal_places=0)
     loan_money = models.DecimalField(default=0,max_digits=10,decimal_places=0)
     last_account = models.DecimalField(default=0,max_digits=10,decimal_places=0)
     note = models.CharField(max_length=50)
     entry_date = models.DateTimeField(auto_now_add=True)
     #entry_user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)

     @property
     def convert_Lt_to_Ton(self):
        measure = Measures.objects.get(item = self.item)
        return self.amount / measure.ton_to_liter
     @property
     def convert_Ton_to_Lt(self):
        measure = Measures.objects.get(item = self.item)
        return self.amount * measure.ton_to_liter  
    
     def __str__(self):
          return f"{self.id}:{self.customer}, {self.item}, {self.amount}, {self.sell_unit}, {self.buy_price},{self.lost_amount},{self.clear_amount},{self.sell_date},{self.total_money},{self.paid_money},{self.loan_money},{self.note},,{self.sell_price} "

     def save(self, *args, **kwargs):
          self.clear_amount = self.amount # - self.lost_amount  
          self.total_money = self.amount * self.sell_price
          self.loan_money = self.total_money - self.paid_money
          
          check_records = Sell.objects.filter(customer=self.customer).count()

          if check_records > 0 : 
              #latest_id = Buy.objects.latest('id').id
              sum_totals = Sell.objects.filter(customer=self.customer).aggregate(Sum("total_money"))
              sum_paids = Sell.objects.filter(customer=self.customer).aggregate(Sum("paid_money"))
              totals = sum_totals['total_money__sum']
              paids = sum_paids['paid_money__sum']

              self.last_account = (totals - paids) + self.total_money - self.paid_money               
          else:
              self.last_account = self.total_money - self.paid_money

          super().save(*args, **kwargs)          