from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib import auth


from accounts.forms import RegistrationForm

# Create your views here.

def register(request):
  form = RegistrationForm(request.POST)
  try:
    if request.method == 'POST':
      if form.is_valid():
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        confirm_password = form.cleaned_data['confirm_password']
        if(password != confirm_password):
          raise Exception
        username = email.split('@')[0]
        user = User.objects.create(
          first_name=first_name,
          last_name=last_name,
          email=email,
          password=password,
          username=username
        )
        user.save()
        messages.success(request, 'Registration Successful')
      else:
        messages.error(request, form.errors)
        return redirect('register')
  except Exception:
    form.errors['password'] = ': Passwords are not identical'
  context = {
    'form': form
  }
  return render(request, 'accounts/register.html', context)

def login(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']

    user = auth.authenticate(username=username, password=password)

    if user != None:
      auth.login(request, user)
      return redirect('home')
    else:
      messages.error(request, 'Invalid Credentials')
      return redirect('login')

  return render(request, 'accounts/login.html')

@login_required(login_url='login')
def logout(request):
  if request.user.is_authenticated:
    auth.logout(request)
    return redirect("login")
  return