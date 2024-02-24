from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import Group,User
from .models import *
from django.views.generic import TemplateView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import *
from django.http import JsonResponse
import json 
import copy as copy_old_value
import csv
import datetime
from django.utils.timezone import localtime, now
from django.db.models import Max
from django.core.serializers.json import DjangoJSONEncoder

# my_group = Group.objects.get(name='my_group_name') 
# my_group.user_set.add(your_user)
RECORD_PER_PAGE=10
def index(request): 
    venders = Venders.objects.all()  
    #customers = Customers.objects.all().exclude(temporary=True)
    customers = Customers.objects.all()
    return render(request,'awat_petrol/index.html',{'venders':venders, 'customers':customers})
#----------- vender part  
#@login_required(login_url='awat_petrol:login')
#@allowed_users(allowed_roles=['awat_admin'])  
def viewVenders(req):
    vendersd = Venders.objects.all().order_by('-id')
    record_per_page = RECORD_PER_PAGE
    p=Paginator(vendersd,record_per_page)
    page = req.GET.get('page')
    venders = p.get_page(page) 
    pagination = True
    return render(req,'awat_petrol/view_venders.html',{'venders':venders,'pagination':pagination})

#@login_required(login_url='awat_petrol:login')
#@allowed_users(allowed_roles=['awat_admin']) 
def getVender(req,id):
    vender = Venders.objects.get(pk=id)
    return HttpResponseRedirect(reverse('awat_petrol:view-venders'))
#@login_required(login_url='awat_petrol:login')
#@allowed_users(allowed_roles=['awat_admin']) 
def addVender(req):
    if req.method=='POST':
        form=VenderForm(req.POST)
        if form.is_valid():
            fullname = form.cleaned_data['fullName']
            address = form.cleaned_data['address']
            telephone = form.cleaned_data['tel']
 
            new_vender = Venders(fullName=fullname, address=address,tel=telephone)
            new_vender.save()
            return render(req,'awat_petrol/add_vender.html',{'form':VenderForm(),'success':True})
    else:
        form=VenderForm()
    return render(req,'awat_petrol/add_vender.html',{'form':VenderForm()})    

#@login_required(login_url='awat_petrol:login')
#@allowed_users(allowed_roles=['awat_admin']) 
def editVender(request,id):
    if request.method=='POST':
        vender = Venders.objects.get(pk=id)
        form = VenderForm(request.POST,instance=vender)
        if form.is_valid():
            form.save()
            return render(request,'awat_petrol/edit_vender.html',{'form':form,'success':True})
    else:
        vender=Venders.objects.get(pk=id)
        form = VenderForm(instance=vender)
    return render(request,'awat_petrol/edit_vender.html',{'form':form})    

#@login_required(login_url='awat_petrol:login')
#@allowed_users(allowed_roles=['awat_admin']) 
def deleteVender(req,id):
    if req.method == 'POST':
        vender = Venders.objects.get(pk=id)
        vender.delete()
       
    return HttpResponseRedirect(reverse('awat_petrol:view-venders'))
def venderAccounts(request,id):
    vender = Venders.objects.get(pk=id)
    buy_records = Buy.objects.filter(vender=vender).order_by('-id')
    
    record_per_page = RECORD_PER_PAGE
    p=Paginator(buy_records,record_per_page)
    page = request.GET.get('page')
    records = p.get_page(page) 
    pagination = True

    if request.method == "POST":
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        records=buy_records.filter(buy_date__range=(start_date, end_date)).order_by('-id') 
        pagination = False

    return render(request, "awat_petrol/vender_accounts.html",{'records':records,'pagination':pagination,'vender':vender})

#@login_required(login_url='awat_petrol:login')
#@allowed_users(allowed_roles=['awat_admin']) 
def printVenderAccount(request,id):
    record = Buy.objects.get(pk=id)
    old_loan = record.last_account - (record.total_money - record.paid_money)
    return render(request,'awat_petrol/print_vender_account.html',{'record':record,'old_loan':old_loan})

#@login_required(login_url='awat_petrol:login')
#@allowed_users(allowed_roles=['awat_admin']) 
def ToVenderEnterMoney(request,id):
    vender = Venders.objects.get(pk=id)
    last_account = 0
    try:
        vender_records = Buy.objects.filter(vender=vender)
        last_account = vender_records.latest('id').last_account
        print(last_account)
    except Buy.DoesNotExist:
        pass
    if request.method == 'POST':
        form = ToVenderEnterMoneyForm(request.POST)
        if form.is_valid():
            paid_money=form.cleaned_data['paid_money']
            buy_date=form.cleaned_data['buy_date']
            note=form.cleaned_data['note']
            if last_account==0:
                messages.info(request, "هیچ بڕە پارەیەکی قەرز نیە!")
                #return render(request,'to_vender_enter_money.html',{'form':ToVenderEnterMoneyForm(),'vender':vender})
                return HttpResponseRedirect(reverse('awat_petrol:to-vender-enter-money', kwargs={'id':id}))   
            if paid_money > last_account:
                messages.info(request, "ئەم بڕە زیاترە لە قەرزەکە!")
                #return render(request,'to_vender_enter_money.html',{'form':ToVenderEnterMoneyForm(),'vender':vender})   
                return HttpResponseRedirect(reverse('awat_petrol:to-vender-enter-money', kwargs={'id':id}))                             
            if paid_money==0 or paid_money=="":
                messages.info(request, "تکایە بڕی پارەی واسڵکراو بنوسە!")
                return HttpResponseRedirect(reverse('awat_petrol:to-vender-enter-money', kwargs={'id':id})) 
                #return render(request,'awat_petrol/to_vender_enter_money.html',{'form':ToVenderEnterMoneyForm(),'vender':vender})             

            # check_records = Buy.objects.filter(vender=vender).count()
            # print(check_records)
            # last_account = 0    
            # if check_records > 1:
            #     latest_id = Buy.objects.latest('id').id
            #     sum_totals = Buy.objects.filter(id__lt=latest_id,vender=vender).aggregate(Sum("total_money"))
            #     sum_paids = Buy.objects.filter(id__lt=latest_id,vender=vender).aggregate(Sum("paid_money"))
            #     totals = sum_totals['total_money__sum']
            #     paids = sum_paids['paid_money__sum']

            #     last_account = (totals - paids) + 0 - paid_money               
            # else:
            #     last_account = 0 - paid_money            
            
            new_Item = Buy(vender=vender, bill_no=0, item=None, amount=0, buy_unit='Lt', buy_price=0, sell_price=0, buy_date=buy_date, paid_money=paid_money,note=note)#,entry_user=request.user
            new_Item.save()
            return render(request,'awat_petrol/to_vender_enter_money.html',{'form':ToVenderEnterMoneyForm(),'success':True,'vender':vender})
    else:
        form=ToVenderEnterMoneyForm()
    return render(request,'awat_petrol/to_vender_enter_money.html',{'form':ToVenderEnterMoneyForm(),'vender':vender}) 
 
