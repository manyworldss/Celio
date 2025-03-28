from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

class CustomUserCreationForm(UserCreationForm):
    # This creates a new form class that inherits from Django's built-in UserCreationForm
    def __init__(self, *args, **kwargs):
        # This is the constructor method that runs when the form is created
        # __init__ is a special Python method that initializes a new object
        # *args and **kwargs allow the method to accept any number of arguments

        super().__init__(*args, **kwargs)
        # super() calls the parent class's (UserCreationForm) __init__ method
        # This ensures all the basic form setup is done before we make our customizations

        # This loop removes Django's default help text for these three fields

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('core:home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            
            # Handle "remember me" checkbox
            if not request.POST.get('remember_me', False):
                # Session expires when browser closes if "remember me" not checked
                request.session.set_expiry(0)
            else:
                # Session will expire based on Django's SESSION_COOKIE_AGE (default 2 weeks)
                request.session.set_expiry(None)
                
            # Log the user in
            login(request, user)
            
            # Check if there's a next parameter in the URL and redirect there
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            return redirect('core:home')
        else:
            # Add a friendly error message for login failures
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    """Custom logout view to ensure clean logout"""
    try:
        logout(request)
        messages.success(request, "You have been successfully logged out.")
    except Exception as e:
        # Handle any errors that might occur during logout
        messages.error(request, "There was an issue logging you out.")
    return redirect('core:home')

def profile(request):
    """View for user profile page"""
    return render(request, 'accounts/profile.html', {
        'user': request.user
    })
