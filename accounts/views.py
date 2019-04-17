from django.shortcuts import render, redirect, get_object_or_404
# from .forms import UserForm
from .forms import UserCustomChangeForm, UserCustomCreationForm
# from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required


def signup(request):
    if request.user.is_authenticated:
        return redirect('posts:list')
        
    if request.method == 'POST':
        signup_form = UserCustomCreationForm(request.POST)
        if signup_form.is_valid():
            signup_user = signup_form.save()
            auth_login(request, signup_user)
            return redirect('posts:list')
    else:
        signup_form = UserCustomCreationForm()
    context = {'signup_form': signup_form}
    return render(request, 'accounts/signup.html', context)
    
def login(request):
    if request.user.is_authenticated:
        return redirect('posts:list')
    
    if request.method == 'POST':
        login_form = AuthenticationForm(request, request.POST)
        if login_form.is_valid():
            login_user = login_form.get_user()
            auth_login(request, login_user)
            return redirect(request.GET.get('next') or 'posts:list')
    else:
        login_form = AuthenticationForm()
    context = {'login_form': login_form}
    return render(request, 'accounts/login.html', context)

def logout(request):
    auth_logout(request)
    return redirect('posts:list')
    
def people(request, username):
    people = get_object_or_404(get_user_model(), username=username)
    context = {'people': people,}
    return render(request, 'accounts/people.html', context)

@login_required   
def update(request):
    username = request.user.username
    if request.method == 'POST':
        update_form = UserCustomChangeForm(request.POST, instance=request.user)
        if update_form.is_valid():
            update_form.save()
            return redirect('people', username)
            
    else:
        update_form = UserCustomChangeForm(instance=request.user)
    context = {'update_form': update_form}
    return render(request, 'accounts/update.html', context)
    
def delete(request):
    request.user.delete()
    return redirect('posts:list')

@login_required
def password(request):
    if request.method == 'POST':
        password_form = PasswordChangeForm(request.user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            return redirect('people', request.user.username)
    else:
        password_form = PasswordChangeForm(request.user)
    context = {'password_form': password_form}
    return render(request, 'accounts/password.html', context)