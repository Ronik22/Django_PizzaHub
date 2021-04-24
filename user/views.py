from django.shortcuts import get_object_or_404, render, redirect
from .forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm
import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

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


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Your account has been updated!")
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'user':request.user,
        'u_form':u_form,
        'p_form':p_form
    }

    return render(request, 'user/profile.html', context)