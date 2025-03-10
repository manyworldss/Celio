from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

class CustomUserCreationForm(UserCreationForm):
    # This creates a new form class that inherits from Django's built-in UserCreationForm
    def __init__(self, *args, **kwargs):
        # This is the constructor method that runs when the form is created
        # __init__ is a special Python method that initializes a new object
        # *args and **kwargs allow the method to accept any number of arguments

        super().__init__(*args, *kwargs)
        # super() calls the parent class's (UserCreationForm) __init__ method
        # This ensures all the basic form setup is done before we make our customizations

        # This loop removes Django's default help text for these three fields

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('core:home')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Successfully logged in!')
            return redirect('core:home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})
