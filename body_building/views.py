from django.shortcuts import render
 
def loginPage(request):
    return render(request,'body_building/login.html',{})
