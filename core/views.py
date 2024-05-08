from django.shortcuts import render,redirect,get_object_or_404
from .models import UserProfile
from .forms import *
from .models import *
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash

from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from django.urls import reverse

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        mobiles = Mobile.objects.all()
        return render(request, 'core/home.html', {'x': request.user, 'mobiles': mobiles})
    else:
        return redirect('login')
    
def log_in(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            mf = CustomAuthenticationForm(request, request.POST)
            if mf.is_valid():
                name = mf.cleaned_data['username']
                pas = mf.cleaned_data['password']
                user = authenticate(username=name, password=pas)
                if user is not None:
                    login(request, user)
                    return redirect('/home/')
        else:
            mf = CustomAuthenticationForm()
        return render(request, 'core/login.html', {'mf': mf})
    else:
        return redirect('/home/')
    
def sign_up(request):
    if request.method == 'POST':
        mf = SignupForm(request.POST)
        if mf.is_valid():
            mf.save()
            return redirect('login')    
    else:
        mf  = SignupForm()
    return render(request,'core/signup.html',{'mf':mf})

def log_out(request):
    logout(request)
    return redirect('login')

def profile(request):
    if request.user.is_authenticated:
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        if request.method == 'POST':
            if request.user.is_superuser:
                mf = AdminprofileForm(request.POST, request.FILES, instance=request.user)
            else:
                mf = UserprofileForm(request.POST, request.FILES, instance=request.user)
            if mf.is_valid():
                mf.save()
                user_profile.phone_number = mf.cleaned_data['phone_number']
                user_profile.profile_pic = mf.cleaned_data['profile_pic']
                user_profile.save()
        else:
            initial_data = {'phone_number': user_profile.phone_number, 'profile_pic': user_profile.profile_pic}
            if request.user.is_superuser:
                mf = AdminprofileForm(instance=request.user, initial=initial_data)
            else:
                mf = UserprofileForm(instance=request.user, initial=initial_data)
        return render(request, 'core/profile.html', {'x': request.user, 'mf': mf})
    else:
        return redirect('login')
    
def pcf(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            mf = CustomPasswordChangeForm(request.user,request.POST)
            if mf.is_valid():
                mf.save()
                update_session_auth_hash(request,mf.user)
                return redirect('/home/')
        else:
            mf = CustomPasswordChangeForm(request.user)
        return render(request,'core/pcf.html',{'mf':mf})
    else:
        return redirect('login')
    
def productlisting(request):
    if request.user.is_authenticated:
        mobile_detail = Mobile.objects.all()
        return render(request, 'core/productlistingmobile.html',{'x': request.user, 'y': mobile_detail})
    else:
        return redirect('/home/')
    
def productview(request, id):
    if request.user.is_authenticated:
        mobile_detail = get_object_or_404(Mobile, pk=id)
        colors = Color.objects.all()
        return render(request, 'core/productview.html', {'y': mobile_detail, 'x': request.user, 'colors': colors})
    else:
        return redirect('/home/')
    
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)      
    total =0
    delhivery_charge = 0
    money_saved = 0
    for item in cart_items:
        item.product.price_and_quantity_total = item.product.discounted_price * item.quantity
        total += item.product.price_and_quantity_total
        money_saved += (item.product.selling_price - item.product.discounted_price) * item.quantity
        if total >= 20000:
            delhivery_charge = 0
        else:
            delhivery_charge = 2000
    final_price= delhivery_charge + total
    return render(request, 'core/cart.html', {'x': request.user,'cart_items': cart_items,'total':total,'final_price':final_price,
                                               'money_saved':money_saved, 'delhivery_charge':delhivery_charge})
    
def add_to_cart(request, id):    
    if request.user.is_authenticated:
        product = Mobile.objects.get(pk=id) 
        user=request.user               
        Cart(user=user,product=product).save()  
        return redirect('productview', id)       
    else:
        return redirect('login')

def add_quantity(request, id):
    product = get_object_or_404(Cart, pk=id)    
    product.quantity += 1                          
    product.save()
    return redirect('viewcart')

def delete_quantity(request, id):
    product = get_object_or_404(Cart, pk=id)
    if product.quantity > 1:
        product.quantity -= 1
        product.save() 
    return redirect('viewcart')

def delete_cart(request,id):
    if request.method == 'POST':
        de = Cart.objects.get(pk=id)
        de.delete()
    return redirect('viewcart')

def address(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('address')           
    else:
        form = CustomerForm()
        addresses = Customer.objects.filter(user=request.user)
    return render(request, 'core/address.html', {'form': form, 'addresses': addresses, 'x': request.user})

def delete_address(request, id):
    if request.method == 'POST':
        address = Customer.objects.get(pk=id)
        address.delete()
    return redirect('address')

def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)      
    total =0
    delhivery_charge = 0
    money_saved = 0
    for item in cart_items:
        item.product.price_and_quantity_total = item.product.discounted_price * item.quantity
        total += item.product.price_and_quantity_total
        money_saved += (item.product.selling_price - item.product.discounted_price) * item.quantity
        if total >= 20000:
            delhivery_charge = 0
        else:
            delhivery_charge = 2000
    final_price= delhivery_charge + total
    
    addresses = Customer.objects.filter(user=request.user)

    return render(request, 'core/checkout.html', {'cart_items': cart_items,'total':total,'final_price':final_price,'addresses':addresses,
                                                  'money_saved':money_saved, 'delhivery_charge':delhivery_charge})


def payment(request):
    if request.method == 'POST':
        selected_address_id = request.POST.get('selected_address')  

    cart_items = Cart.objects.filter(user=request.user)      
    total =0
    delhivery_charge = 0
    money_saved = 0
    for item in cart_items:
        item.product.price_and_quantity_total = item.product.discounted_price * item.quantity
        total += item.product.price_and_quantity_total
        money_saved += (item.product.selling_price - item.product.discounted_price) * item.quantity
        if total >= 20000:
            delhivery_charge = 0
        else:
            delhivery_charge = 2000
    final_price= delhivery_charge + total
    
    addresses = Customer.objects.filter(user=request.user)
    
    host = request.get_host()   
    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': final_price,
        'item_name': 'mobile',
        'invoice': uuid.uuid4(),
        'currency_code': 'USD',
        'notify_url': f"http://{host}{reverse('paypal-ipn')}",
        'return_url': f"http://{host}{reverse('paymentsuccess', args=[selected_address_id])}",
        'cancel_url': f"http://{host}{reverse('paymentfailed')}",
    }
    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

    return render(request, 'core/payment.html', {'cart_items': cart_items,'total':total,'final_price':final_price,'addresses':addresses,
                                                  'money_saved':money_saved, 'delhivery_charge':delhivery_charge, 'paypal':paypal_payment})