#------------Customer Part
#@login_required(login_url='awat_petrol:login')
#@allowed_users(allowed_roles=['awat_admin']) 
def viewCustomers(req):
    customersd = Customers.objects.all().order_by('-id')
    record_per_page = RECORD_PER_PAGE
    p=Paginator(customersd,record_per_page)
    page = req.GET.get('page')
    customers = p.get_page(page) 
    pagination = True
    return render(req,'awat_petrol/view-customers.html',{'customers':customers,'pagination':pagination})

#@login_required(login_url='awat_petrol:login')
#@allowed_users(allowed_roles=['awat_admin']) 
def getCustomer(req,id):
    customer = Customers.objects.get(pk=id)
    return HttpResponseRedirect(reverse('awat_petrol:view-customers'))

#@login_required(login_url='awat_petrol:login')
#@allowed_users(allowed_roles=['awat_admin']) 
def addCustomer(req):
    if req.method=='POST':
        form=CustomerForm(req.POST)
        if form.is_valid():
            fullname = form.cleaned_data['fullName']
            address = form.cleaned_data['address']
            telephone = form.cleaned_data['tel']
             

            new_customer = Customers(fullName=fullname, address=address,tel=telephone)
            new_customer.save()
            return render(req,'awat_petrol/add_customer.html',{'form':CustomerForm(),'success':True})
    else:
        form=CustomerForm()
    return render(req,'awat_petrol/add_customer.html',{'form':CustomerForm()})    

#@login_required(login_url='awat_petrol:login')
#@allowed_users(allowed_roles=['awat_admin']) 
def editCustomer(request,id):
    if request.method=='POST':
        customer = Customers.objects.get(pk=id)
        form = CustomerForm(request.POST,instance=customer)
        if form.is_valid():                
            form.save()
            return render(request,'awat_petrol/edit_customer.html',{'form':form,'success':True})
    else:
        customer=Customers.objects.get(pk=id)
        form = CustomerForm(instance=customer)
    return render(request,'awat_petrol/edit_customer.html',{'form':form})    

#@login_required(login_url='awat_petrol:login')
#@allowed_users(allowed_roles=['awat_admin']) 
def deleteCustomer(req,id):
    if req.method == 'POST':
        customer = Customers.objects.get(pk=id)
        customer.delete()  
    return HttpResponseRedirect(reverse('awat_petrol:view-customers'))
#------------Store Part
def viewStore(request):
    datad=Store.objects.all().order_by('-id')
    record_per_page = RECORD_PER_PAGE
    p=Paginator(datad,record_per_page)
    page = request.GET.get('page')
    data = p.get_page(page) 
    pagination = True
    return render(request,'awat_petrol/view_store.html',{'data':data,'pagination':pagination})

def editStore(request,id):
    item = Store.objects.get(pk=id)
    if request.method=='POST':
        form = StoreForm(request.POST,instance=item)
        if form.is_valid():
            form.save()
            return render(request,'awat_petrol/edit_store.html',{'form':form,'name':item.item.name,'success':True})
    else:
        form = StoreForm(instance=item)
    return render(request,'awat_petrol/edit_store.html',{'form':form,'name':item.item.name})
#------------User Part
def viewUsers(req):
    users = User.objects.filter(groups__name='awat_user')
    uss = []
    for us in users:
        try:
            u = Users.objects.get(pk = us.id)
            if u:
               uss.append(u)
                
        except Users.DoesNotExist:
            pass    
       
    return render(req,'awat_petrol/view_users.html',{'users':uss})

def addUser(request):
    try:
       shifts=Shifts.objects.all()
    except Shifts.DoesNotExist:
        pass   
    if request.method =='POST':
        uname = request.POST.get('username')
        upass = request.POST.get('password1')
        cpass = request.POST.get('password2')
        shift_id = request.POST.get('shift')
        note = request.POST.get('note')                
        shift=Shifts.objects.get(pk=shift_id)  

        if cpass == upass:
            try:
                user = User.objects.create_user(username=uname,password=upass)
                group = Group.objects.get(name='awat_user') 
                user.groups.add(group) 
                Users.objects.create(u_id=user.id,password=upass,shift=shift,user=user.username,note=note)
                return render(request,'awat_petrol/add_user.html',{'shifts':shifts,'success':True})
            except:
                messages.info(request,'تکایە، زانیاری دروست بنوسە!') 
                return render(request,'awat_petrol/add_user.html',{'shifts':shifts})

        #return redirect('login')
        else:
            messages.info(request,'تکایە، زانیاری دروست بنوسە!') 
    return render(request,'awat_petrol/add_user.html',{'shifts':shifts}) 

def changeUserPassword(request,id):
    user = Users.objects.get(pk=id)
    sqliteuser = User.objects.get(pk=id)
    if request.method == 'POST':
        old_passwod = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        if user.u_id == sqliteuser.id and user.password == old_passwod:
            if new_password1 == new_password2:
                user.password = new_password1
                sqliteuser.set_password(new_password1)
                user.save()
                sqliteuser.save()
                return render(request,'awat_petrol/change_user_password.html',{'username':user.user,'success':True})
            else:
                messages.info(request,"پێویستە هەردوو وشە نهێنیە تازەکە وەک یەکبن!")            
        else:
            messages.info(request,"تکایە وشە نهێنیە کۆنەکە بە دروستی بنوسە!")
    return render(request,'awat_petrol/change_user_password.html',{'username':user.user})   

def changeUserShift(request,id):
    user = Users.objects.get(pk=id)
    shifts=Shifts.objects.all()
    if request.method == 'POST':
        shift_id= request.POST.get('shift')
        new_shift = Shifts.objects.get(pk=shift_id)
        user.shift = new_shift
        user.save()
        return render(request,'awat_petrol/change_user_shift.html',{'username':user.user,'shifts':shifts,'success':True})

    return render(request,'awat_petrol/change_user_shift.html',{'username':user.user,'shifts':shifts})  
# def editUser(request,id):
#     if request.method=='POST':
#         user = Users.objects.get(pk=id)
#         sqliteuser = User.objects.get(pk=id)
#          
#         if form.is_valid():
#             form.save()
#             return render(request,'awat_petrol/edit_User.html',{'form':form,'success':True})
#     else:
#         User=Users.objects.get(pk=id)
#         form = UserForm(instance=User)
#     return render(request,'awat_petrol/edit_User.html',{'form':form})    

 
def deleteUser(req,id):
    if req.method == 'POST':
        user = Users.objects.get(pk=id)
        sqliteuser = User.objects.get(pk=user.u_id)
        user.delete()  
        sqliteuser.delete()     
    return HttpResponseRedirect(reverse('awat_petrol:view-users'))
#------------Measure Part
def viewMeasures(req):
    measures = Measures.objects.all()
    return render(req,'awat_petrol/view_measures.html',{'measures':measures})

