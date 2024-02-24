from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name='peshang_petrol' 
urlpatterns = [
    #------ users part
    #path('register/',views.registerPage,name='register'),
    path('login/',views.loginPage,name='login'),
    path('logout/',views.logoutUser,name='logout'),

    path('', views.index,name='index'),
    path('view-venders/',views.viewVenders,name='view-venders'),
    #------ vender part
    path('<int:id>',views.getVender,name='view-vender'),
    path('add-vender/',views.addVender,name='add-vender'),
    path('edit-vender/<int:id>/',views.editVender,name='edit-vender'),
    path('delete-vender/<int:id>/',views.deleteVender,name='delete-vender'),
    path('vender-accounts/<int:id>/',views.venderAccounts,name='vender-accounts'),
    #------ customer part
    path('view-customers/',views.viewCustomers,name='view-customers'),
    path('<int:id>',views.getCustomer,name='view-customer'),
    path('add-customer/',views.addCustomer,name='add-customer'),
    path('edit-customer/<int:id>/',views.editCustomer,name='edit-customer'),
    path('delete-customer/<int:id>/',views.deleteCustomer,name='delete-customer'),
    #------ item part
    path('view-items/',views.viewItems,name='view-items'),    
    path('add-item/',views.addItem,name='add-item'),
    path('edit-item/<int:id>/',views.editItem,name='edit-item'),
    path('delete-item/<int:id>/',views.deleteItem,name='delete-item'), 
    path('export-items-csv',views.exportItemsCSV,name='export-items-csv'),
    #------ measure part
    path('view-measures/',views.viewMeasures,name='view-measures'),    
    path('add-measure/',views.addMeasure,name='add-measure'),
    path('edit-measure/<int:id>/',views.editMeasure,name='edit-measure'),
    path('delete-measure/<int:id>/',views.deleteMeasure,name='delete-measure'), 
 
    #------ store part
    path('store/',views.viewStore,name='show-store'),
    #------ find buy_unit  
    path('find-buy-unit',views.findBuyUnit,name='find-buy-unit'), 
    #------ buy part  
    path('view-buy/',views.viewBuy,name='view-buy'),
    path('add-buy/<int:id>/',views.addBuy,name='add-buy'),
 
    path('tanks/', views.EditorChartView.as_view(), name='tanks'),
    path('search-vender/', views.searchVender, name='search-vender'),
    path('search-customer/', views.searchCustomer, name='search-customer'),
    path('print-vender-account/<int:id>/', views.printVenderAccount, name='print-vender-account'),
    path('to-vender-enter-money/<int:id>/', views.ToVenderEnterMoney, name='to-vender-enter-money'),  
    path('edit-buy-record/<int:id>/', views.editBuyRecord, name='edit-buy-record'),
    path('delete-buy-record/<int:id>/', views.deleteBuyRecord, name='delete-buy-record'),
    #------ find sell_unit  
    path('find-sell-unit',views.findSellUnit,name='find-sell-unit'), 
    #------ sell part  
    path('view-sell/',views.viewSell,name='view-sell'),   
    path('customer-accounts/<int:id>/',views.customerAccounts,name='customer-accounts'),  
    path('to-customer-enter-money/<int:id>/', views.ToCustomerEnterMoney, name='to-customer-enter-money'),
    path('add-sell/<int:id>/',views.addSell,name='add-sell'),
    path('sell-temporary-customer/',views.sellTemporaryCustomer,name='sell-temporary-customer'),
    path('print-customer-account/<int:id>/', views.printCustomerAccount, name='print-customer-account'),
    path('edit-sell-record/<int:id>/', views.editSellRecord, name='edit-sell-record'),
    path('delete-sell-record/<int:id>/', views.deleteSellRecord, name='delete-sell-record'),
]
