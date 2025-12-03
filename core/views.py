from django.http import HttpResponseForbidden
from django.shortcuts import render , get_object_or_404, redirect
from .models import Painting, Category, Cart, CartItem, Order, OrderItem
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime 
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.db.models import Sum, F
from django.db.models.functions import TruncMonth
from django.http import JsonResponse
import calendar
import json
from collections import OrderedDict
import datetime



# Create your views here.


@login_required
def generate_invoice(request, order_id):

    # Get the order, or return a 404 if not found or if it doesn't belong to the user
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    
    # Get all order items related to this order
    order_items = order.orderitem_set.all()

    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'invoice_detail.html', context)






@login_required
def profile_update(request):
    user = request.user

    # Check if the user has a profile
    try:
        profile = user.profile  # Access related profile
        has_profile = True
    except Profile.DoesNotExist:
        profile = None
        has_profile = False

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        password_form = PasswordChangeForm(user, request.POST)

        if has_profile:
            profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        
        if 'update_user' in request.POST and user_form.is_valid():
            user_form.save()
            if has_profile and profile_form.is_valid():
                profile_form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile_update')

        elif 'update_password' in request.POST and password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Prevent logout after password change
            messages.success(request, "Password updated successfully.")
            return redirect('profile_update')

    else:
        user_form = UserUpdateForm(instance=user)
        password_form = PasswordChangeForm(user)
        profile_form = ProfileUpdateForm(instance=profile) if has_profile else None

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'password_form': password_form,
        'has_profile': has_profile  # Flag to check in the template
    }

    return render(request, 'profile_update.html', context)




@login_required
def profile(request):
    categorys = Category.objects.all()
    return render(request, 'user dashboard.html', {'user': request.user, 'categorys':categorys})

# @login_required
# def seller_dashboard(request):
#     return render(request, 'sellar dashboard.html', {'user': request.user})



@login_required
def seller_dashboard(request):

    if hasattr(request.user, 'profile') and request.user.profile.is_seller:


        listed_paintings = Painting.objects.filter(seller=request.user)
        listing_no = listed_paintings.count()   

        seller = request.user 
        # ordered_items = Order.objects.filter(orderitem__painting__seller=seller).distinct()

        orders = Order.objects.filter(orderitem__painting__seller=seller, status="Placed").distinct()
        ordered_items = OrderItem.objects.filter(painting__seller=seller)

          # Filter order items of this seller
        seller_order_items = OrderItem.objects.filter(painting__seller=seller)

        # Revenue grouped by month
        monthly_data = (
            seller_order_items
            .annotate(month=TruncMonth('order__date_ordered'))
            .values('month')
            .annotate(total=Sum('painting__price'))
            .order_by('month')
        )

        # Create a dictionary of all months with 0 initially
        current_year = datetime.date.today().year
        all_months = OrderedDict((calendar.month_name[i], 0) for i in range(1, 13))

        for entry in monthly_data:
            month_name = entry['month'].strftime('%B')
            all_months[month_name] = float(entry['total'])

        chart_labels = list(all_months.keys())
        chart_data = list(all_months.values())

        context = {
            'chart_labels': json.dumps(chart_labels),
            'chart_data': json.dumps(chart_data),
            'listed_paintings': Painting.objects.filter(seller=seller),
            'orders': Order.objects.filter(orderitem__painting__seller=seller).distinct(),
            'listing_no': Painting.objects.filter(seller=seller).count(),
            'orders_no': seller_order_items.values('order').distinct().count()
        }
        


        return render(request, 'sellar dashboard.html', context)
    

    return HttpResponseForbidden("You are not authorized to access this page.")




def category(request, pk):
    
    categorys = Category.objects.all()
    
    category = Category.objects.get(id = pk)
    
    painting = Painting.objects.filter(category=category )
   
    return render(request, "category.html", {'painting':painting, 'category':category, 'categorys':categorys})
    


def search_paintings(request):
    query = request.GET.get('q', '') 
    if query:
        
        results = Painting.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    else:
        results = Painting.objects.all()  

    
    return render(request, 'searches.html', {'results': results, 'query': query})

def home(request):
    # messages.success(request, "welcome to home")

    categorys = Category.objects.all()
    new= Painting.objects.order_by('?')[:5] 
    best = Painting.objects.get(title="Serenity by the Lake")
    return render(request, "home.html", { 'best': best , 'new': new , 'user': request.user, 'categorys':categorys})


def about(request):
    categorys = Category.objects.all()
    return render(request, "about.html",{'categorys':categorys})


def contact(request):
    categorys = Category.objects.all()
    context = {}

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        if email and name and message:
            
            current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S") 

            email_message = (
                f"Date & Time: {current_time}\n"
                f"Name: {name}\n"
                f"Email: {email}\n"
                f"Phone: {phone}\n\n"
                f"Message:\n{message}"
            )

            try:
                send_mail(
                    subject="E-commerce Contact Form",
                    message=email_message,
                    from_email=email, 
                    recipient_list=[settings.EMAIL_HOST_USER], 
                    fail_silently=False
                )
                context['result'] = 'Email sent successfully'
            except Exception as e:
                context['result'] = f'Error sending email: {e}'
        else:
            context['result'] = 'All fields are required'

    return render(request, "contact.html", {'categorys':categorys})



