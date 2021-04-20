from django.shortcuts import render, redirect
from .forms import UserRegisterForm
import requests
from django.conf import settings
from django.contrib import messages

# Create your views here.

""" User account creation """
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():

            # reCAPTCHA V2
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()

            if result['success']:
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f"Your account has been created! You can login now")
                return redirect('login')
            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')            
            
    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html', {'form':form})