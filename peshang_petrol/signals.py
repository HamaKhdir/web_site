from .models import Store,Items,Measures,Buy,Sell 
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver




@receiver(post_save,sender=Items)
def when_create_item(sender,instance,created,**kwargs):
    if created:
        Store.objects.create(item=instance)

@receiver(post_save,sender=Buy)  
def when_create_buy(sender,instance,created,**kwargs):
    if created:
        
        if instance.item != None:
            clear_amount = instance.clear_amount
            store = Store.objects.get(item=instance.item.id)
            measure = Measures.objects.get(name=instance.item.buy_unit)
           
            if store :
                clear_amount = clear_amount * measure.to_liter
                store.amount += clear_amount
                store.save() 

@receiver(post_save,sender=Sell)  
def when_create_sell(sender,instance,created,**kwargs):
    if created:
        if instance.item != None:
            clear_amount = instance.clear_amount
            lost_amount = instance.lost_amount
            store = Store.objects.get(item=instance.item.id)
            measure = Measures.objects.get(name=instance.item.sell_unit)
           
            if store :
                clear_amount = clear_amount * measure.to_liter
                amt=clear_amount + lost_amount
                store.amount -= amt
                store.save()    
               
        



              