# def login_user(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username= username, password=password)
#         if user is not None:
#             login(request, user)
#             return render(request, "user dashboard.html" , {'user':user})
#         else:
#             return redirect('login')
#     else:
#         return render(request, "login.html")


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        categorys = Category.objects.all()
        
        if user is not None:
            login(request, user)

            if hasattr(user, 'profile') and user.profile.is_seller:  
                # return render(request, "sellar dashboard.html" , {'user':user})
                return redirect(seller_dashboard)

            else:
                return render(request, "user dashboard.html" , {'user':user, 'categorys':categorys})
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')  
    return render(request, "login.html")



    

def logout_user(request):
    logout(request)
    return redirect('home')

def signup_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                
               
                login(request, user)
                
                messages.success(request, "Account created successfully!")
                return redirect('home')
            else:
                messages.error(request, "Username already taken.")
        else:
            messages.error(request, "Passwords do not match.")
    
    return render(request, 'signup.html')



def register_seller(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        display_name = request.POST.get('display_name')
        profile_picture = request.FILES.get('photo')
        
        if password == confirm_password:
            if not User.objects.filter(username=username).exists():
                if not Profile.objects.filter(display_name=display_name).exists():
                    user = User.objects.create_user(username=username, email=email, password=password)
                    Profile.objects.create(user=user, is_seller=True, display_name=display_name,    profile_picture=profile_picture)
                    login(request, user)
                    return redirect('home')
                else:
                    return render(request, 'register_seller.html', {'error': 'Display name already taken.'})
            else:
                return render(request, 'register_seller.html', {'error': 'Username already exists.'})
        else:
            return render(request, 'register_seller.html', {'error': 'Passwords do not match.'})
    
    return render(request, 'register_seller.html')




def base(request):
    return render(request, "base.html")

def product(request, pk):
    painting = Painting.objects.get(id = pk)
    return render(request, "product.html", {'painting': painting})

@login_required
def add_to_cart(request, painting_id):
    painting = get_object_or_404(Painting, id=painting_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, painting=painting)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('view_cart')



@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('view_cart')

@login_required
def view_cart(request):
    
    cart, created = Cart.objects.get_or_create( user=request.user)
    

    cart_items = cart.cartitem_set.all()  
    total_price = sum(item.painting.price * item.quantity for item in cart_items)
    
    
    return render(request, 'cart.html', {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': total_price
    })


def clearall(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart.cartitem_set.all().delete()
    return redirect('view_cart')

# def checkout(request):
#     cart = get_object_or_404(Cart, user=request.user)
#     cart_items = cart.cartitem_set.all()
#     total_price = sum(item.painting.price * item.quantity for item in cart_items)

#     if request.method == 'POST':
        
#         address = request.POST['address']
#         city = request.POST['city']
#         state = request.POST['state']
#         zip_code = request.POST['zip']


#         order = Order.objects.create(
#             user=request.user,
#             shipping_address=address,
#             shipping_city=city,
#             shipping_state=state,
#             shipping_zip=zip_code
#         )

#         for cart_item in cart_items:
#             OrderItem.objects.create(
#                 order=order,
#                 painting=cart_item.painting,
#                 quantity=cart_item.quantity
#             )

#         # Clear the cart after placing the order
#         cart.cartitem_set.all().delete()


#         return redirect('order_confirmation', order_id=order.id)

#     return render(request, 'checkout.html', {'cart_items': cart_items, 'total_price':total_price})


def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.cartitem_set.all()


    total_price = sum(item.painting.price * item.quantity for item in cart_items)


    if request.method == 'POST':
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        zip_code = request.POST['zip']

        for cart_item in cart_items:
            # Create a separate order for each painting
            order = Order.objects.create(
                user=request.user,
                shipping_address=address,
                shipping_city=city,
                shipping_state=state,
                shipping_zip=zip_code
            )

            # Create an OrderItem for this order
            OrderItem.objects.create(
                order=order,
                painting=cart_item.painting,
                quantity=cart_item.quantity
            )

        # Clear the cart after placing orders
        cart.cartitem_set.all().delete()

        return redirect('order_confirmation_list')  # Redirect to a list of all orders

    return render(request, 'checkout.html', {'cart_items': cart_items, 'total_price':total_price})



@login_required
def order_confirmation_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-date_ordered')
    return render(request, 'order_confirmation.html', {'orders': orders})


@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = order.orderitem_set.all()
    
    return render(request, 'order_confirmation.html', {'order': order, 'order_items': order_items})

# @login_required
# def view_orders(request):
    
#     orders = Order.objects.filter(user=request.user).order_by('-date_ordered')
    
#     return render(request, 'orders.html', {'orders': orders})

@login_required
def view_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-date_ordered')
    
    return render(request, 'orders.html', {'orders': orders})



@login_required
def direct_order(request, painting_id):
    painting = get_object_or_404(Painting, id=painting_id)

    if request.method == 'POST':
        

        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        zip_code = request.POST['zip']


        order = Order.objects.create(
            user=request.user,
            shipping_address=address,
            shipping_city=city,
            shipping_state=state,
            shipping_zip=zip_code
        )


        order_item = OrderItem.objects.create(order=order, painting=painting, quantity=1)
        

        order.complete = True
        # order.total_price = order_item.get_total()
        order.save()


        return redirect('order_confirmation', order_id=order.id)

    return render(request, 'direct_order.html', {'painting': painting})

@login_required
def mark_as_shipped(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # Get only the seller's order items
    seller_items = order.orderitem_set.filter(painting__seller=request.user)

    if not seller_items.exists():
        return HttpResponseForbidden("You are not authorized to update this order.")

    # Check if all the seller's items in this order are shipped
    for item in seller_items:
        item.order.status = "Shipped"
        item.order.save()

    return redirect('seller_orders')  

@login_required
def mark_as_delivered(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # Ensure the seller owns the order items
    seller_items = order.orderitem_set.filter(painting__seller=request.user)

    if not seller_items.exists():
        return HttpResponseForbidden("You are not authorized to update this order.")

    # Update order status to 'Delivered' only if it's currently 'Shipped'
    if order.status == "Shipped":
        order.status = "Delivered"
        order.save()

    return redirect('seller_orders')  # Redirect back to seller dashboard

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.status in ['Placed', 'Received']:  # Can be cancelled only if not shipped
        order.status = 'Cancelled'
        order.save()
        messages.success(request, "Your order has been cancelled successfully.")
    else:
        messages.error(request, "You cannot cancel this order as it is already shipped or delivered.")

    return redirect('view_orders')




@login_required
def seller_product(request):
    if hasattr(request.user, 'profile') and request.user.profile.is_seller:
        if request.method == 'POST':
            title = request.POST['title']
            description = request.POST['description']
            category_id = request.POST['category']
            image = request.FILES['image']
            price = request.POST['price']

            category = get_object_or_404(Category, id=category_id)

            painting = Painting.objects.create(
                title=title,
                description=description,
                category=category,
                image=image,
                price=price,
                seller=request.user,
                is_selling=True
            )
            return redirect('seller_product')

        listed_paintings = Painting.objects.filter(seller=request.user)

        categories = Category.objects.all()
        return render(request, 'seller product.html', {'categories': categories, 'listed_paintings': listed_paintings,})

        
    return HttpResponseForbidden("You are not authorized to access this page.")



@login_required
def delete_painting(request, painting_id):
    painting = get_object_or_404(Painting, id=painting_id, seller=request.user) 
    painting.delete()
    messages.success(request, "Painting deleted successfully.")
    return redirect('seller_product') 




@login_required
def seller_orders(request):
    seller = request.user  

    orders = Order.objects.filter(orderitem__painting__seller=seller).distinct()
    for order in orders:
        seller_total = order.orderitem_set.filter(painting__seller=seller).aggregate(
            total=Sum(F('quantity') * F('painting__price'))
        )['total'] or 0  # Default to 0 if None
        
        order.seller_total = seller_total

    context = {
        'orders': orders
    }
    return render(request, 'seller orders.html', context)

@login_required
def seller_customer(request):
    seller = request.user  

    orders = Order.objects.filter(orderitem__painting__seller=seller).distinct()

    customers = User.objects.filter(order__orderitem__painting__seller=seller).distinct()

    context = {
        'orders': orders,
        'customers':customers

    }
    return render(request, 'seller customer.html', context)


@login_required
def seller_order_detail(request, order_id):
    # order = get_object_or_404(Order, id=order_id)

    # seller_paintings = order.orderitem_set.filter(painting__seller=request.user)

    seller = request.user
    seller_paintings = OrderItem.objects.filter(order__id=order_id, painting__seller=seller)

    if not seller_paintings.exists():
        return HttpResponseForbidden("You do not have permission to view this order.")
    seller_total = sum(item.get_total() for item in seller_paintings)

    order = seller_paintings.first().order  

    context = {
        'order': order,
        'order_items': seller_paintings,
        'seller_total': seller_total
    }
    return render(request, 'seller order detail.html', context)


# @login_required
# def monthly_revenue_data(request):
#     seller = request.user

#     # Filter OrderItems where the painting's seller is the logged-in seller and order is delivered
#     revenue_data = (
#         OrderItem.objects
#         .filter(painting__seller=seller, order__status='Delivered')
#         .annotate(month=TruncMonth('order__date_ordered'))
#         .values('month')
#         .annotate(revenue=Sum('painting__price'))
#         .order_by('month')
#     )

#     # Convert queryset to JSON-friendly format
#     data = {
#         'labels': [item['month'].strftime('%B %Y') for item in revenue_data],
#         'revenue': [float(item['revenue']) for item in revenue_data],
#     }
#     return JsonResponse(data)