from django.shortcuts import redirect, render
from userauths.forms import UserRegisterForm, UserLoginForm, ProfileForm, PasswordResetForm, SetNewPasswordForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.models import User
from userauths.models import User, Profile
from django.contrib.auth import get_user_model, login
# from .forms import UserRegisterForm
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .decorators import user_not_authenticated
from django.core.mail import EmailMessage
from django.db.models.query_utils import Q

from .tokens import account_activation_token

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('userauths:sign-in')
    else:
        messages.error(request, 'Activation link is invalid!')
    
    return redirect('core:index')

def activateEmail(request, user, to_email):
    mail_subject = 'Activate your user account.'
    message = render_to_string('userauths/activate_account.html', {
        'user': user,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear {user.username}, please go to you email {to_email} inbox and click on \
            received activation link to confirm and complete the registration. Note: Check your spam folder.')
    else:
        messages.error(request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')

@user_not_authenticated
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active=False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            # login(request, user)
            # messages.success(request, f"Hey {user.username}, Your account has been created successfully!")
            return redirect('core:index')
        else:
            for error in list(form.errors.values()):
                print(request, error)

    else:
        form = UserRegisterForm()

    return render(
        request = request,
        template_name = "userauths/sign-up.html",
        context={"form":form}
        )

@user_not_authenticated
def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = authenticate( 
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                messages.success(request, f"Hello <b>{user.username}</b>! You have been logged in")
                return redirect("core:index")

        else:
            for key, error in list(form.errors.items()):
                if key == 'captcha' and error[0] == 'This field is required.':
                    messages.error(request, "You must pass the reCAPTCHA test")
                    continue
                
                messages.error(request, error) 
    else:
        form = UserLoginForm()

    return render(
        request=request,
        template_name="userauths/sign-in.html",
        context={"form": form}
        )

def logout_view(request):
    logout(request)
    messages.warning(request, "You Logged Out")
    return redirect("core:index")

def profile_edit(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            messages.success(request, "Profile Updated Succesfully!")
            return redirect("core:dashboard")
    else:
        form = ProfileForm(instance=profile)
    

    context = {
        'form': form,
        "profile":profile,
    }
    return render(request, "userauths/profile-edit.html", context)

@user_not_authenticated
def reset_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = get_user_model().objects.filter(Q(email=user_email)).first()
            if associated_user:
                subject = "Password Reset request"
                message = render_to_string("userauths/reset-password-email.html", {
                    'user': associated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': account_activation_token.make_token(associated_user),
                    "protocol": 'https' if request.is_secure() else 'http'
                })
                email = EmailMessage(subject, message, to=[associated_user.email])
                if email.send():
                    messages.success(request,
                        """
                        <h2>Password reset sent</h2><hr>
                        <p>
                            We've emailed you instructions for setting your password, if an account exists with the email you entered. 
                            You should receive them shortly.<br>If you don't receive an email, please make sure you've entered the address 
                            you registered with, and check your spam folder.
                        </p>
                        """
                    )
                else:
                    messages.error(request, "Problem sending reset password email, <b>SERVER PROBLEM</b>")

            return redirect('core:index')

        for key, error in list(form.errors.items()):
            if key == 'captcha' and error[0] == 'This field is required.':
                messages.error(request, "You must pass the reCAPTCHA test")
                continue

    form = PasswordResetForm()
    return render(
        request=request, 
        template_name="userauths/reset-password.html", 
        context={"form": form}
        )

def passwordResetConfirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = SetNewPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been set. You may go ahead and <b>log in </b> now.")
                return redirect('userauths:sign-in')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
        
        form = SetNewPasswordForm(user)
        return render(request, 'userauths/reset-password-confirm.html', {'form': form})
    else:
        messages.error(request, "Link is expired")

    messages.error(request, 'Something went wrong, redirecting back to Homepage')
    return redirect("core:index")