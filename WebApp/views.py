from django.shortcuts import render, redirect
from AdminApp.models import CategoryDb, ProductDb
from WebApp.models import UserRegisterDb, CartDb
from django.contrib import messages
# Create your views here.
#******************************************************************
def register_page(request):
    return render(request,"register.html")

def login_page(request):
    return render(request,"login.html")

def save_user(request):
    if request.method == "POST":
        uname = request.POST.get("uname")
        email = request.POST.get("email")
        pswrd = request.POST.get("password")
        con_pass = request.POST.get("con_pass")
        if UserRegisterDb.objects.filter(Username=uname).exists():
            messages.error(request,"Username already exist")
            return redirect(register_page)
        elif UserRegisterDb.objects.filter(Email=email).exists():
            messages.error(request, "Email already exist")
            return redirect(register_page)
        else:
            obj=UserRegisterDb(Username=uname,Email=email,Password=pswrd,Confirm_password=con_pass)
            obj.save()
            return redirect(register_page)

def user_login(request):
    if request.method == "POST":
        uname = request.POST.get("uname")
        pswrd = request.POST.get("password")
        if UserRegisterDb.objects.filter(Username=uname, Password=pswrd).exists():
            request.session['Username'] = uname
            request.session['Password'] = pswrd
            messages.success(request,"Welcome to BookZone")
            return redirect(home_page)
        else:
            return redirect(login_page)

def user_logout(request):
    del request.session['Username']
    del request.session['Password']
    return redirect(home_page)

#***************************************************************************
def home_page(request):
    categories = CategoryDb.objects.all()
    products = ProductDb.objects.all()
    new_arrivals = ProductDb.objects.order_by('-id')[:8]
    return render(request,"home.html",{"new_arrivals":new_arrivals,"categories":categories,"products":products})

def about_page(request):
    categories = CategoryDb.objects.all()
    return render(request,"about.html",{"categories":categories})

def all_products(request):
    products = ProductDb.objects.all()
    categories = CategoryDb.objects.all()
    return render(request,"all_products.html",{"products":products,"categories":categories})

def cart_page(request):
    products = CartDb.objects.filter(Username=request.session['Username'])
    subtotal = 0
    delivery = 0
    total = 0
    for i in products:
        subtotal +=  i.Total_price

        if subtotal > 2000:
            delivery = 0
        elif subtotal >1000:
            delivery = 50
        else:
            delivery = 100

        total = subtotal + delivery

    return render(request,"cart.html",{"products":products,"subtotal":subtotal,"total":total,"delivery":delivery})

def save_cart(request):
    if request.method == "POST":
        uname = request.POST.get("uname")
        pro_name = request.POST.get("pro_name")
        qnty = request.POST.get("quantity")
        total_price = request.POST.get("total")
        price = request.POST.get("price")
        obj = CartDb(Username=uname,Price=price,Quantity=qnty,Total_price=total_price,Product_Name=pro_name)
        obj.save()
        return redirect(home_page)

def delete_cart_item(request,pro_id):
    data = CartDb.objects.filter(id=pro_id)
    data.delete()
    return redirect(cart_page)

def filtered_product(request,cat_name):
    product = ProductDb.objects.filter(CategoryName=cat_name).all()
    categories = CategoryDb.objects.all()
    products = ProductDb.objects.all()
    return render(request,"filtered_product.html",{"categories":categories,"product":product,"products":products})

def single_product(request,pro_id):
    products = ProductDb.objects.filter(id=pro_id)
    return render(request,"single_product.html",{"products":products})

def contact_page(request):
    categories = CategoryDb.objects.all()
    return render(request,"contact.html",{"categories":categories})

def checkout_page(request):
    return render(request,"checkout.html")

