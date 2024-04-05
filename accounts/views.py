from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required

# verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings
import requests

from core.models import *

from .forms import *

def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            username = email.split("@")[0]

            user = User.objects.create_user(
                first_name=first_name, last_name=last_name, username=username,
                email=email, password=password
            )
            user.phone = phone
            user.save()

            # User activation account
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(
                mail_subject,  # Subject
                message,  # Message
                settings.EMAIL_HOST_USER,  # Sender
                [to_email]  # Receiver
            )
            send_email.fail_silently = True
            send_email.send()
            return redirect('/verify-email/?command=verification&email='+email)
    else:
        form = RegistrationForm()

    context = {
        'form': form,
    }

    template_name = 'accounts/signup.html'
    return render(request, template_name, context)

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.verified = True
        user.save()
        messages.success(
            request, 'Congratulations! your account is activated. Now you can login!')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link.')
        return redirect('signup')

def verify_email(request):
    template_name = 'accounts/verify-email-message.html'
    return render(request, template_name)

def login(request):
    if request.user.is_authenticated:
        messages.warning(request, f"Hey, you are already logged in.")
        return redirect('dashboard')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            user = auth.authenticate(request, email=email, password=password)

            if user is not None:
                auth.login(request, user)
                messages.success(request, f"You are logged in.")
                return redirect("dashboard")
            else:
                messages.warning(
                    request, f"User with {email}  does not exist, Create an account first.")
        except:
            messages.warning(request, f"User with {email} does not exist")

    template_name = 'accounts/login.html'
    return render(request, template_name)

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('login')

def profile(request):
    user = request.user
    courses = Courses.objects.filter(user=user).order_by('-date')
    trainings_enrolled = TrainingEnrollment.objects.filter(student=user).order_by('-date')
    trainings = Trainings.objects.filter(user=user).order_by('-date')
    context = {
        'courses': courses,
        'trainings_enrolled': trainings_enrolled,
        'trainings': trainings,
    }
    template_name = 'accounts/profile.html'
    return render(request, template_name, context)

def user_settings(request):
    user = request.user
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('profile')  # Redirect to the profile page after successful update
        else:
            messages.error(request, 'Error updating your profile. Please check the provided information.')
    else:
        form = UserUpdateForm(instance=user)

    context = {
        'form': form,
    }

    template_name = 'accounts/user_settings.html'
    return render(request, template_name, context)

@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = User.objects.get(email__exact=request.user.email)
        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()

                auth.logout(request)
                messages.success(
                    request, 'Your password was updated successfully!')
                return redirect('change_password')
            else:
                messages.error(request, 'Please enter valid current password!')
                return redirect('change_password')
        else:
            messages.error(
                request, 'New password and confirm password must much!')
            return redirect('change_password')

    template_name = 'accounts/change_password.html'
    return render(request, template_name)


def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            # Reset password email
            current_site = get_current_site(request)
            mail_subject = 'Reset your password'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(
                mail_subject,  # Subject
                message,  # Message
                settings.EMAIL_HOST_USER,  # Sender
                [to_email]  # Receiver
            )
            send_email.fail_silently = True
            send_email.send()

            messages.success(
                request, 'Password reset email has been sent to your email address.')
            return redirect('forgotPassword')

        else:
            messages.error(request, 'Account does not exists!')
            return redirect('forgotPassword')

    template_name = 'accounts/forgotPassword.html'
    return render(request, template_name)

def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password!')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link is expired.')
        return redirect('login')

def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful!')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('resetPassword')

    else:
        template_name = 'accounts/reset_password.html'
        return render(request, template_name)

