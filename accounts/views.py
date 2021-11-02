from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import UserLoginForm, UserRegistrationForm, ProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User as MyUser, Profile
from core.models import Post


class UserLogin(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'You logged in successfully!', 'success')
                return redirect('core:home')
            else:
                messages.warning(request, 'Username or Password is Invalid', 'warning')

            return render(request, self.template_name, {'form': self.form_class})


class UserLogout(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You logged out successfully', 'success')
        return redirect('core:home')


class UserRegister(View):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = MyUser.objects.create_user(email=cd['email'], username=cd['username'], password=cd['password1'])
            Profile.objects.create(user=user, full_name=user.username)
            messages.success(request, 'You registered successfully', 'success')
            return redirect('core:home')
        else:
            messages.error(request, "Error", 'danger')
        return render(request, self.template_name, {'form': form})


class UserProfile(View):
    form_class = None
    template_name = 'accounts/profile.html'

    def get(self, request, username):
        user = get_object_or_404(MyUser, username=username)
        posts = Post.objects.filter(user=user)
        return render(request, self.template_name, {'user': user, 'posts': posts})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile updated successfully', 'success')
            return redirect('accounts:user_profile', request.user.username)


class UserEditProfile(View):
    form_class = ProfileForm
    template_name = 'accounts/edit_profile.html'

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class(instance=request.user.profile)})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile updated successfully', 'success')
            return redirect('accounts:user_profile', request.user.username)
