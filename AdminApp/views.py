from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
from AdminApp.models import CategoryDb, ProductDb
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login


# Create your views here.
def dashboard(request):
    return render(request,"dashboard.html")
#*************************************************************************************************

def add_category(request):
    return render(request,"add_category.html")

def save_category(request):
    if request.method =="POST":
        cat_name = request.POST.get("cname")
        cat_desc = request.POST.get("desc")
        cat_img = request.FILES['img']
        obj = CategoryDb(Category_name=cat_name,Description=cat_desc,Category_images=cat_img)
        obj.save()
        return redirect(add_category)

def display_category(request):
    category=CategoryDb.objects.all()
    return render(request,"display_category.html",{"category":category})

def edit_category(request,cat_id):
    category = CategoryDb.objects.get(id=cat_id)
    return render(request,"edit_category.html",{"category":category})

def update_category(request,category_id):
    if request.method == "POST":
        cat_name = request.POST.get("cname")
        cat_desc = request.POST.get("desc")
        try:
            img = request.FILES['Category_images']
            fs = FileSystemStorage()
            file = fs.save(img.name,img)
        except MultiValueDictKeyError:
            file = CategoryDb.objects.get(id=category_id).Category_images
        CategoryDb.objects.filter(id=category_id).update(Category_name=cat_name,Description=cat_desc,Category_images=file)
        return redirect(display_category)

def delete_category(request,cat_id):
    data = CategoryDb.objects.filter(id=cat_id)
    data.delete()
    return redirect(display_category)
#*****************************************************************************************************************************

def admin_login_page(request):
    return render(request,"Admin_loginPage.html")

def admin_login(request):
    if request.method == "POST":
        uname= request.POST.get("username")
        paswrd = request.POST.get("password")
        if User.objects.filter(username__contains=uname).exists():
            data = authenticate(username=uname, password=paswrd)
            if data is not None:
                login(request, data)
                request.session['username'] = uname
                request.session['password'] = paswrd
                return redirect(dashboard)
            else:
                return redirect(admin_login_page)
        else:
            return redirect(admin_login_page)

def admin_logout(request):
        del request.session['username']
        del request.session['password']
        return redirect(admin_login_page)

#*******************************************************************************************************

def add_product(request):
    categories = CategoryDb.objects.all()
    return render(request,"add_product.html",{"categories":categories})

def display_product(request):
    product = ProductDb.objects.all()
    return render(request,"display_product.html",{"product":product})

def save_product(request):
    if request.method == "POST":
        cat_name = request.POST.get("cname")
        pro_name = request.POST.get("pname")
        price =  request.POST.get("price")
        overview =  request.POST.get("oview")

        author =  request.POST.get("aname")
        pro_img = request.FILES['img']
        obj = ProductDb(CategoryName=cat_name,Product_Name=pro_name,Price=price,Overview=overview
                        ,Author_Name=author,Product_img=pro_img)
        obj.save()

    return redirect(add_product)

def edit_product(request,pro_id):
    categories = CategoryDb.objects.all()
    products = ProductDb.objects.get(id=pro_id)
    return render(request,"edit_product.html",{"products":products,"categories":categories})

def delete_product(request,pro_id):
    data = ProductDb.objects.filter(id=pro_id)
    data.delete()
    return redirect(display_product)

def update_product(request,product_id):
    if request.method == "POST":
        cat_name = request.POST.get("cname")
        pro_name = request.POST.get("pname")
        price = request.POST.get("price")
        overview = request.POST.get("oview")

        author = request.POST.get("aname")
        try:
            img = request.FILES['Product_img']
            fs = FileSystemStorage()
            file = fs.save(img.name, img)
        except MultiValueDictKeyError:
            file = ProductDb.objects.get(id=product_id).Product_img

        ProductDb.objects.filter(id=product_id).update(CategoryName=cat_name,Product_Name=pro_name,
                                                       Price=price,Author_Name=author,Overview=overview,
                                                       Product_img=file)
        return redirect(display_product)