from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from AdminApp.models import CategoryDb, ProductDb
from WebApp.models import UserRegisterDb, CartDb, OrderDb
from django.contrib import messages
from django.conf import settings
import razorpay
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
    categories = CategoryDb.objects.all()
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

    return render(request,"cart.html",{"products":products,"subtotal":subtotal,"total":total,"delivery":delivery,"categories":categories})

def save_cart(request):
    if request.method == "POST":
        uname = request.POST.get("uname")
        pro_name = request.POST.get("pro_name")
        qnty = request.POST.get("quantity")
        total_price = request.POST.get("total")
        price = request.POST.get("price")
        obj = CartDb(Username=uname,Price=price,Quantity=qnty,Total_price=total_price,Product_Name=pro_name)
        obj.save()
        messages.success(request,"Item Added Successfully")
        return redirect(home_page)

def delete_cart_item(request,pro_id):
    data = CartDb.objects.filter(id=pro_id)
    data.delete()
    messages.success(request,"Item removed from  your cart ")
    return redirect(cart_page)

def filtered_product(request,cat_name):
    product = ProductDb.objects.filter(CategoryName=cat_name).all()
    categories = CategoryDb.objects.all()
    products = ProductDb.objects.all()
    return render(request,"filtered_product.html",{"categories":categories,"product":product,"products":products})

def single_product(request,pro_id):
    products = ProductDb.objects.filter(id=pro_id)
    categories = CategoryDb.objects.all()
    return render(request,"single_product.html",{"products":products,"categories":categories})

def contact_page(request):
    categories = CategoryDb.objects.all()
    return render(request,"contact.html",{"categories":categories})

def checkout_page(request):
    categories = CategoryDb.objects.all()
    username = request.session.get('Username')
    products = CartDb.objects.filter(Username=username) if username else CartDb.objects.none()
    subtotal = 0
    delivery = 0
    total = 0

    for item in products:
        subtotal += item.Total_price or 0

    if subtotal:
        if subtotal > 2000:
            delivery = 0
        elif subtotal > 1000:
            delivery = 50
        else:
            delivery = 100

    total = subtotal + delivery

    if request.method == "POST":
        form_username = request.POST.get("username") or username

        if not form_username:
            messages.error(request, "Please login to place your order.")
            return redirect(login_page)

        if not products.exists():
            messages.error(request, "Your cart is empty.")
            return redirect(cart_page)

        obj = OrderDb(
            Username=form_username,
            Full_name=request.POST.get("full_name"),
            Place=request.POST.get("place"),
            Email=request.POST.get("email"),
            Address=request.POST.get("address"),
            Pincode=request.POST.get("pincode") or None,
            Message=request.POST.get("message"),
            Mobile=request.POST.get("mobile") or None,
            Total_price=str(total),
        )
        obj.save()
        return redirect('payment')

    return render(request, "checkout.html", {
        "categories": categories,
        "products": products,
        "subtotal": subtotal,
        "delivery": delivery,
        "total": total,
        "username": username or "",
    })


def get_razorpay_client():
    razorpay_key_id = getattr(settings, "RAZORPAY_KEY_ID", "rzp_test_0ib0jPwwZ7I1lT")
    razorpay_key_secret = getattr(settings, "RAZORPAY_KEY_SECRET", "VjHNO5zKeKxz8PYe7VnzwxMR")
    return razorpay.Client(auth=(razorpay_key_id, razorpay_key_secret))


