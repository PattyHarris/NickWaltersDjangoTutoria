from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def signup(request):
    # If the method is a POST, that means we're here because the
    # form button was clicked.  Otherwise, if the method is a GET,
    # the user came to the signup.html page for register as a new
    # user.
    if request.method == 'POST':
        # Verify that the passwords are the same - I would do this only if the
        # username is unique, but we'll follow along with the class....
        if request.POST['password1'] == request.POST['password2']:
            # Verify that the username is unique by searching for the given username.
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'accounts/signup.html', {'error': 'Sorry, username has already been taken!'})
            except User.DoesNotExist:
                # Create the user with the data entered from the sign up page.
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                login(request, user)
                return render(request, 'accounts/signup.html')
        else:
            return render(request, 'accounts/signup.html', {'error': 'Password Mismatch!'})
    else:
        return render(request, 'accounts/signup.html')


def loginView(request):
    # If the method is a POST, that means we're here because the
    # form button was clicked.  Otherwise, if the method is a GET,
    # the user came to the signup.html page for register as a new
    # user.
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:

            login(request, user)

            # If the POST contains a ?next=/posts/create parameter, then it
            # means the user tried to create a  post but had not logged in first.
            # If login is successful, we'll redirect them back to that page.
            if 'next' in request.POST:
                return redirect(request.POST['next'])

            # Otherwise, login is successful, redirect back to the 'home' page.
            return redirect('home')

        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid username or password.'})
    else:
        return render(request, 'accounts/login.html')


# Handle logout - see notes on why this needs to be a POST method.
def logoutView(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
