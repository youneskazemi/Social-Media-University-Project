from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import UserLoginForm, UserRegistrationForm, ProfileForm, ChangePasswordForm, EmailForm, NumberForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User as MyUser, Profile, Relation
from core.models import Post
from django.http import JsonResponse
from django.core.mail import send_mail
import random


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


class UserProfile(LoginRequiredMixin, View):
    form_class = None
    template_name = 'accounts/profile.html'

    def get(self, request, username):
        user = get_object_or_404(MyUser, username=username)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        posts = Post.objects.filter(user=user)
        is_following = False
        if relation.exists():
            is_following = True

        return render(request, self.template_name, {'user': user, 'posts': posts, 'is_following': is_following})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile updated successfully', 'success')
            return redirect('accounts:user_profile', request.user.username)


class UserEditProfile(LoginRequiredMixin, View):
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


class follow(LoginRequiredMixin, View):
    def post(self, request):
        user_id = request.POST['user_id']
        following = get_object_or_404(MyUser, pk=user_id)
        check_relation = Relation.objects.filter(from_user=request.user, to_user=following)
        if check_relation.exists():
            return JsonResponse({'status': 'exists'})
        else:
            Relation(from_user=request.user, to_user=following).save()
            return JsonResponse({'status': 'ok'})


class unfollow(LoginRequiredMixin, View):
    def post(self, request):
        user_id = request.POST['user_id']
        following = get_object_or_404(MyUser, pk=user_id)
        check_relation = Relation.objects.filter(from_user=request.user, to_user=following)
        if check_relation.exists():
            check_relation.delete()
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'notexists'})


class send_email(View):
    form_class = EmailForm
    template_name = 'accounts/reset_password.html'

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request):
        number = random.randint(1000, 9999)
        subject = "Reset Password"
        message = f"for rest your password enter {number}"
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            email = cd["email"]
            send_mail(subject=subject, message=message, from_email="", recipient_list=[email],
                      fail_silently=False)
            return redirect("accounts:confirm_password", number, email)


class confirm_password(View):
    form_class = NumberForm
    template_name = 'accounts/confirm_password.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request, number, email):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['number'] == number:
                return redirect("accounts:change_password", email)
            else:
                messages.error(request, "number is invalid", "warning")
                return redirect("accounts:confirm_password", number, email)


class change_password(View):
    template_name = "accounts/change_password.html"
    form_class = ChangePasswordForm

    def get(self, request, *args, **kwargs):
        return render(request, "accounts/change_password.html", {"form": self.form_class})

    def post(self, request, email):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = get_object_or_404(MyUser, email=email)
            user.set_password(cd['password1'])
            user.save()
            messages.success(request, "your password successfully changed!", "success")
            return redirect("core:home")
