from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.views.decorators.cache import cache_control
from django.shortcuts import get_object_or_404
from .forms import UserChangeForm



# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    if request.user.is_superuser and request.user.is_authenticated:
        return redirect('admin_panel')

    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def contact(request):
     return render(request,'contact.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def handlelogin(request):
    
    if request.user.is_authenticated:
        return redirect('index')
    if request.method=="POST":
        user_name=request.POST.get("username")
        pass1=request.POST.get("pass1")


        if not User.objects.filter(username=user_name).exists():
            messages.warning(request, "Invalid Username")
            return redirect('handlelogin')

        myuser=authenticate(username=user_name,password=pass1)

        if not myuser:
            messages.warning(request, 'Invalid password')
            return redirect('handlelogin')
            
            
        login(request,myuser)
        messages.success(request,"Login Success")
        return redirect('index')

    return render(request,'login.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def handlesignup(request):
    
    if request.user.is_authenticated:
        return redirect('index')
    if request.method=="POST":
        user_name=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("pass1")
        confirm_password=request.POST.get("pass2")
        first_name= request.POST.get("firstname")
        last_name=request.POST.get("lastname")
        if password!= confirm_password:
            messages.warning(request,"Password Is Incorrect")
            return redirect('handlesignup')
       
        if not first_name:
            messages.warning(request,"firstname required")
            return redirect('handlesignup')
        try:
            if User.objects.get(username=user_name):
                messages.info(request,"Username Is Taken")
                return redirect('/signup')

        except Exception as e:
            print(e)    

        try:
            if User.objects.get(email=email):
                 messages.info(request,"Email Is Taken")
                 return redirect('/signup')
        except Exception as e:
            print(e)    

        myuser=User.objects.create_user(username=user_name,email=email,password=password, first_name=first_name, last_name=last_name)
        myuser.save()
        messages.success(request,"Signup Success Please Login")
        return redirect('/login')       

    return render(request,'signup.html')  

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def handlelogout(request):
    logout(request)
    messages.info(request,"Logout Success")
    return redirect('/login')

def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_panel')
    if request.method=="POST":
        username = request.POST.get("username")
        password=request.POST.get("pass1")
        check_if_user_exists = User.objects.filter(username = username).exists()

        if not check_if_user_exists:
            messages.error(request,"Invalid username")
            return redirect('/admin_login')

        myuser=authenticate(username=username, password=password)
        
        if not myuser:
            messages.error(request,"Invalid password")
            return redirect('/admin_login')


        if myuser.is_superuser:
            login(request, myuser)
            messages.success(request,"Login Success")
            return redirect('admin_panel')
        else:
            messages.warning(request,"You are not an admin!")
            return redirect('handlelogin')

    
    return render(request,'admin_login.html')


# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_panel(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    # Query the User table to get all user objects
    user_data = User.objects.all()
    
    # Pass the user data to the template
    context = {"data": user_data}
    
    return render(request, 'admin_panel.html', context)

def add_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        # Create a new user
        user = User.objects.create_user(username=username, email=email, password=password)
        
        # Log in the user (optional)
        login(request, user)
        
        messages.success(request, "User created successfully")
        return redirect('admin_panel')
    
    return render(request, 'admin_panel.html')

def edit_user(request, user_id):
    
    user = get_object_or_404(User, pk=user_id)
    if request.method == "POST":
        form = UserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f"User '{user.username}' updated successfully")
            return redirect('admin_panel')
            
            
    else:
        form = UserChangeForm(instance=user)
    return render(request, 'edit_user.html', {'form': form, 'user': user})

  

def delete_user(request, user_id):
    # Retrieve the user object or return a 404 if it doesn't exist
    
    user = get_object_or_404(User, pk=user_id)
    # Delete the user
    user.delete()
    
    # Add a success message
    messages.success(request, f"User '{user.username}' deleted successfully")
    
    # Redirect back to the admin panel
    return redirect('admin_panel')

def admin_logout(request):
    logout(request)
    messages.info(request,"Logout Success")
    return redirect('admin_login')

