
from textwrap import indent
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User

from accounts.models import Profile
from .forms import LoginForm, ProfileForm, SignupForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
# Create your views here.


def login_view(request):
    template_name = "accounts/login.html"
    context = {}
    context["form"] = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            if not User.objects.filter(username=username).exists():
                messages.warning(request, "User not found!")
                return render(request, template_name, context)

            user = authenticate(username=username, password=password)

            # this part is for search and find and specify the users who are detailformer which are selected by admin panel in the role of their jobs as detailformer by manager of the website.
            detailformer_users = list()
            for profile in Profile.objects.filter(job="detailformer"):
                detailformer_users.append(profile.user)
            print(detailformer_users)
            # End part of search and find and specify the users who are detailformer which are selected by admin panel in the role of their jobs as detailformer by manager of the website.

            if user is not None and user not in detailformer_users:
                login(request, user)
                messages.success(request, "you're loging successfuly")
                return redirect("main:home")

            elif Profile.objects.filter(job='detailformer'):
                login(request, user)
                messages.success(request, "به صفحه ی وارد کردن اطلاعات بار خوش آمدید")
                return redirect("main:home")

            else:
                messages.error(request, "Username or password is incorrect!")
                return render(request, template_name, context)
        else:
            messages.error(request, "error!")

    return render(request, template_name, context)


def logout_view(request):

    logout(request)
    messages.success(request, "goodbye")

    #by below we will sent to the login page after logout from our page.
    return redirect("accounts:login")


@login_required()
def profile_view(request):
    template_name = 'accounts/profile.html'
    context = {}
    user = request.user

    initial = {
        "bio": user.profile.bio,
        "phone_number":user.profile.phone_number,
        "age":user.profile.age,
        "job":user.profile.job,
        "gender":user.profile.gender,
        "nc":user.profile.nc,
        "first_name":user.profile.first_name,
        "last_name":user.profile.last_name
    }

    form = ProfileForm(request.POST or None, instance=user, initial=initial)

    if request.method == 'POST':
        
        if form.is_valid():
            form.save()
            
            bio = form.cleaned_data['bio']
            user.profile.bio = bio

            phone_number = form.cleaned_data['phone_number']
            user.profile.phone_number = phone_number

            age = form.cleaned_data['age']
            user.profile.age = age

            job = form.cleaned_data['job']
            user.profile.job = job

            gender = form.cleaned_data['gender']
            user.profile.gender = gender

            nc = form.cleaned_data['nc']
            user.profile.nc = nc

            first_name = form.cleaned_data['first_name']
            user.profile.first_name = first_name

            last_name = form.cleaned_data['last_name']
            user.profile.last_name = last_name

            user.profile.save()

            messages.success(request, "profile updated")
            return redirect("accounts:profile")

        else:
            context["form"] = form
            return render(request, template_name, context)

    context["form"] = form

    return render(request, template_name, context)


def signup_view(request):
    template_name = 'accounts/signup.html'
    context = {}
    form = SignupForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            bio = form.cleaned_data['bio']
            

            phone_number = form.cleaned_data['phone_number']


            age = form.cleaned_data['age']
            

            job = form.cleaned_data['job']
            

            gender = form.cleaned_data['gender']
            

            nc = form.cleaned_data['nc']
            

            first_name = form.cleaned_data['first_name']
            

            last_name = form.cleaned_data['last_name']
            

            user.profile.save()



            user.refresh_from_db()
            user.profile.bio = bio
            user.profile.phone_number = phone_number
            user.profile.age = age
            user.profile.job = job
            user.profile.gender = gender
            user.profile.nc = nc
            user.profile.first_name = first_name
            user.profile.last_name = last_name


            user.profile.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request,"your account created successfully.")
            return redirect("main:home")

        else:
            context["form"] = form
            return render(request, template_name, context)
    else:
        context["form"] = form

    return render(request, template_name, context)



from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy("accounts:profile")