def addMeasure(req):
    if req.method=='POST':
        form=MeasureForm(req.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            to_liter = form.cleaned_data['to_liter']
            check_name = Measures.objects.filter(name=name).values()
            if check_name.count() == 0: 
                new_measure = Measures(name=name, to_liter=to_liter)
                new_measure.save()
                return render(req,'awat_petrol/add_measure.html',{'form':MeasureForm(),'success':True})
    else:
        form=MeasureForm()
    return render(req,'awat_petrol/add_measure.html',{'form':MeasureForm()})  

 
def editMeasure(request,id):
    if request.method=='POST':
        measure = Measures.objects.get(pk=id)
        form = MeasureForm(request.POST,instance=measure)
        if form.is_valid():
            form.save()
            return render(request,'awat_petrol/edit_measure.html',{'form':form,'success':True})
    else:
        measure=Measures.objects.get(pk=id)
        form = MeasureForm(instance=measure)
    return render(request,'awat_petrol/edit_measure.html',{'form':form})    

 
def deleteMeasure(req,id):
    if req.method == 'POST':
        measure = Measures.objects.get(pk=id)
        measure.delete()       
    return HttpResponseRedirect(reverse('awat_petrol:view-measures'))

#------------Item Part
def viewItems(req):
    itemsd = Items.objects.all().order_by('-id')
    record_per_page = RECORD_PER_PAGE
    p=Paginator(itemsd,record_per_page)
    page = req.GET.get('page')
    items = p.get_page(page) 
    pagination = True
    return render(req,'awat_petrol/view_items.html',{'items':items,'pagination':pagination})
#------------Item Part2
 
def addItem(req):
    if req.method=='POST':
        form=ItemForm(req.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            buy_unit = form.cleaned_data['buy_unit']
            tank_size = form.cleaned_data['tank_size']
            sell_unit = form.cleaned_data['sell_unit']
            buy_price = form.cleaned_data['buy_price']
            sell_price = form.cleaned_data['sell_price']
            warning_amount = form.cleaned_data['warning_amount']

            check_name = Items.objects.filter(name=name).values()
            if check_name.count() == 0: 
                new_Item = Items(name=name, buy_unit=buy_unit, tank_size=tank_size,sell_unit=sell_unit,buy_price=buy_price,sell_price=sell_price,warning_amount=warning_amount)
                new_Item.save()
                return render(req,'awat_petrol/add_Item.html',{'form':ItemForm(),'success':True})
    else:
        form=ItemForm()
    return render(req,'awat_petrol/add_Item.html',{'form':ItemForm()})  

 
def editItem(request,id):
    item=Items.objects.get(pk=id)
    if request.method=='POST':
        form = ItemForm(request.POST,instance=item)
        if form.is_valid():    
            form.save()
            return render(request,'awat_petrol/edit_item.html',{'form':form,'success':True})
    else:        
        form = ItemForm(instance=item)
    return render(request,'awat_petrol/edit_item.html',{'form':form})    

 
def deleteItem(req,id):
    if req.method == 'POST':
        item = Items.objects.get(pk=id)
        item.delete()       
    return HttpResponseRedirect(reverse('awat_petrol:view-items'))  

 
def exportItemsCSV(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="items.csv"'

    writer = csv.writer(response)
    writer.writerow(['Item name', 'Buy unit', 'Sell unit', 'Buy price', 'Sell price', 'Warning amount'])

    items = Items.objects.all().values_list('name', 'buy_unit', 'sell_unit', 'buy_price', 'sell_price', 'warning_amount')
    for item in items:
        writer.writerow(item)
    return response  

#------------Shift Part
def viewShifts(req):
    shifts = Shifts.objects.all()
    return render(req,'awat_petrol/view_shifts.html',{'shifts':shifts})

def addShift(req):
    if req.method=='POST':
        form=ShiftForm(req.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            start_work = form.cleaned_data['start_work']
            end_work = form.cleaned_data['end_work']
            check_name = Shifts.objects.filter(name=name).values()
            if check_name.count() == 0: 
                new_Shift = Shifts(name=name, start_work=start_work,end_work=end_work)
                new_Shift.save()
                return render(req,'awat_petrol/add_shift.html',{'form':ShiftForm(),'success':True})
    else:
        form=ShiftForm()
    return render(req,'awat_petrol/add_shift.html',{'form':ShiftForm()})  

 
def editShift(request,id):
    if request.method=='POST':
        shift = Shifts.objects.get(pk=id)
        form = ShiftForm(request.POST,instance=shift)
        if form.is_valid():
            form.save()
            return render(request,'awat_petrol/edit_shift.html',{'form':form,'success':True})
    else:
        shift=Shifts.objects.get(pk=id)
        form = ShiftForm(instance=shift)
    return render(request,'awat_petrol/edit_shift.html',{'form':form})    

 
def deleteShift(req,id):
    if req.method == 'POST':
        shift = Shifts.objects.get(pk=id)
        users = Users.objects.filter(shift=shift)
        for u in users:
            sqlite_user = User.objects.get(pk=u.u_id)
            sqlite_user.delete()
        shift.delete()       
    return HttpResponseRedirect(reverse('awat_petrol:view-shifts'))
#------------Counters Part
def viewCounters(req):
    countersd = Counter.objects.all().order_by('-id')
    record_per_page = RECORD_PER_PAGE
    p=Paginator(countersd,record_per_page)
    page = req.GET.get('page')
    counters = p.get_page(page) 
    pagination = True

    return render(req,'awat_petrol/view_counters.html',{'counters':counters,'pagination':pagination})
def addCounter(req):
    if req.method=='POST':
        form=CounterForm(req.POST) 
        if form.is_valid():
            item = form.cleaned_data['item']
            register = form.cleaned_data['register']
            shift = form.cleaned_data['shift']
            old_register =0
            check_records = Counter.objects.filter(item=item).count()
            if check_records > 0 :
                last_rec = Counter.objects.filter(item=item).aggregate(Max('id'))
                last_id = last_rec['id__max'] # or last_rec.get('id__max')
                last_record = Counter.objects.get(pk=last_id)
                old_register = last_record.register
                store = Store.objects.get(item=item)
                if store.amount >= (register - old_register):
                    bri_froshraw = store.amount - (register - old_register)
                    store.amount = bri_froshraw
                    store.save()
                    new_sell_by_counters = SellByCounters(item=item,amount=(register - old_register))
                    new_sell_by_counters.save()
                else:
                    messages.info(req, " ئەو بڕە بەردەست نیە لە ناو کۆگا! ")
                    return HttpResponseRedirect(reverse('awat_petrol:view-counters'))                

            new_counter = Counter(item=item, register=register,old_register = old_register,shift=shift)
            new_counter.save()
            
            return render(req,'awat_petrol/add_counter.html',{'form':CounterForm(),'success':True})
    else:
        form=CounterForm()
    return render(req,'awat_petrol/add_counter.html',{'form':CounterForm()})  

def deleteCounter(req,id):
    if req.method == 'POST':
        counter = Counter.objects.get(pk=id)
        counter.delete()       
    return HttpResponseRedirect(reverse('awat_petrol:view-counters'))
#------------Return Item
def viewReturnItems(request):
    returnsd = ReturnItem.objects.all().order_by('-id')
    record_per_page = RECORD_PER_PAGE
    p=Paginator(returnsd,record_per_page)
    page = request.GET.get('page')
    returns = p.get_page(page) 
    pagination = True
    return render(request,'awat_petrol/view_return_items.html',{'returns':returns,'pagination':pagination})
def addReturnItem(req):
    if req.method=='POST':
        form=ReturnItemForm(req.POST)
        if form.is_valid():
            item = form.cleaned_data['item']
            amount = form.cleaned_data['amount']
            price = form.cleaned_data['price']
            shift = form.cleaned_data['shift']
            return_date = form.cleaned_data['return_date']
            note = form.cleaned_data['note']
            store_item = Store.objects.get(pk=item.id)
            store_amount = store_item.amount + amount
            store_item.amount = store_amount
            store_item.save()
            new_Item = ReturnItem(item=item, amount=amount, price=price,shift=shift,return_date=return_date,note=note)
            new_Item.save()
            return render(req,'awat_petrol/add_return_item.html',{'form':ReturnItemForm(),'success':True})
    else:
        form=ReturnItemForm()
    return render(req,'awat_petrol/add_return_item.html',{'form':ReturnItemForm()})

def deleteReturnItem(req,id):
    if req.method == 'POST':
        return_item = ReturnItem.objects.get(pk=id)
        
        store_item = Store.objects.get(item=return_item.item)
         
        return_amount = return_item.amount
        if return_amount <= store_item.amount:
            store_amount = store_item.amount - return_amount
            store_item.amount = store_amount
            store_item.save()
            return_item.delete() 
        else:
            messages.info(req,"پێویستە لەم بڕە زیاتر لە کۆگا هەبێت!!")  
                    
    return HttpResponseRedirect(reverse('awat_petrol:view-return-items'))            
#------------DailyExpenses Part
def viewDailyExpenses(req):
    daily_expensesd = DailyExpenses.objects.all().order_by('-id')
    record_per_page = RECORD_PER_PAGE
    p=Paginator(daily_expensesd,record_per_page)
    page = req.GET.get('page')
    daily_expenses = p.get_page(page) 
    pagination = True
    return render(req,'awat_petrol/view_daily_expenses.html',{'daily_expenses':daily_expenses,'pagination':pagination})

def addDailyExpenses(req):
    if req.method=='POST':
        form=DailyExpensesForm(req.POST)
        if form.is_valid():
            # subject = form.cleaned_data['subject']
            # amount = form.cleaned_data['amount']
            # shift = form.cleaned_data['shift']
            # note = form.cleaned_data['note']
            # expenses_date = form.cleaned_data['expenses_date']
            # new_rec = DailyExpenses(subject=subject, amount=amount,shift=shift,note=note,expenses_date=expenses_date)
            form.save()
            return render(req,'awat_petrol/add_daily_expenses.html',{'form':DailyExpensesForm(),'success':True})
    else:
        form=DailyExpensesForm()
    return render(req,'awat_petrol/add_daily_expenses.html',{'form':DailyExpensesForm()})  

 
def editDailyExpenses(request,id):
    if request.method=='POST':
        daily_expenses = DailyExpenses.objects.get(pk=id)
        form = DailyExpensesForm(request.POST,instance=daily_expenses)
        if form.is_valid():
            form.save()
            return render(request,'awat_petrol/edit_daily_expenses.html',{'form':form,'success':True})
    else:
        daily_expenses = DailyExpenses.objects.get(pk=id)
        form = DailyExpensesForm(instance=daily_expenses)
    return render(request,'awat_petrol/edit_daily_expenses.html',{'form':form})    

 
def deleteDailyExpenses(req,id):
    if req.method == 'POST':
        daily_expenses = DailyExpenses.objects.get(pk=id)
        daily_expenses.delete()       
    return HttpResponseRedirect(reverse('awat_petrol:view-daily-expenses'))

#------------Tanks Part
class EditorChartView(TemplateView):#LoginRequiredMixin
    #login_url='awat_petrol:login'
    template_name = 'awat_petrol/tanks.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["qs"] = Store.objects.all()
        return context

#------------search Part 
#@login_required(login_url='awat_petrol:login')
#@allowed_users(allowed_roles=['awat_admin']) 
def searchVender(request):
    if request.method =="GET":
        search = request.GET.get('venderSearch')
        if search != "":
            venders = Venders.objects.all().filter(fullName__startswith=search)
            customers = Customers.objects.all()
            return render(request,'awat_petrol/index.html',{'venders':venders,'customers':customers}) 
        else:
            return HttpResponseRedirect(reverse('awat_petrol:index'))

#@login_required(login_url='awat_petrol:login')
#@allowed_users(allowed_roles=['awat_admin'])         
def searchCustomer(request):
    if request.method =="GET":
        search = request.GET.get('customerSearch')
        if search != "":
            customers = Customers.objects.all().filter(fullName__startswith=search)
            venders = Venders.objects.all()
            return render(request,'awat_petrol/index.html',{'venders':venders,'customers':customers}) 
        else:
            return HttpResponseRedirect(reverse('awat_petrol:index')) 

#@login_required(login_url='awat_petrol:login')
#@allowed_users(allowed_roles=['awat_admin']) 
def customerAccounts(request,id):
    customer = Customers.objects.get(pk=id)
    buy_records = Sell.objects.filter(customer=customer).order_by('-id')
    
    record_per_page = RECORD_PER_PAGE
    p=Paginator(buy_records,record_per_page)
    page = request.GET.get('page')
    records = p.get_page(page) 
    pagination = True

    if request.method == "POST":
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        records=buy_records.filter(buy_date__range=(start_date, end_date)).order_by('-id') 
        pagination = False

    return render(request, "awat_petrol/customer_accounts.html",{'records':records,'pagination':pagination,'customer':customer})

#@login_required(login_url='awat_petrol:login')
#@allowed_users(allowed_roles=['awat_admin'])  
def ToCustomerEnterMoney(request,id):
    customer = Customers.objects.get(pk=id)
    last_account = 0
    try:
        customer_records = Sell.objects.filter(customer=customer)
        last_account = customer_records.latest('id').last_account        
    except Sell.DoesNotExist:
        pass
    if request.method == 'POST':
        form = ToCustomerEnterMoneyForm(request.POST)
        if form.is_valid():
            paid_money=form.cleaned_data['paid_money']
            sell_date=form.cleaned_data['sell_date']
            note=form.cleaned_data['note']
            if last_account==0:
                messages.info(request, "هیچ بڕە پارەیەکی قەرز نیە!")
                return HttpResponseRedirect(reverse('awat_petrol:to-customer-enter-money', kwargs={'id':id})) 
                #return render(request,'to_customer_enter_money.html',{'form':ToCustomerEnterMoneyForm(),'customer':customer})  
            if paid_money > last_account:
                messages.info(request, f"ئەم بڕە {paid_money} زیاترە لە قەرزەکە!")
                return HttpResponseRedirect(reverse('awat_petrol:to-customer-enter-money', kwargs={'id':id})) 
                #return render(request,'to_customer_enter_money.html',{'form':ToCustomerEnterMoneyForm(),'customer':customer})                               
            if paid_money==0 or paid_money=="":
                messages.info(request, "تکایە بڕی پارەی واسڵکراو بنوسە!")
                return HttpResponseRedirect(reverse('awat_petrol:to-customer-enter-money', kwargs={'id':id})) 
                #return render(request,'awat_petrol/to_customer_enter_money.html',{'form':ToCustomerEnterMoneyForm(),'customer':customer})             

            new_Item = Sell(customer=customer, item=None, amount=0, sell_unit='Lt', buy_price=0, sell_price=0, sell_date=sell_date, paid_money=paid_money,note=note)#,entry_user=request.user
            new_Item.save()
            return render(request,'awat_petrol/to_customer_enter_money.html',{'form':ToCustomerEnterMoneyForm(),'success':True,'customer':customer})
    else:
        form=ToCustomerEnterMoneyForm()
    return render(request,'awat_petrol/to_customer_enter_money.html',{'form':ToCustomerEnterMoneyForm(),'customer':customer}) 

#------------Buy Part
#@login_required(login_url='awat_petrol:login')
#@allowed_users(allowed_roles=['awat_admin']) 
def viewBuy(request):
    buy_records = Buy.objects.filter().exclude(item=None).order_by('-id')

    record_per_page = RECORD_PER_PAGE
    p=Paginator(buy_records,record_per_page)
    page = request.GET.get('page')
    records = p.get_page(page) 
    pagination = True

    total_buy=[]
    total_prof=[]
    total_profit=[]

     
    filt=Buy.objects.filter().exclude(item=None).values('item').annotate(total=Sum('amount'))
    
    for t in filt:
            name=None 
            try:
               item = Items.objects.get(pk = t['item'])
               name = item.name              
            except Items.DoesNotExist:
                name = None
            if name != None:
                a={name:t['total']}
                total_buy.append(a)
    
      
    b_price=0
    for i in buy_records:
        
        if i.item !=None:
           b_price = (i.buy_price) / i.item.buy_unit.to_liter
           s_price = i.sell_price
           amount = (i.amount) * i.item.buy_unit.to_liter
           #pro = (s_price - round(b_price,5)) * round(amount,5)
           pro = (s_price - b_price) * amount
           a={'item':i.item.name,'total':round(pro)}
           total_prof.append(a)
   
    score_dict = dict()
    for d in total_prof:
        name = d['item']
        if name in score_dict:
            score_dict[name] += d['total']
        else:
            score_dict[name] = d['total']
    total_profit.append(score_dict)
     
    if request.method == "POST":
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        records=buy_records.filter(buy_date__range=(start_date, end_date)).exclude(item=None).order_by('-id') 
        pagination = False

        total_buy=[]
        total_prof=[]
        total_profit=[]

       
        filt=Buy.objects.filter(buy_date__range=(start_date, end_date)).exclude(item=None).values('item').annotate(total=Sum('amount'))
        for t in filt:
            name=None 
            try:
                item = Items.objects.get(pk = t['item'])
                name = item.name              
            except Items.DoesNotExist:
                name = None
            if name != None:
                a={name:t['total']}
                total_buy.append(a)

        b_price=0
        for i in records:
            if i.item !=None:
                b_price = (i.buy_price) / i.item.buy_unit.to_liter
                s_price = i.sell_price
                amount = (i.amount) * i.item.buy_unit.to_liter
                #pro = (s_price - round(b_price,5)) * round(amount,5)
                pro = (s_price - b_price) * amount
                a={'item':i.item.name,'total':round(pro)}
                total_prof.append(a)
        
        score_dict = dict()
        for d in total_prof:
            name = d['item']
            if name in score_dict:
                score_dict[name] += d['total']
            else:
                score_dict[name] = d['total']
        total_profit.append(score_dict)

    return render(request, "awat_petrol/view_buy.html",{'records':records,'pagination':pagination,'total_profit':total_profit,'total_buy':total_buy})

#@login_required(login_url='awat_petrol:login')
#@allowed_users(allowed_roles=['awat_admin']) 
def addBuy(req,id): 
    vender = Venders.objects.get(pk=id)   
    if req.method=='POST':
        form=BuyForm(req.POST)
        if form.is_valid():
            bill_no = form.cleaned_data['bill_no']
            item = form.cleaned_data['item']
            amount = form.cleaned_data['amount']
            #lost_amount = form.cleaned_data['lost_amount']
            total_money = form.cleaned_data['total_money']
            buy_price = form.cleaned_data['buy_price']
            buy_date = form.cleaned_data['buy_date']
            paid_money = form.cleaned_data['paid_money']
            note = form.cleaned_data['note']
            
            store = Store.objects.get(item=form.instance.item.id)
            finditem = Items.objects.get(id=form.instance.item.id)
            sell_price = finditem.sell_price
             
            store_amount = store.amount/finditem.buy_unit.to_liter
            tank_size = finditem.tank_size

            if (amount + store_amount) > tank_size:
                messages.info(req, f"جێگای {amount} نابێتەوە لە تانکیەکە")
                return render(req,'awat_petrol/add_buy.html',{'form':BuyForm(),'vender':vender}) 
            else:

                # check_records = Buy.objects.filter(vender=vender).count()
                
                # if check_records > 0:
                #     latest_id = Buy.objects.latest('id').id
                #     res = Buy.objects.filter(vender=vender).aggregate(max_id=Max('pk'))
                #     max_id = res.get('max_id')

                #     sum_totals = Buy.objects.filter(id__lt=max_id,vender=vender).aggregate(Sum("total_money"))
                #     sum_paids = Buy.objects.filter(id__lt=max_id,vender=vender).aggregate(Sum("paid_money"))
                #     totals = sum_totals['total_money__sum']
                #     paids = sum_paids['paid_money__sum']

                #     last_account = (totals - paids) + total_money - paid_money               
                # else:
                #     last_account = total_money - paid_money

                new_Item = Buy(vender=vender, bill_no=bill_no, item=item, amount=amount, buy_unit=finditem.buy_unit,sell_price=sell_price, buy_price=buy_price, buy_date=buy_date, paid_money=paid_money,note=note) #,entry_user=req.user
                new_Item.save()
                return render(req,'awat_petrol/add_buy.html',{'form':BuyForm(),'vender':vender,'success':True})
    else:
        form=BuyForm()
    return render(req,'awat_petrol/add_buy.html',{'form':BuyForm(),'vender':vender}) 

#@login_required(login_url='awat_petrol:login')
#@allowed_users(allowed_roles=['awat_admin']) 
def editBuyRecord(request,id):
    buy_record = Buy.objects.get(pk=id)
    old_amount = copy_old_value.copy(buy_record.amount)
    old_item = copy_old_value.copy(buy_record.item)
    
    vender_id = buy_record.vender.id
    totals =0
    paids =0
    i=Buy.objects.filter(id__lt=id,vender=buy_record.vender).count()
    
    if i > 0:
        sum_totals = Buy.objects.filter(id__lt=id,vender=buy_record.vender).aggregate(Sum("total_money"))
        sum_paids = Buy.objects.filter(id__lt=id,vender=buy_record.vender).aggregate(Sum("paid_money"))
        totals=sum_totals['total_money__sum']
        paids=sum_paids['paid_money__sum']
 
    if buy_record.item == None:
         
        if request.method == 'POST': 
           form = ToVenderEnterMoneyForm(request.POST,instance=buy_record)
           if form.is_valid():
               paid_money = form.instance.paid_money
               buy_date = form.instance.buy_date
               note = form.instance.note  

               last_account = (totals - paids) + buy_record.total_money - paid_money            
               Buy.objects.filter(pk=id).update(paid_money=paid_money,last_account=last_account ,buy_date=buy_date,note=note)
               
               get_current_last_account = Buy.objects.get(pk=id).last_account
               list=Buy.objects.filter(id__gt=id,vender=buy_record.vender)
               for l_id in list :
                    buy=Buy.objects.get(pk=l_id.id)
                    item = buy.item
                    tot = buy.total_money
                    pai =buy.paid_money
                    last_account = get_current_last_account + (tot - pai)
                    Buy.objects.filter(pk=l_id.id).update(last_account = last_account) 
                    get_current_last_account = get_current_last_account + (tot - pai)

               return render(request,'awat_petrol/edit_buy_record.html',{'form':form,'vender_id':vender_id,'success':True})
        else:
            form=ToVenderEnterMoneyForm(instance=buy_record)       
    else:
         
        if request.method == 'POST':         
            form = BuyToUpdateRecordForm(request.POST,instance=buy_record)
            if form.is_valid():    
                bill_no=form.instance.bill_no
                item=form.instance.item
                amount=form.instance.amount
                buy_price=form.instance.buy_price
                buy_date=form.instance.buy_date
                paid_money=form.instance.paid_money
                note=form.instance.note
                # amount = amount * buy_record.item.buy_unit.to_liter
                # print(f"Item to liter{amount}")
                lost_amount = form.instance.lost_amount
 
                last_account = (totals - paids) + buy_record.total_money - paid_money 

                clear_amount = amount - lost_amount  
                total_money = amount * buy_price
                loan_money = total_money - paid_money

                
                if old_item != item:
                    print("item changed")
                    # we use this variable when the item unit is changed
                    new_item = item
                    new_item_store = Store.objects.get(item=new_item.id)
                    new_item_store_amount = new_item_store.amount

                    old_item_store = Store.objects.get(item=old_item.id)
                    old_item_store_amount = old_item_store.amount

                    Store.objects.filter(item=old_item_store.item).update(amount=(old_item_store_amount - old_amount)) 
                    Store.objects.filter(item=new_item_store.item).update(amount=(new_item_store_amount + amount))
                    
                     # we need to know the buy_unit of the item has effects on it's amount!!!
                     # the store should be change according to old item value and new one value!
                     # subtract old value for old item, and add new value for new item
                    Buy.objects.filter(pk=id).update(bill_no=bill_no,item=item,amount=amount,clear_amount=clear_amount,total_money=total_money,loan_money=loan_money,buy_price=buy_price,buy_date=buy_date,paid_money=paid_money,note=note,last_account=last_account) 
                else:
                    print("item not changed")

                    store = Store.objects.get(item=item.id)
                    store_amount = store.amount / buy_record.item.buy_unit.to_liter

                    new_stor= ((store_amount + amount) - old_amount) * buy_record.item.buy_unit.to_liter
                    
                    Store.objects.filter(item=store.item.id).update(amount=new_stor) 
                    # change the store for this item only, by it's new value. 
                    Buy.objects.filter(pk=id).update(bill_no=bill_no,item=item,amount=amount,clear_amount=clear_amount,total_money=total_money,loan_money=loan_money,buy_price=buy_price,buy_date=buy_date,paid_money=paid_money,note=note,last_account=last_account)

                get_current_last_account = Buy.objects.get(pk=id).last_account
                list=Buy.objects.filter(id__gt=id,vender=buy_record.vender)
                for l_id in list :
                    buy=Buy.objects.get(pk=l_id.id)
                    item = buy.item
                    tot = buy.total_money
                    pai =buy.paid_money
                    last_account = get_current_last_account + (tot - pai)
                    Buy.objects.filter(pk=l_id.id).update(last_account = last_account) 
                    get_current_last_account = get_current_last_account + (tot - pai)        
                return render(request,'awat_petrol/edit_buy_record.html',{'form':form,'vender_id':vender_id,'success':True})
        else:
            form=BuyToUpdateRecordForm(instance=buy_record)
    return render(request,'awat_petrol/edit_buy_record.html',{'form':form,'vender_id':vender_id}) 

#@login_required(login_url='awat_petrol:login')
#@allowed_users(allowed_roles=['awat_admin']) 
def deleteBuyRecord(request,id):
     
    buy_record = Buy.objects.get(pk=id)
 
    message = ""
    vender_id = copy_old_value.copy(buy_record.vender.id)
    vender = copy_old_value.copy(buy_record.vender)
    if request.method == 'POST':
        # vender = copy_old_value.copy(buy_record.vender)

        totals =buy_record.total_money
        paids =buy_record.paid_money

        get_current_both_total_paid = 0

        # i=Buy.objects.filter(id__lt=id,vender=buy_record.vender).count()       
        # if i > 0:
        #     sum_totals = Buy.objects.filter(id__lt=id,vender=buy_record.vender).aggregate(Sum("total_money"))
        #     sum_paids = Buy.objects.filter(id__lt=id,vender=buy_record.vender).aggregate(Sum("paid_money"))
        #     totals=sum_totals['total_money__sum']
        #     paids=sum_paids['paid_money__sum'] 

        if buy_record.item != None:  
            get_current_both_total_paid = totals + paids
            amount = buy_record.amount * buy_record.item.buy_unit.to_liter
            store = Store.objects.get(item = buy_record.item.id)
            store_amount = store.amount 
            if store_amount >= amount:
                Store.objects.filter(item=buy_record.item.id).update(amount=store_amount - amount)
                buy_record.delete()    
            else: 
                message = "ئەو بڕەی لە ناو کۆگایە کەمترە لەو بڕە!"
        else: 
            # none item part
            get_current_both_total_paid = -(totals + paids) 
            buy_record.delete()  

        list=Buy.objects.filter(id__gt=id,vender=vender)
        for l_id in list :
            buy=Buy.objects.get(pk=l_id.id)
            last_account = buy.last_account
            Buy.objects.filter(pk=l_id.id).update(last_account = last_account - get_current_both_total_paid ) 
                            
    return HttpResponseRedirect(reverse('awat_petrol:vender-accounts', kwargs={'id':vender_id})) 
#------------find buy_unit
#@login_required(login_url='awat_petrol:login')
#@allowed_users(allowed_roles=['awat_admin']) 
def findBuyUnit(request):
    item_id = request.GET.get('id', None)
    item = Items.objects.get(id=item_id)
    measure = Measures.objects.get(name = item.buy_unit)
    return JsonResponse(json.dumps({'data':measure.name}), content_type="application/json",safe=False) 
#@login_required(login_url='awat_petrol:login')
#@allowed_users(allowed_roles=['awat_admin']) 
def printVenderAccount(request,id):
    record = Buy.objects.get(pk=id)
    old_loan = record.last_account - (record.total_money - record.paid_money)
    return render(request,'awat_petrol/print_vender_account.html',{'record':record,'old_loan':old_loan})

#------------Sell Part
#@login_required(login_url='awat_petrol:login')
#@allowed_users(allowed_roles=['awat_admin']) 
def viewSell(request):
 

    sell_records = Sell.objects.filter().exclude(item=None).order_by('-id')

    record_per_page = RECORD_PER_PAGE
    p=Paginator(sell_records,record_per_page)
    page = request.GET.get('page')
    records = p.get_page(page) 
    pagination = True

    total_sell=[]
    total_prof=[]
    total_profit=[]

     
    filt=Sell.objects.filter().exclude(item=None).values('item').annotate(total=Sum('amount'))
    
    for t in filt:
            name=None 
            try:
               item = Items.objects.get(pk = t['item'])
               name = item.name              
            except Items.DoesNotExist:
                name = None
            if name != None:
                a={name:t['total']}
                total_sell.append(a)
    
      
    b_price=0
    for i in sell_records:
        
        if i.item !=None:
           b_price = (i.buy_price) / i.item.buy_unit.to_liter
           s_price = i.sell_price
           amount = (i.amount) 
           #pro = (s_price - round(b_price,5)) * round(amount,5)
           pro = (s_price - b_price) * amount
           a={'item':i.item.name,'total':round(pro)}
           total_prof.append(a)
   
    score_dict = dict()
    for d in total_prof:
        name = d['item']
        if name in score_dict:
            score_dict[name] += d['total']
        else:
            score_dict[name] = d['total']
    total_profit.append(score_dict)
     
    if request.method == "POST":
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        records=sell_records.filter(sell_date__range=(start_date, end_date)).exclude(item=None).order_by('-id') 
        pagination = False

        total_sell=[]
        total_prof=[]
        total_profit=[]

       
        filt=Sell.objects.filter(sell_date__range=(start_date, end_date)).exclude(item=None).values('item').annotate(total=Sum('amount'))
        for t in filt:
            name=None 
            try:
                item = Items.objects.get(pk = t['item'])
                name = item.name              
            except Items.DoesNotExist:
                name = None
            if name != None:
                a={name:t['total']}
                total_sell.append(a)

        b_price=0
        for i in records:
            if i.item !=None:
                b_price = (i.buy_price) / i.item.buy_unit.to_liter
                s_price = i.sell_price
                amount = (i.amount) 
                #pro = (s_price - round(b_price,5)) * round(amount,5)
                pro = (s_price - b_price) * amount
                a={'item':i.item.name,'total':round(pro)}
                total_prof.append(a)
        
        score_dict = dict()
        for d in total_prof:
            name = d['item']
            if name in score_dict:
                score_dict[name] += d['total']
            else:
                score_dict[name] = d['total']
        total_profit.append(score_dict)

    return render(request, "awat_petrol/view_sell.html",{'records':records,'total_sell':total_sell,'total_profit':total_profit,'pagination':pagination})
#------------find sell_unit
#@login_required(login_url='awat_petrol:login')
#@allowed_users(allowed_roles=['awat_admin']) 
def findSellUnit(request):
    item_id = request.GET.get('id', None)
    item = Items.objects.get(id=item_id)
    item_price = item.sell_price
    print(item_price)
    measure = Measures.objects.get(name = item.sell_unit)
    return JsonResponse(json.dumps({'data':measure.name,'price':item_price},cls=DjangoJSONEncoder), content_type="application/json",safe=False) 

#@login_required(login_url='awat_petrol:login')
#@allowed_users(allowed_roles=['awat_admin']) 
def addSell(req,id): 
    customer = Customers.objects.get(pk=id)   
    if req.method=='POST':
        form=SellForm(req.POST)
        if form.is_valid():
            item = form.cleaned_data['item']
            amount = form.cleaned_data['amount']
            lost_amount = form.cleaned_data['lost_amount']
            total_money = form.cleaned_data['total_money']
            # find_sell_price = Items.objects.get(name = item)
            # form.fields['sell_price'].initial = find_sell_price.sell_price
            sell_price = form.cleaned_data['sell_price']
            sell_date = form.cleaned_data['sell_date']
            paid_money = form.cleaned_data['paid_money']
            note = form.cleaned_data['note']
            
            store = Store.objects.get(item=form.instance.item.id)
            finditem = Items.objects.get(id=form.instance.item.id)
            sell_price = finditem.sell_price
             
            store_amount = store.amount #/finditem.buy_unit.to_liter
             
            if amount > store_amount:
                messages.info(req, f"بڕی {amount}{finditem.sell_unit} {finditem.name} بەردەست نیە!")
                return render(req,'awat_petrol/add_sell.html',{'form':SellForm(),'customer':customer}) 
            else:
                new_Item = Sell(customer=customer, item=item, amount=amount, lost_amount=lost_amount,sell_unit=finditem.sell_unit, sell_price=sell_price, buy_price=finditem.buy_price, sell_date=sell_date, paid_money=paid_money,note=note)#,entry_user=req.user
                new_Item.save()
                return render(req,'awat_petrol/add_sell.html',{'form':SellForm(),'customer':customer,'success':True})
    else:
        form=SellForm()
    return render(req,'awat_petrol/add_sell.html',{'form':SellForm(),'customer':customer}) 


#@login_required(login_url='awat_petrol:login')
#@allowed_users(allowed_roles=['awat_admin']) 
def printCustomerAccount(request,id):
    record = Sell.objects.get(pk=id)
    old_loan = record.last_account - (record.total_money - record.paid_money)
    return render(request,'awat_petrol/print_customer_account.html',{'record':record,'old_loan':old_loan})

#@login_required(login_url='awat_petrol:login')
#@allowed_users(allowed_roles=['awat_admin']) 
def editSellRecord(request,id):
    sell_record = Sell.objects.get(pk=id)
    old_amount = copy_old_value.copy(sell_record.amount)
    old_lost_amount = copy_old_value.copy(sell_record.lost_amount)
    old_item = copy_old_value.copy(sell_record.item)
    
    customer_id = sell_record.customer.id
    totals =0
    paids =0
    i=Sell.objects.filter(id__lt=id,customer=sell_record.customer).count()
    
    if i > 0:
        sum_totals = Sell.objects.filter(id__lt=id,customer=sell_record.customer).aggregate(Sum("total_money"))
        sum_paids = Sell.objects.filter(id__lt=id,customer=sell_record.customer).aggregate(Sum("paid_money"))
        totals=sum_totals['total_money__sum']
        paids=sum_paids['paid_money__sum']
 
    if sell_record.item == None:
         
        if request.method == 'POST': 
           form = ToCustomerEnterMoneyForm(request.POST,instance=sell_record)
           if form.is_valid():
               paid_money = form.instance.paid_money
               sell_date = form.instance.sell_date
               note = form.instance.note  

               last_account = (totals - paids) + sell_record.total_money - paid_money            
               Sell.objects.filter(pk=id).update(paid_money=paid_money,last_account=last_account ,sell_date=sell_date,note=note)
               
               get_current_last_account = Sell.objects.get(pk=id).last_account
               list=Sell.objects.filter(id__gt=id,customer=sell_record.customer)
               for l_id in list :
                    sell=Sell.objects.get(pk=l_id.id)
                    item = sell.item
                    tot = sell.total_money
                    pai =sell.paid_money
                    last_account = get_current_last_account + (tot - pai)
                    Sell.objects.filter(pk=l_id.id).update(last_account = last_account) 
                    get_current_last_account = get_current_last_account + (tot - pai)

               return render(request,'awat_petrol/edit_sell_record.html',{'form':form,'customer_id':customer_id,'success':True})
        else:
            form=ToCustomerEnterMoneyForm(instance=sell_record)       
    else:
         
        if request.method == 'POST':         
            form = SellToUpdateRecordForm(request.POST,instance=sell_record)
            if form.is_valid():    
                
                item=form.instance.item
                amount=form.instance.amount
                # lost_amount=form.instance.lost_amount
                sell_price=form.instance.sell_price
                sell_date=form.instance.sell_date
                paid_money=form.instance.paid_money
                note=form.instance.note

                lost_amount = form.instance.lost_amount
 
                last_account = (totals - paids) + sell_record.total_money - paid_money 

                clear_amount = amount #- lost_amount  
                total_money = amount * sell_price
                loan_money = total_money - paid_money

                
                if old_item != item:
                    print("item changed")
                    # we use this variable when the item unit is changed
                    new_item = item
                    new_item_store = Store.objects.get(item=new_item.id)
                    new_item_store_amount = new_item_store.amount

                    old_item_store = Store.objects.get(item=old_item.id)
                    old_item_store_amount = old_item_store.amount

                    Store.objects.filter(item=old_item_store.item).update(amount=(old_item_store_amount + (old_amount+old_lost_amount))) 
                    Store.objects.filter(item=new_item_store.item).update(amount=(new_item_store_amount - (amount+lost_amount)))
                    
                     # we need to know the buy_unit of the item has effects on it's amount!!!
                     # the store should be change according to old item value and new one value!
                     # subtract old value for old item, and add new value for new item
                    Sell.objects.filter(pk=id).update(item=item,amount=amount,clear_amount=clear_amount,lost_amount=lost_amount,total_money=total_money,loan_money=loan_money,sell_price=sell_price,sell_date=sell_date,paid_money=paid_money,note=note,last_account=last_account) 
                else:
                    print("item not changed")

                    store = Store.objects.get(item=item.id)
                    store_amount = store.amount  

                    new_stor= ((store_amount - (amount+lost_amount)) + (old_amount+ old_lost_amount))  
                    
                    Store.objects.filter(item=store.item.id).update(amount=new_stor) 
                    # change the store for this item only, by it's new value. 
                    Sell.objects.filter(pk=id).update(item=item,amount=amount,clear_amount=clear_amount,lost_amount=lost_amount,total_money=total_money,loan_money=loan_money,sell_price=sell_price,sell_date=sell_date,paid_money=paid_money,note=note,last_account=last_account)

                get_current_last_account = Sell.objects.get(pk=id).last_account
                list=Sell.objects.filter(id__gt=id,customer=sell_record.customer)
                for l_id in list :
                    sell=Sell.objects.get(pk=l_id.id)
                    item = sell.item
                    tot = sell.total_money
                    pai =sell.paid_money
                    last_account = get_current_last_account + (tot - pai)
                    Sell.objects.filter(pk=l_id.id).update(last_account = last_account) 
                    get_current_last_account = get_current_last_account + (tot - pai)        
                return render(request,'awat_petrol/edit_sell_record.html',{'form':form,'customer_id':customer_id,'success':True})
        else:
            form=SellToUpdateRecordForm(instance=sell_record)
    return render(request,'awat_petrol/edit_sell_record.html',{'form':form,'customer_id':customer_id}) 


#@login_required(login_url='awat_petrol:login')
#@allowed_users(allowed_roles=['awat_admin']) 
def deleteSellRecord(request,id):
     
    sell_record = Sell.objects.get(pk=id)
 
    message = ""
    customer_id = copy_old_value.copy(sell_record.customer.id)
    customer = copy_old_value.copy(sell_record.customer)
    if request.method == 'POST':
        # vender = copy_old_value.copy(buy_record.vender)

        totals =sell_record.total_money
        paids =sell_record.paid_money

        get_current_both_total_paid = 0

        if sell_record.item != None:  
            get_current_both_total_paid = totals + paids
            amount = sell_record.amount  
            lost_amount =  sell_record.lost_amount 
            store = Store.objects.get(item = sell_record.item.id)
            store_amount = store.amount 
            print(f"tank size {sell_record.item.tank_size}")
            print(f"store nwe: amount{amount}+ clear{lost_amount}+ oldstore{store_amount} ={(amount + lost_amount)+store_amount}")
             
            if sell_record.item.tank_size >= (amount + lost_amount)+store_amount:
                
                Store.objects.filter(item=sell_record.item.id).update(amount=store_amount + (amount + lost_amount))
                sell_record.delete()    
            else: 
                message = "ئەم بڕە لە ناو تانکیەکە جێگای نابێتەوە!"
        else: 
            # none item part
            get_current_both_total_paid = -(totals + paids) 
            sell_record.delete()  

        list=Sell.objects.filter(id__gt=id,customer=customer)
        for l_id in list :
            sell=Sell.objects.get(pk=l_id.id)
            last_account = sell.last_account
            Sell.objects.filter(pk=l_id.id).update(last_account = last_account - get_current_both_total_paid ) 
                            
    return HttpResponseRedirect(reverse('awat_petrol:customer-accounts', kwargs={'id':customer_id})) 
