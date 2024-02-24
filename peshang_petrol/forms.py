from django import forms
from .models import *
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CreatUserForm(UserCreationForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}))
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm Password'}))
    class Meta:
        model = User
        fields = ['username','email','password1','password2']



class DateInput(forms.DateInput):
    input_type='date'

class MeasureForm(forms.ModelForm):
    class Meta:
        model= Measures
        fields=['name','to_liter']
        labels={'name':'ناوی یەکە','to_liter':'بڕ بە لیتر'}

        widgets={'name':forms.Select(attrs={'class':'form-select'}),
                 'to_liter':forms.NumberInput(attrs={'class':'form-control','min':'0'}),
                 }

class ItemForm(forms.ModelForm):
    
    class Meta:
        model= Items
        fields=['name','buy_unit','tank_size','sell_unit','buy_price','sell_price','warning_amount']
        labels={'name':'ناوی ماددە','buy_unit':'یەکەی کڕین','tank_size':'قەبارەی تانک','sell_unit':'یەکەی فرۆشتن','buy_price':'نرخی کڕین',
                'sell_price':'نرخی فرۆشتن یەک لیتر','warning_amount':'بڕی ئاگادارکردنەوە'}

        widgets={'name':forms.TextInput(attrs={'class':'form-control'}),
                 'buy_unit':forms.Select(attrs={'class':'form-select','id':'buy_unit'}),
                 'tank_size':forms.NumberInput(attrs={'class':'form-control','id':'tank_size','min':'0'}),
                 'sell_unit':forms.Select(attrs={'class':'form-select','id':'sell_unit'}),
                 'buy_price':forms.NumberInput(attrs={'class':'form-control','min':'0','id':'buy_price'}),
                 'sell_price':forms.NumberInput(attrs={'class':'form-control','min':'0','id':'sell_price'}),
                 'warning_amount':forms.NumberInput(attrs={'class':'form-control','id':'warning_amount'})
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
        fields=['fullName','address','tel','temporary']
        labels={'fullName':'ناوی سیانی','address':'ناونیشان','tel':'تەلەفۆن','temporary':'موشتەری کاتی'}

        widgets={'fullName':forms.TextInput(attrs={'class':'form-control'}),
                 'address':forms.TextInput(attrs={'class':'form-control'}),
                 'tel':forms.TextInput(attrs={'class':'form-control'}),
                 'temporary' : forms.CheckboxInput(attrs={'class': 'form-check-input mt-0'})
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
 
        widgets={'item':forms.Select(attrs={'class':'form-select','id':'item'}),
                 'amount':forms.NumberInput(attrs={'class':'form-control','id':'amount','min':'0'}),
                 #'lost_amount':forms.NumberInput(attrs={'class':'form-control','type':'hidden','id':'lost_amount','min':'0'}),
                 #'buy_unit':forms.Select(attrs={'class':'form-select','type':'hidden','id':'buy_unit'}),
                 'buy_price':forms.NumberInput(attrs={'class':'form-control','id':'buy_price','requered':'requered','min':'0'}),
                 'bill_no':forms.NumberInput(attrs={'class':'form-control','id':'bill_no','min':'0'}),
                 'buy_date':DateInput(attrs={'autocomplete':'off','class':'form-control','min':'0'}),
                 'paid_money':forms.NumberInput(attrs={'class':'form-control','min':'0'}),
                 'total_money':forms.NumberInput(attrs={'class':'form-control','id':'total_money','min':'0','readonly':'readonly'}),
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

class SellForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sell_date'].initial = datetime.now()
    note = forms.CharField(label='تێبینی',required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model= Sell
        fields=['item','amount','lost_amount','sell_price','total_money','paid_money','sell_date','note']
        labels={'item':'ماددە','amount':'بڕ بە ( یەکەی فرۆشتن )','lost_amount':'بڕی بە فیڕۆچوو','sell_price':'نرخی یەک ( یەکەی فرۆشتن )  ','total_money':'کۆی گشتی پارە','paid_money':'پارەی واسڵ','sell_date':'بەرواری فرۆشتن'}
 
        widgets={'item':forms.Select(attrs={'class':'form-select','id':'item'}),
                 'amount':forms.NumberInput(attrs={'class':'form-control','id':'amount','min':'0'}),
                 'lost_amount':forms.NumberInput(attrs={'class':'form-control','id':'lost_amount','min':'0'}),
                 'sell_price':forms.NumberInput(attrs={'class':'form-control','id':'sell_price','min':'0','readonly':'readonly'}),
                 'sell_date':DateInput(attrs={'autocomplete':'off','class':'form-control'}),
                 'paid_money':forms.NumberInput(attrs={'class':'form-control','min':'0'}),
                 'total_money':forms.NumberInput(attrs={'class':'form-control','id':'total_money','min':'0','readonly':'readonly'}),
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