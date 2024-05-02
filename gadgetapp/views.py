from django.shortcuts import render,redirect,get_object_or_404
from .models import Gadget,ProfileUser,Cart,CartItems
from django.views import View
from .forms import GadgetForm,CustomUserRegistrationForm,NewsLetterForm
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import razorpay
from django.core.mail import send_mail
from GadgetHub.settings import EMAIL_HOST_USER





def home(request):
    
    return render(request, 'gadgetapp/home.html')



def register(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        

    else: 
        form = CustomUserRegistrationForm()

    return render(request, 'gadgetapp/register.html', {'form':form})




def user_login(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None :

            login(request, user)
            return redirect('home')
        
        else:

            pass

    return render(request, 'gadgetapp/login.html')



def user_logout(request):

    logout(request)
    return redirect('login')




class CategoryView(View):
    def get(self, request, val):
        gadget = Gadget.objects.filter(category=val)
        name = Gadget.objects.filter(category=gadget[0].category).values('name')
        return render(request, "gadgetapp/category.html", locals())
    
    
def all_gadgets(request):

    all_gadgets = Gadget.objects.all()

    return render(request, 'gadgetapp/all_gadget.html',{'all_gadgets': all_gadgets})

    

def create_gadget(request):

    if request.user.is_authenticated and request.user.role == 'owner':
        if request.method == 'POST':
            form = GadgetForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('create_gadget')

        else:

            form = GadgetForm()

        return render(request, 'gadgetapp/create_gadget.html',{'form': form})
    
    else:

        return redirect('home')




def gadget_detail(request, pk):

    gadget = get_object_or_404(Gadget, pk=pk)

    return render(request,'gadgetapp/gadget_detail.html', {'gadget': gadget})


def search_results(request):
    search_query = request.GET.get('search','')
    gadget = Gadget.objects.filter(Q(category__icontains=search_query)|Q(brand__icontains=search_query))

    return render(request,'gadgetapp/search_results.html',{'gadget':gadget, 'search_query':search_query} )



def edit_gadget(request, id):
    gadget = get_object_or_404(Gadget, id=id)
    
    if request.method == 'POST':
        form = GadgetForm(request.POST, instance=gadget)
        if form.is_valid():
            form.save()
            return redirect('all_gadgets')
    else:
        form = GadgetForm(instance=gadget)
    return render(request, 'gadgetapp/edit_gadget.html',{'form': form})
    

def delete_gadget(request, id):
    gadget = get_object_or_404(Gadget, id=id)
    gadget.delete()
    return redirect('all_gadgets')


def add_to_cart(request, pk):
    if request.method == 'POST':
        gadget = get_object_or_404(Gadget, pk=pk)
        quantity = int(request.POST.get('quantity',1))
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItems.objects.get_or_create(cart=cart, gadget=gadget, defaults = {'quantity':quantity})

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        else:
            cart_item.quantity = quantity
            cart_item.save()
        
        return redirect('cart')


def cart_view(request):
    cart_items = CartItems.objects.filter(cart__user=request.user)
    total_amount = sum(item.gadget.price*item.quantity for item in cart_items)
    return render(request, 'gadgetapp/cart.html', {'cart_items':cart_items ,'total_amount':total_amount})

def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItems, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')


def proceed_to_pay(request):
    cart_items = CartItems.objects.filter(cart__user=request.user)
    total_amount = sum(item.gadget.price * item.quantity for item in cart_items)
    return render(request, 'gadgetapp/proceed_to_pay.html',{'total_amount': total_amount})

@csrf_exempt
def payment_confirmation(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItems.objects.filter(cart=cart)
    
    total_amount = sum(item.gadget.price * item.quantity for item in cart_items)
    order_amount = (total_amount) * 100  # Converting to paisa (Razorpay requires amount in paisa)
    order_currency = 'INR'
    
    client = razorpay.Client(auth=(settings.RAZORPAY_TEST_KEY_ID, settings.RAZORPAY_TEST_KEY_SECRET))
    order = client.order.create({'amount': order_amount, 'currency': order_currency})

    # Assuming payment is successful, so clear the cart
    cart_items_data = []
    for item in cart_items:
        cart_items_data.append({
            'name': item.gadget.name,
            'quantity': item.quantity,
            'price': item.gadget.price
        })
    cart_items.delete()

    # Send email confirmation
    send_payment_confirmation_email(request.user, cart_items_data, total_amount)


    context = {
        'order_amount': order_amount,
        'order': order,
        'razorpay_key_id': settings.RAZORPAY_TEST_KEY_ID
    }
    return render(request, 'gadgetapp/payment_confirmation.html', context)

def send_payment_confirmation_email(user, cart_items_data, total_amount):
    subject = 'Payment Confirmation'
    message = f'Hi {user.username},\n\nYour payment has been successfully processed.Your Order is placed, Thank you for your purchase!\n\nPurchase Details:\n'
    for item in cart_items_data:
        message += f'- {item["name"]}: {item["quantity"]} x {item["price"]}\n'
    message += f'\nTotal Amount: {total_amount}'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=True)


def newsletter(request):


    if request.method == 'POST':
        form = NewsLetterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    else:

        form = NewsLetterForm()

    return render(request, 'gadgetapp/newsletter.html',{'form':form})