def payment_success(request,selected_address_id):
    user =request.user
    customer_data = Customer.objects.get(pk=selected_address_id,)
    cart = Cart.objects.filter(user=user)
    final_price=0
    for c in cart:
        final_price = c.product.discounted_price * c.quantity
        Order(user=user, customer=customer_data, mobile=c.product, quantity=c.quantity, final_price=final_price).save()
        c.delete()
    return render(request,'core/payment_success.html')

def payment_failed(request):
    return render(request,'core/payment_failed.html')

def order(request):
    ord=Order.objects.filter(user=request.user)
    return render(request,'core/order.html',{'ord':ord, 'x': request.user})

def buynow(request, id):
    mobile = Mobile.objects.get(pk=id)     
    delhivery_charge = 2000  # Default delivery charge
    total = mobile.discounted_price
    money_saved = mobile.selling_price - mobile.discounted_price
    if total >= 20000:
        delhivery_charge = 0
    final_price = delhivery_charge + total
    addresses = Customer.objects.filter(user=request.user)
    return render(request, 'core/buynow.html', {'final_price': final_price, 'total': total, 'addresses': addresses, 'mobile': mobile, 'money_saved': money_saved, 'delhivery_charge': delhivery_charge})

def buynow_payment(request,id):
    if request.method == 'POST':
        selected_address_id = request.POST.get('buynow_selected_address')

    mobile = Mobile.objects.get(pk=id) 
    delhivery_charge =2000
    final_price= delhivery_charge + mobile.discounted_price
    address = Customer.objects.filter(user=request.user)

    host = request.get_host()   
    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': final_price,
        'item_name': 'mobile',
        'invoice': uuid.uuid4(),
        'currency_code': 'USD',
        'notify_url': f"http://{host}{reverse('paypal-ipn')}",
        'return_url': f"http://{host}{reverse('buynowpaymentsuccess', args=[selected_address_id,id])}",
        'cancel_url': f"http://{host}{reverse('paymentfailed')}",
    }
    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

    return render(request, 'core/payment.html', {'final_price':final_price,'addresses':address,'mobile':mobile,'paypal':paypal_payment})

def buynow_payment_success(request,selected_address_id,id):
    user =request.user
    customer_data = Customer.objects.get(pk=selected_address_id,)
    mobile = Mobile.objects.get(pk=id)
    final_price= mobile.discounted_price + 2000
    Order(user=user,customer=customer_data,mobile=mobile,quantity=1,final_price=final_price).save()
    return render(request,'core/payment_success.html')