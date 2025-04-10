from django.shortcuts import render, redirect,get_object_or_404
from .models import Vehicles, Category, Contact, Add, Payment,Review,Rider
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login,logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import logging
logger=logging.getLogger('django')
def index(request):
    cate = Category.objects.all()
    cateid = request.GET.get('category')
    if cateid:
        data = Vehicles.objects.filter(Category=cateid)
    else:
        data = Vehicles.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        if not name:
            messages.error(request, 'Name is required!')
        elif not email:
            messages.error(request, 'Email is required!')
        elif not phone:
            messages.error(request, 'Phone is required!')
        elif not message:
            messages.error(request, 'Message is required!')
        else:
            Contact.objects.create(name=name, email=email, phone=phone, message=message)
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('index')  
    context = {
        'data': data,
        'cate': cate,
    }
    return render(request, 'vehicle/index.html', context)
def services(request):
    return render(request, 'vehicle/services.html')
def ride(request):
    if request.method == 'POST':
        full_name = request.POST.get('field1')
        address = request.POST.get('field2')
        email = request.POST.get('field3')
        phone_number = request.POST.get('field4')
        location = request.POST.get('field5')
        time = request.POST.get('time')
        date = request.POST.get('date')
        terms_accepted = request.POST.get('field7')
        if not full_name or not address or not email or not phone_number or not location or not time or not date:
            messages.error(request, "Please fill out all required fields.")
            return redirect('ride')
        if not terms_accepted:
            messages.error(request, "You must agree to the terms and conditions.")
            return redirect('ride') 
        rider = Rider(
            full_name=full_name,
            address=address,
            email=email,
            phone_number=phone_number,
            location=location,
            time=time,
            date=date,
        )
        rider.save()
        messages.success(request, "Your details have been submitted successfully!")
        return redirect('ride')  
        
    return render(request, 'vehicle/ride.html')
def about(request):
    return render(request, 'vehicle/about.html')
@login_required(login_url='log_in')
def contactus(request):
    return render(request, 'vehicle/contactus.html')
def review(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        rating = request.POST.get('rating')  
        review_text = request.POST.get('review_text')
        if not rating:
            messages.error(request, "Please select a rating.")
            return redirect('review')
        review = Review(name=name, email=email, rating=rating, review_text=review_text)
        review.save()
        messages.success(request, "Thank you for your review!")
        return redirect('review')  
    reviews = Review.objects.all()
    return render(request, 'vehicle/review.html', {'reviews': reviews})
def policy(request):
    return render(request, 'vehicle/policy.html')
def risk(request):
    return render(request, 'vehicle/risk.html')
def terms(request):
    return render(request, 'vehicle/terms.html')
def home(request):
    searched=request.GET.get('searched')
    if searched:
        data=Add.objects.filter(Q(name__icontains=searched)|Q(age__icontains=searched)|Q(email__icontains=searched))
        data=data.filter(isdelete=False)
    else:    
       data=Add.objects.filter(isdelete=False)
    return render(request,'vehicle/home.html',{'data':data})
# Add Views
def add(request):
    if request.method == 'POST' and request.FILES:
        name = request.POST.get('name')
        age = request.POST.get('age')
        email = request.POST.get('email')
        vname = request.POST.get('vname')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        try:
            age = int(age)
        except ValueError:
            messages.error(request, 'Please provide a valid age (numeric).')
            return redirect('add')

        if age < 20 or age > 80:
            messages.error(request, 'Your age should be between 20 and 80.')
            return redirect('add')
        if not image:
            messages.error(request, 'Please upload an image.')
            return redirect('add')
        try:
            user = Add(name=name, age=age, email=email, vname=vname, description=description, image=image)
            user.full_clean()  
            user.save()
            subject = "Django Email Testing"
            message = "Thanks for filling out our form. I feel thankful for adding your information. i really hope you will get a peaceful ride.Thank You!!!!!"
            from_email = "dahalrushma38@gmail.com"
            recipient_list = ['dahalrushma6@gmail.com']

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            messages.success(request, f'Hi {name}, your data was successfully submitted. Please check your email.')

        except ValidationError as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect('add')

        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect('add')

        return redirect('add')  

    return render(request, 'vehicle/add.html')

def delete_data(request, id):
    try:
        data = Add.objects.get(id=id)
        data.isdelete = True
        data.save()
        messages.success(request, "Item successfully deleted.")
    except Add.DoesNotExist:
        messages.error(request, "Item not found.")
    return redirect('home')
def clear_items(request):
    Add.objects.all().update(isdelete=True) 
    
    return redirect('home')  
@login_required(login_url='log_in')
def restore(request, id):
    try:
        data = Add.objects.get(id=id)
        data.isdelete = False
        data.save()
        messages.success(request, "Item successfully restored.")
    except Add.DoesNotExist:
        messages.error(request, "Item not found.")
    return redirect('home')
@login_required(login_url='log_in')
def recycle(request):
    data = Add.objects.filter(isdelete=True)
    if not data:
        messages.info(request, "No deleted items in the recycle bin.")
    return render(request, 'vehicle/recycle.html', {'data': data})
@login_required(login_url='log_in')
def edit(request,id):
    data = get_object_or_404(Add, id=id)
    if request.method == 'POST':
        image = request.FILES.get('image', None)
        name = request.POST.get('name')
        age = request.POST.get('age')
        email = request.POST.get('email')
        description = request.POST.get('description')
        vname = request.POST.get('vname')
        
        if not name or not age or not email or not description or not vname:
            messages.error(request, "Please fill out all required fields.")
            return redirect('edit', id=id)
        data.name = name
        data.age = age
        data.email = email
        data.description = description
        data.vname = vname
        
        if image:
            data.image = image  
        
        data.save()
        messages.success(request, "Your details have been updated successfully!")
        return redirect('home')

    return render(request,'vehicle/edit.html',{'data':data})
# payment view
def payment(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        amount = request.POST.get('money')
        pickup_date = request.POST.get('pick')
        dropoff_date = request.POST.get('drop')
        if not fname or not email or not address or not city or not amount or not pickup_date or not dropoff_date:
            messages.error(request, "All fields are required!")
            return redirect('payment')

        try:
            payment = Payment(
                full_name=fname,
                email=email,
                address=address,
                city=city,
                amount=amount,
                pickup_date=pickup_date,
                dropoff_date=dropoff_date
            )
            payment.save()
            messages.success(request, "Payment details have been successfully submitted. Proceeding to checkout!")
            return redirect('payment')  

        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect('payment')  
    return render(request, 'vehicle/payment.html')

# =========================== AUTH =============================================
# Registration view
def register(request):
    if request.method == 'POST':
        namee = request.POST.get('namee')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        if password != password1:
            messages.error(request, "Password and confirm password do not match!")
            return redirect('register')

        try:
            validate_password(password)
            if User.objects.filter(email=email).exists():
                messages.error(request, "Your email is already registered!")
                return redirect('register')

            # Create the user
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = namee
            user.save()
            messages.success(request, 'Successfully registered!')
            return redirect('log_in') 

        except ValidationError as e:
            for error in e.messages:
                messages.error(request, error)
            return redirect('register')

    return render(request, 'auth/register.html')
def log_in(request):
     if request.method =='POST':
        username=request.POST['username']
        password=request.POST['password']
        
        if not User.objects.filter(username=username).exists():
            messages.error(request,'username isnot register yet !!')
            return redirect('log_in')
        
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('index')
     return render(request,'auth/login.html')
 
def log_out(request):
    logout(request)
    return redirect('index') 
