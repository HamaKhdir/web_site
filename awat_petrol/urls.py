from django.urls import path
from . import views


app_name='awat_petrol' 
urlpatterns = [
    path('', views.index,name='index'),
    #------ store part
    path('store/',views.viewStore,name='show-store'),
    path('edit-store/<int:id>/',views.editStore,name='edit-store'),
    path('tanks/', views.EditorChartView.as_view(), name='show-tanks'), 
    #------ vender part
    path('view-venders/',views.viewVenders,name='view-venders'),
    path('<int:id>',views.getVender,name='view-vender'),
    path('add-vender/',views.addVender,name='add-vender'),
    path('edit-vender/<int:id>/',views.editVender,name='edit-vender'),
    path('delete-vender/<int:id>/',views.deleteVender,name='delete-vender'),
    path('vender-accounts/<int:id>/',views.venderAccounts,name='vender-accounts'),
    path('to-vender-enter-money/<int:id>/', views.ToVenderEnterMoney, name='to-vender-enter-money'),
    path('search-vender/', views.searchVender, name='search-vender'),
    path('print-vender-account/<int:id>/', views.printVenderAccount, name='print-vender-account'),
    #------ customer part
    path('view-customers/',views.viewCustomers,name='view-customers'),
    path('<int:id>',views.getCustomer,name='view-customer'),
    path('add-customer/',views.addCustomer,name='add-customer'),
    path('edit-customer/<int:id>/',views.editCustomer,name='edit-customer'),
    path('delete-customer/<int:id>/',views.deleteCustomer,name='delete-customer'),
    path('customer-accounts/<int:id>/',views.customerAccounts,name='customer-accounts'),
    path('to-customer-enter-money/<int:id>/', views.ToCustomerEnterMoney, name='to-customer-enter-money'),
    path('search-customer/', views.searchCustomer, name='search-customer'), 
    #------ user part
    path('view-users/',views.viewUsers,name='view-users'), 
    path('add-user/',views.addUser,name='add-user'),
    path('change-user-password/<int:id>/',views.changeUserPassword,name='change-user-password'),
    path('change-user-shift/<int:id>/',views.changeUserShift,name='change-user-shift'),
    path('delete-user/<int:id>/',views.deleteUser,name='delete-user'), 
    #------ item part
    path('view-items/',views.viewItems,name='view-items'),    
    path('add-item/',views.addItem,name='add-item'),
    path('edit-item/<int:id>/',views.editItem,name='edit-item'),
    path('delete-item/<int:id>/',views.deleteItem,name='delete-item'), 
    path('export-items-csv',views.exportItemsCSV,name='export-items-csv'),
    #------ shift part
    path('view-shifts/',views.viewShifts,name='view-shifts'),    
    path('add-shift/',views.addShift,name='add-shift'),
    path('edit-shift/<int:id>/',views.editShift,name='edit-shift'),
    path('delete-shift/<int:id>/',views.deleteShift,name='delete-shift'), 
    #------ measure part
    path('view-measures/',views.viewMeasures,name='view-measures'),    
    path('add-measure/',views.addMeasure,name='add-measure'),
    path('edit-measure/<int:id>/',views.editMeasure,name='edit-measure'),
    path('delete-measure/<int:id>/',views.deleteMeasure,name='delete-measure'), 
    #------ counter part
    path('add-counter/',views.addCounter,name='add-counter'),
    path('view-counters/',views.viewCounters,name='view-counters'),
    path('delete-counter/<int:id>/',views.deleteCounter,name='delete-counter'),
    #------ Daily Expenses part
    path('view-daily-expenses/',views.viewDailyExpenses,name='view-daily-expenses'),    
    path('add-daily-expenses/',views.addDailyExpenses,name='add-daily-expenses'),
    path('edit-daily-expenses/<int:id>/',views.editDailyExpenses,name='edit-daily-expenses'),
    path('delete-daily-expenses/<int:id>/',views.deleteDailyExpenses,name='delete-daily-expenses'),
    #------ buy part  
    path('view-buy/',views.viewBuy,name='view-buy'),
    path('add-buy/<int:id>/',views.addBuy,name='add-buy'),
    path('edit-buy-record/<int:id>/', views.editBuyRecord, name='edit-buy-record'),
    path('delete-buy-record/<int:id>/', views.deleteBuyRecord, name='delete-buy-record'),
    #------ find buy_unit  
    path('find-buy-unit',views.findBuyUnit,name='find-buy-unit'),
    #------ find sell_unit  
    path('find-sell-unit',views.findSellUnit,name='find-sell-unit'), 
    #------ sell part  
    path('view-sell/',views.viewSell,name='view-sell'), 
    path('add-sell/<int:id>/',views.addSell,name='add-sell'),
    path('print-customer-account/<int:id>/', views.printCustomerAccount, name='print-customer-account'),
    path('edit-sell-record/<int:id>/', views.editSellRecord, name='edit-sell-record'),
    path('delete-sell-record/<int:id>/', views.deleteSellRecord, name='delete-sell-record'),
    #------ return item part  
    path('view-return-items/',views.viewReturnItems,name='view-return-items'), 
    path('add-return-item/',views.addReturnItem,name='add-return-item'),
    path('delete-return-item/<int:id>/', views.deleteReturnItem, name='delete-return-item'),
]