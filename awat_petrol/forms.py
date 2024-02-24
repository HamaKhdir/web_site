from django import forms
from .models import *
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
 

class UserForm(UserCreationForm):
    class Meta:
        model= User
        fields=['username','password1','password2']
        labels={'username':'ناوی بەکارهێنەر','password1':'پاسۆرد','password2':'پاسۆرد دووبارە'}

        widgets={'username':forms.TextInput(attrs={'class':'form-control','placeholder':'ناوی بەکارهێنەر'}),
                 'password1':forms.PasswordInput(attrs={'class':'form-control','placeholder':'پاسۆرد'}),
                 'password2':forms.PasswordInput(attrs={'class':'form-control','placeholder':'پاسۆرد دووبارە'}),
                 }

class DateInput(forms.DateInput):
    input_type='date'

class MeasureForm(forms.ModelForm):
    class Meta:
        model= Measures
        fields=['name','to_liter']
        labels={'name':'ناوی یەکە','to_liter':'بڕ بە لیتر'}

        widgets={'name':forms.Select(attrs={'class':'form-select','dir':'ltr'}),
                 'to_liter':forms.NumberInput(attrs={'class':'form-control','min':'0'}),
                 }
        
class ItemForm(forms.ModelForm):
    
    class Meta:
        model= Items
        #rdering = ['-id']
        fields=['name','buy_unit','tank_size','sell_unit','buy_price','sell_price','warning_amount']
        labels={'name':'ناوی ماددە','buy_unit':'یەکەی کڕین','tank_size':'قەبارەی تانک','sell_unit':'یەکەی فرۆشتن','buy_price':'نرخی کڕین',
                'sell_price':'نرخی فرۆشتن یەک لیتر','warning_amount':'بڕی ئاگادارکردنەوە'}

        widgets={'name':forms.TextInput(attrs={'class':'form-control'}),
                 'buy_unit':forms.Select(attrs={'class':'form-select','id':'buy_unit','dir':'ltr'}),
                 'tank_size':forms.NumberInput(attrs={'class':'form-control','id':'tank_size','min':'0'}),
                 'sell_unit':forms.Select(attrs={'class':'form-select','id':'sell_unit','dir':'ltr'}),
                 'buy_price':forms.NumberInput(attrs={'class':'form-control','min':'0','id':'buy_price'}),
                 'sell_price':forms.NumberInput(attrs={'class':'form-control','min':'0','id':'sell_price'}),
                 'warning_amount':forms.NumberInput(attrs={'class':'form-control','id':'warning_amount'})
                 }         

class ShiftForm(forms.ModelForm):
    class Meta:
        model= Shifts
        fields=['name','start_work','end_work']
        labels={'name':'ناوی شەفت','start_work':'کاتی دەست بەکاربوون','end_work':'کاتی دەست هەڵگرتنش'}

        widgets={'name':forms.TextInput(attrs={'class':'form-control'}),
                 'start_work':forms.TimeInput(attrs={'type': 'time','class':'form-control'}),
                 'end_work':forms.TimeInput(attrs={'type': 'time','class':'form-control'}),
                 }
                  
class ReturnItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['return_date'].initial = datetime.now()

    note = forms.CharField(label='تێبینی',required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model= ReturnItem
        fields=['item','amount','price','shift','return_date']
        labels={'item':'ناوی ماددە','amount':'بڕی گەڕاوە بە لیتر','price':'نرخی یەک لیتر','shift':'شەفت','return_date':'ڕۆژی گەڕانەوە'}

        widgets={'item':forms.Select(attrs={'class':'form-select','dir':'ltr'}),
                    'amount':forms.NumberInput(attrs={'class':'form-control','min':'0'}),
                    'price':forms.NumberInput(attrs={'class':'form-control','min':'0'}),
                    'shift':forms.Select(attrs={'class':'form-select','dir':'ltr'}),
                    'return_date':DateInput(attrs={'autocomplete':'off','class':'form-control'}),
                }  
        
class CounterForm(forms.ModelForm):
    class Meta:
        model= Counter
        fields=['item','register','shift']
        labels={'item':'ناوی ماددە','register':'ژمارەی سەر عدادەکان','shift':'شەفت'}

        widgets={'item':forms.Select(attrs={'class':'form-select','dir':'ltr'}),
                    'register':forms.NumberInput(attrs={'class':'form-control','min':'0'}),
                    'shift':forms.Select(attrs={'class':'form-select','dir':'ltr'}),
                }       
            
            
class DailyExpensesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['expenses_date'].initial = datetime.now()

    note = forms.CharField(label='تێبینی',required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model= DailyExpenses
        fields=['subject','amount','shift','expenses_date']
        labels={'subject':'جۆری خەرجی','amount':'بڕی پارە','shift':'شەفت','expenses_date':'ڕۆژی خەرجی'}

        widgets={'subject':forms.TextInput(attrs={'class':'form-control'}),
                 'amount':forms.NumberInput(attrs={'class':'form-control','min':'0'}),
                 'shift':forms.Select(attrs={'class':'form-select','dir':'ltr'}),
                 'expenses_date':DateInput(attrs={'autocomplete':'off','class':'form-control'}),
                }            

class VenderForm(forms.ModelForm):
    
    class Meta:
        model= Venders
        fields=['fullName','address','tel']
        labels={'fullName':'ناوی سیانی','address':'ناونیشان','tel':'تەلەفۆن'}

        widgets={'fullName':forms.TextInput(attrs={'class':'form-control'}),
                 'address':forms.TextInput(attrs={'class':'form-control'}),
                 'tel':forms.TextInput(attrs={'class':'form-control'}),
                 }
        
class CustomerForm(forms.ModelForm):
    
    class Meta:
        model= Customers
        fields=['fullName','address','tel']
        labels={'fullName':'ناوی سیانی','address':'ناونیشان','tel':'تەلەفۆن'}

        widgets={'fullName':forms.TextInput(attrs={'class':'form-control'}),
                 'address':forms.TextInput(attrs={'class':'form-control'}),
                 'tel':forms.TextInput(attrs={'class':'form-control'}),
                 }    
            
class ToVenderEnterMoneyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['buy_date'].initial = datetime.now()
    note = forms.CharField(label='تێبینی',required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model= Buy
        fields=['paid_money','buy_date','note']
        labels={'paid_money':'بڕی واصڵ','buy_date':'بەروار'}

        widgets={ 
                'paid_money':forms.NumberInput(attrs={'class':'form-control','min':'0'}),
                'buy_date':DateInput(attrs={'autocomplete':'off','class':'form-control','min':'0'}),
                }   
class ToCustomerEnterMoneyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sell_date'].initial = datetime.now()
    note = forms.CharField(label='تێبینی',required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model= Sell
        fields=['paid_money','sell_date','note']
        labels={'paid_money':'بڕی واصڵ','sell_date':'بەروار'}

        widgets={ 
                'paid_money':forms.NumberInput(attrs={'class':'form-control','min':'0'}),
                'sell_date':DateInput(attrs={'autocomplete':'off','class':'form-control','min':'0'}),
                }           

class BuyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['buy_date'].initial = datetime.now()
    note = forms.CharField(label='تێبینی',required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model= Buy
        fields=['item','amount','buy_price','total_money','paid_money','buy_date','bill_no','note']
        labels={'item':'ماددە','amount':'بڕ بە ( یەکەی کڕین )','lost_amount':'بڕی بەفیڕۆچوو','buy_price':'نرخی یەک ( یەکەی کڕین )  ','buy_date':'بەرواری کڕین','bill_no':'رقم وصل','paid_money':'پارەی واسڵ','total_money':'کۆی گشتی پارە'}
 
        widgets={'item':forms.Select(attrs={'class':'form-select','id':'item','dir':'ltr'}),
                 'amount':forms.NumberInput(attrs={'class':'form-control','id':'amount','min':'0'}),
                 #'lost_amount':forms.NumberInput(attrs={'class':'form-control','type':'hidden','id':'lost_amount','min':'0'}),
                 #'buy_unit':forms.Select(attrs={'class':'form-select','type':'hidden','id':'buy_unit'}),
                 'buy_price':forms.NumberInput(attrs={'class':'form-control','id':'buy_price','requered':'requered','min':'0'}),
                 'bill_no':forms.NumberInput(attrs={'class':'form-control','id':'bill_no','min':'0'}),
                 'buy_date':DateInput(attrs={'autocomplete':'off','class':'form-control','min':'0'}),
                 'paid_money':forms.NumberInput(attrs={'class':'form-control','min':'0'}),
                 'total_money':forms.NumberInput(attrs={'class':'form-control','id':'total_money','min':'0','readonly':'readonly'}),
                 }   

class BuyToUpdateRecordForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['buy_date'].initial = datetime.now()
    note = forms.CharField(label='تێبینی',required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model= Buy
        fields=['item','amount','buy_price','lost_amount','total_money','paid_money','buy_date','bill_no','note']
        labels={'item':'ماددە','amount':'بڕ بە ( یەکەی کڕین )','lost_amount':'بڕی بەفیڕۆچوو','buy_price':'نرخی یەک ( یەکەی کڕین )  ','buy_date':'بەرواری کڕین','bill_no':'رقم وصل','paid_money':'پارەی واسڵ','total_money':'کۆی گشتی پارە'}
 
        widgets={'item':forms.HiddenInput(attrs={'class':'form-select','id':'item'}),
                 'amount':forms.NumberInput(attrs={'class':'form-control','id':'amount','min':'0'}),
                 'lost_amount':forms.NumberInput(attrs={'class':'form-control','type':'hidden','id':'lost_amount','min':'0'}),
                 #'buy_unit':forms.Select(attrs={'class':'form-select','type':'hidden','id':'buy_unit'}),
                 'buy_price':forms.NumberInput(attrs={'class':'form-control','id':'buy_price','requered':'requered','min':'0'}),
                 'bill_no':forms.NumberInput(attrs={'class':'form-control','id':'bill_no','min':'0'}),
                 'buy_date':DateInput(attrs={'autocomplete':'off','class':'form-control','min':'0'}),
                 'paid_money':forms.NumberInput(attrs={'class':'form-control','min':'0'}),
                 'total_money':forms.NumberInput(attrs={'class':'form-control','id':'total_money','min':'0','readonly':'readonly'}),
                 }  

class StoreForm(forms.ModelForm):
    class Meta:
        model= Store
        fields=['amount']
        labels={'amount':'بڕ بە لیتر'}

        widgets={ 
                 'amount':forms.NumberInput(attrs={'class':'form-control','min':'0.0'}),
                }                     

class SellForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sell_date'].initial = datetime.now()
    note = forms.CharField(label='تێبینی',required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model= Sell
        fields=['item','amount','lost_amount','sell_price','total_money','paid_money','sell_date','note']
        labels={'item':'ماددە','amount':'بڕ بە ( یەکەی فرۆشتن )','lost_amount':'بڕی بە فیڕۆچوو','sell_price':'نرخی یەک ( یەکەی فرۆشتن )  ','total_money':'کۆی گشتی پارە','paid_money':'پارەی واسڵ','sell_date':'بەرواری فرۆشتن'}
 
        widgets={'item':forms.Select(attrs={'class':'form-select','id':'item','dir':'ltr'}),
                 'amount':forms.NumberInput(attrs={'class':'form-control','id':'amount','min':'0'}),
                 'lost_amount':forms.NumberInput(attrs={'class':'form-control','id':'lost_amount','min':'0'}),
                 'sell_price':forms.NumberInput(attrs={'class':'form-control','id':'sell_price','min':'0','readonly':'readonly'}),
                 'sell_date':DateInput(attrs={'autocomplete':'off','class':'form-control'}),
                 'paid_money':forms.NumberInput(attrs={'class':'form-control','min':'0'}),
                 'total_money':forms.NumberInput(attrs={'class':'form-control','id':'total_money','min':'0','readonly':'readonly'}),
                 } 

class SellTemporaryCustomerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sell_date'].initial = datetime.now()
    note = forms.CharField(label='تێبینی',required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model= Sell
        fields=['item','amount','lost_amount','sell_price','total_money','sell_date','note']
        labels={'item':'ماددە','amount':'بڕ بە ( یەکەی فرۆشتن )','lost_amount':'بڕی بە فیڕۆچوو','sell_price':'نرخی یەک ( یەکەی فرۆشتن )  ','total_money':'کۆی گشتی پارە','sell_date':'بەرواری فرۆشتن'}
 
        widgets={'item':forms.Select(attrs={'class':'form-select','id':'item','dir':'ltr'}),
                 'amount':forms.NumberInput(attrs={'class':'form-control','id':'amount','min':'0'}),
                 'lost_amount':forms.NumberInput(attrs={'class':'form-control','id':'lost_amount','min':'0'}),
                 'sell_price':forms.NumberInput(attrs={'class':'form-control','id':'sell_price','min':'0','readonly':'readonly'}),
                 'sell_date':DateInput(attrs={'autocomplete':'off','class':'form-control','min':'0'}),
                 #'paid_money':forms.NumberInput(attrs={'class':'form-control','id':'paid_money','min':'0'}),
                 'total_money':forms.NumberInput(attrs={'class':'form-control','id':'total_money','min':'0','readonly':'readonly'}),
                 }   

class SellToUpdateRecordForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sell_date'].initial = datetime.now()
    note = forms.CharField(label='تێبینی',required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model= Sell
        fields=['item','amount','lost_amount','sell_price','total_money','paid_money','sell_date','note']
        labels={'item':'ماددە','amount':'بڕ بە ( یەکەی کڕین )','lost_amount':'بڕی بەفیڕۆچوو','sell_price':'نرخی فرۆشتن','sell_date':'بەرواری کڕین','paid_money':'پارەی واسڵ','total_money':'کۆی گشتی پارە'}
 
        widgets={'item':forms.HiddenInput(attrs={'class':'form-select','id':'item'}),
                 'amount':forms.NumberInput(attrs={'class':'form-control','id':'amount','min':'0'}),
                 'lost_amount':forms.NumberInput(attrs={'class':'form-control','id':'lost_amount','min':'0'}),
                 'sell_price':forms.NumberInput(attrs={'class':'form-control','id':'sell_price','min':'0','readonly':'readonly'}),
                 'sell_date':DateInput(attrs={'autocomplete':'off','class':'form-control','min':'0'}),
                 'paid_money':forms.NumberInput(attrs={'class':'form-control','min':'0'}),
                 'total_money':forms.NumberInput(attrs={'class':'form-control','id':'total_money','min':'0','readonly':'readonly'}),
                 }                      