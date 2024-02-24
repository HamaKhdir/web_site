from django.db import models
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User 

class UnitsSelect(models.TextChoices):
        LITER = 'Lt', _('لیتر')
        TON = 'Tn', _('تۆن')  

class Measures(models.Model):
     name = models.CharField(max_length=2,choices=UnitsSelect.choices)
     to_liter  = models.DecimalField(default=1,max_digits=10,decimal_places=2)
     def __str__(self):
        return self.name 
       
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
             
class Shifts(models.Model):
    name = models.CharField(max_length=15)
    start_work = models.TimeField(auto_now=False, auto_now_add=False)
    end_work = models.TimeField(auto_now=False, auto_now_add=False)
    def __str__(self):
        return self.name    

class Users(models.Model):
    u_id = models.PositiveIntegerField(primary_key=True,null=False,unique=True)
    user = models.CharField(max_length=100)   # should be checked with it's group before saved!
    password = models.CharField(max_length=200)
    shift = models.ForeignKey(Shifts,on_delete=models.CASCADE)  
    note = models.CharField(max_length=50)

    def __str__(self):
        return self.user

class Venders(models.Model):
    fullName = models.CharField(max_length=30,unique=True)
    address = models.CharField(max_length=50)
    tel = models.CharField(max_length=20)
   
    def __str__(self):
        return self.fullName
            
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

# @receiver(post_save, sender=User)
# def created_users(sender,instance,created,**kwargs):
#     if created:         
#         #print(instance.username)
#         # check the group before will saved the user.
#         # before we try to use this function, we should have a form and saved the group of user.
#         #print(instance.id)
#         # Users.objects.create(u_id=instace.id, user=instace.username)
    
class ReturnItem(models.Model):
    item = models.ForeignKey(Items,on_delete=models.CASCADE) 
    amount = models.PositiveBigIntegerField(default=0) 
    price = models.PositiveIntegerField(default=0) 
    shift = models.ForeignKey(Shifts,on_delete=models.CASCADE) 
    note = models.CharField(max_length=100)
    amount_money =  models.PositiveBigIntegerField(default=0)
    return_date = models.DateField()
    entry_date = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        self.buy_amount = self.amount * self.price        
        super().save(*args, **kwargs) 
    
class Counter(models.Model):
    item = models.ForeignKey(Items,on_delete=models.CASCADE)
    register = models.PositiveBigIntegerField(default=0)
    old_register = models.PositiveBigIntegerField(default=0)
    buy_amount =  models.PositiveBigIntegerField(default=0)
    buy_amount_money =  models.PositiveBigIntegerField(default=0)
    shift = models.ForeignKey(Shifts,on_delete=models.CASCADE)
    entry_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.old_register !=0:
            self.buy_amount = self.register - self.old_register
        else:
            self.buy_amount = 0
        self.buy_amount_money = self.buy_amount * self.item.sell_price         
        super().save(*args, **kwargs) 
    
    def __str__(self):
        return f"{self.item}, {self.register}"
    
class DailyExpenses(models.Model):
    subject = models.CharField(max_length=50) 
    amount = models.PositiveBigIntegerField(default=0)  
    shift = models.ForeignKey(Shifts,on_delete=models.CASCADE)
    expenses_date = models.DateField()
    note = models.CharField(max_length=100) 
    
class Customers(models.Model):
    fullName = models.CharField(max_length=30,unique=True)
    address = models.CharField(max_length=50)
    tel = models.CharField(max_length=20)

    def __str__(self):
        return self.fullName 
    
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
     is_counter = models.BooleanField(default=True)
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
          return f"{self.id}:{self.customer}, {self.item}, {self.amount}, {self.sell_unit}, {self.buy_price},{self.lost_amount},{self.clear_amount},{self.sell_date},{self.total_money},{self.paid_money},{self.loan_money},{self.note},{self.sell_price} "

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

class SellByCounters(models.Model):
     item = models.ForeignKey(Items,blank=True, null=True, on_delete=models.SET_NULL)
     amount = models.DecimalField(max_digits=10,decimal_places=2)
     sell_unit = models.CharField(max_length=2,choices=UnitsSelect.choices,default=UnitsSelect.LITER)
     buy_price = models.DecimalField(max_digits=10,decimal_places=0)
     sell_price = models.DecimalField(max_digits=10,decimal_places=0)
     total_money = models.DecimalField(default=0,max_digits=10,decimal_places=0)
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
          return f"{self.id}, {self.item}, {self.amount}, {self.sell_unit}, {self.buy_price},{self.sell_price} "

     def save(self, *args, **kwargs): 
          current_item =Items.objects.get(name=self.item)
          self.sell_unit = current_item.sell_unit
          self.buy_price = current_item.buy_price
          self.sell_price=current_item.sell_price
          self.total_money = self.amount * self.sell_price
          super().save(*args, **kwargs)           