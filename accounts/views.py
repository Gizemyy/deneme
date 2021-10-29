from django.shortcuts import render, Http404
from django.contrib.auth.models import User
from .forms import LoginForm, RegisterForm, ProfileForm
from django.contrib.auth import authenticate, login, logout
from accounts.models import Profile
from django.shortcuts import HttpResponseRedirect, redirect,get_object_or_404


def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('ask:home')
    return render(request, "account_form.html", {"form": form, 'title': 'Giriş Yap'})


def register_view(request):
    form = RegisterForm(request.POST or None)
    profile = Profile()
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password1')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        profile.user = user
        profile.save()
        login(request, new_user)
        return redirect('accounts:edit')
    return render(request, "account_form.html", {"form": form, 'title': 'Üye Ol','profile': profile})

def logout_view(request):
    logout(request)
    return redirect('accounts:login')

def profile_detail(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'profile_detail.html', {'profile': profile})

def profile_update(request):
    if not request.user.is_authenticated:
        raise Http404()
    profiles = Profile.objects.get(user=request.user)
    form = ProfileForm(request.POST or None, request.FILES, instance=profiles)
    if form.is_valid():
        profile = form.save()
        profile.user.first_name = form.cleaned_data.get('first_name')
        profile.user.last_name = form.cleaned_data.get('last_name')
        profile.user.email = form.cleaned_data.get('email')
        profile.user.save()
        form.save()
        return HttpResponseRedirect(profile.get_absolute_url())
    context = {
        'form': form,
    }
    return render(request, 'edit_profile.html', context)


def follow_profile(request, id):
    profile = Profile.objects.get(user=request.user)
    other = Profile.objects.get(id=id)
    user = User.objects.get(id=id)

    if other.user != profile.user and other.user in profile.following_user.all():
        follow = False
        profile.following_user.remove(other.user)
        other.follower_user.remove(profile.user)
    elif other.user != profile.user and not other.user in profile.following_user.all():
        follow = True
        profile.following_user.add(other.user)
        other.follower_user.add(profile.user)
    if other.user in profile.following_user.all():
        follow = True
    else:
        follow = False
    context = {
        'other': other,
        'user': user,
        'follow': follow,
    }
    return render(request, 'show_profile.html', context)


def show_another_profile(request, id):
    user = User.objects.get(id=id)
    profile = Profile.objects.get(user=request.user)
    other = Profile.objects.get(id=id)

    if other.user in profile.following_user.all():
        follow = True
    else:
        follow = False

    return render(request, 'show_profile.html', {'user': user, 'follow': follow, 'other':other})


def profile_following_space(request,id):
    following = get_object_or_404(Profile, id=id).following.all()
    profile = Profile.objects.get(id=id)
    follows = profile.following_user.all()
    followers = profile.follower_user.all()
    context = {

        'following': following,
        'profile': profile,
        'follows': follows,
        'followers': followers
    }
    return render(request, 'following.html', context)


