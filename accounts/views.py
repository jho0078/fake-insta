from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import CustomUserChangeForm, CustomUserCreationForm, ProfileForm
from .models import Profile


def signup(request):
    if request.user.is_authenticated:
        return redirect('posts:list')
        
    if request.method == 'POST':
        signup_form = CustomUserCreationForm(request.POST)
        if signup_form.is_valid():
            signup_user = signup_form.save()
            Profile.objects.create(user=signup_user)
            auth_login(request, signup_user)
            return redirect('posts:list')
    else:
        signup_form = CustomUserCreationForm()
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
            # 단축평가
            # 로그인이 안된 사람이 접근이 불가능한 페이지를 접속하려 하면 
            # @login_required 에 의해 로그인페이지로 이동하게 된다.
            # 이 때 ?next=/new/ 이런식으로 원래 이동하려 했던 주소가 next에 저장된다.
            # 이 주소가 있다면 이 곳으로 리턴하고, 없다면(정상적인 접근)
            # posts:list 로 이동한다.
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
        update_form = CustomUserChangeForm(request.POST, instance=request.user)
        if update_form.is_valid():
            update_form.save()
            return redirect('people', username)
            
    else:
        update_form = CustomUserChangeForm(instance=request.user)
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
    
@login_required
def profile_update(request):
    profile = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        profile_form = ProfileForm(data=request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('people', request.user.username)
    else:
        profile_form = ProfileForm(instance=request.user.profile)
    context = {'profile_form': profile_form}
    return render(request, 'accounts/profile_update.html', context)
    
@login_required
def follow(request, user_pk):
    people = get_object_or_404(get_user_model(), pk=user_pk)
    # people 을 팔로워하고 있는 모든 유저에 현재 접속 유저가 있다면
    if request.user in people.followers.all():
    # 언팔로우
        people.followers.remove(request.user)
    # 아니면
    else:
    # 팔로우
        people.followers.add(request.user)
    return redirect('people', people.username)
    
# usercreationform 의 아빠는 modelform 인자 : request.POST, request.FILES ... instance
# 데이터베이스에 저장
# authenticationform 의 아빠는 django  인자 : request, request.POST ... instance
# 세션에 저장