def payment_page(request, order_id=None):
    categories = CategoryDb.objects.all()
    for category in categories:
        count = ProductDb.objects.filter(CategoryName=category.Category_name).count()
        category.product_count = count

    username = request.session.get('Username')
    customer = OrderDb.objects.filter(Username=username).order_by('-id').first()

    if customer is None:
        messages.error(request, "Please place an order before continuing to payment.")
        return redirect(checkout_page)

    if customer.Payment_status == "Paid":
        messages.success(request, "This order has already been paid successfully.")
        return redirect(home_page)

    try:
        total_price = int(float(customer.Total_price))
    except (TypeError, ValueError):
        messages.error(request, "Invalid order total found. Please place the order again.")
        return redirect(checkout_page)

    amount = total_price * 100
    razorpay_key_id = getattr(settings, "RAZORPAY_KEY_ID", "rzp_test_0ib0jPwwZ7I1lT")
    razorpay_key_secret = getattr(settings, "RAZORPAY_KEY_SECRET", "VjHNO5zKeKxz8PYe7VnzwxMR")

    try:
        client = get_razorpay_client()
        if customer.Razorpay_order_id and customer.Payment_status == "Pending":
            payment_order_id = customer.Razorpay_order_id
        else:
            razorpay_order = client.order.create({
                "amount": amount,
                "currency": "INR",
                "payment_capture": "1",
            })
            payment_order_id = razorpay_order["id"]
            customer.Razorpay_order_id = payment_order_id
            customer.Payment_status = "Initiated"
            customer.save(update_fields=["Razorpay_order_id", "Payment_status"])
    except Exception:
        messages.error(request, "Razorpay is not configured properly. Please add valid Razorpay keys.")
        return redirect(home_page)

    context = {
        "categories": categories,
        "customer": customer,
        "order": customer,
        "display_amount": total_price,
        "amount": amount,
        "amount_paise": amount,
        "razorpay_key_id": razorpay_key_id,
        "payment_order_id": payment_order_id,
        "payment_success_url": reverse("payment_success"),
        "payment_failed_url": reverse("payment_failed"),
    }
    return render(request, "payment.html", context)


def payment_success(request):
    if request.method != "POST":
        messages.error(request, "Invalid payment response.")
        return redirect('payment')

    razorpay_payment_id = request.POST.get("razorpay_payment_id")
    razorpay_order_id = request.POST.get("razorpay_order_id")
    razorpay_signature = request.POST.get("razorpay_signature")

    order = OrderDb.objects.filter(Razorpay_order_id=razorpay_order_id).order_by("-id").first()
    if order is None:
        messages.error(request, "Order not found for this payment.")
        return redirect('checkout')

    razorpay_key_id = getattr(settings, "RAZORPAY_KEY_ID", "rzp_test_0ib0jPwwZ7I1lT")
    razorpay_key_secret = getattr(settings, "RAZORPAY_KEY_SECRET", "VjHNO5zKeKxz8PYe7VnzwxMR")
    client = razorpay.Client(auth=(razorpay_key_id, razorpay_key_secret))

    try:
        client.utility.verify_payment_signature({
            "razorpay_order_id": razorpay_order_id,
            "razorpay_payment_id": razorpay_payment_id,
            "razorpay_signature": razorpay_signature,
        })
    except razorpay.errors.SignatureVerificationError:
        order.Payment_status = "Failed"
        order.Razorpay_payment_id = razorpay_payment_id
        order.Razorpay_signature = razorpay_signature
        order.save(update_fields=["Payment_status", "Razorpay_payment_id", "Razorpay_signature"])
        messages.error(request, "Payment verification failed. Please try again.")
        return redirect('payment')

    order.Payment_status = "Paid"
    order.Razorpay_payment_id = razorpay_payment_id
    order.Razorpay_signature = razorpay_signature
    order.save(update_fields=["Payment_status", "Razorpay_payment_id", "Razorpay_signature"])

    CartDb.objects.filter(Username=order.Username).delete()
    messages.success(request, "Payment successful. Your order has been confirmed.")
    return redirect(home_page)


def payment_failed(request):
    razorpay_order_id = request.GET.get("order_id")
    order = OrderDb.objects.filter(Razorpay_order_id=razorpay_order_id).order_by("-id").first()
    if order is not None and order.Payment_status != "Paid":
        order.Payment_status = "Failed"
        order.save(update_fields=["Payment_status"])

    messages.error(request, "Payment was cancelled or failed. Please try again.")
    return redirect('payment')
