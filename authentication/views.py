import json
from django.contrib.auth import authenticate, login as django_login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from authentication.decorators import user_is_entry_author
from authentication.forms import RegistrationForm, LoginForm, VerifyForm
from authentication.helpers import create_authy_user, send_one_touch_request, send_authy_token_request, \
    verify_authy_token, check_user_status
from authentication.models import UserProfile, CountryCodes


def landing_page(request):
    return render(request, "landing_page.html")


def register(request):
    context = {}
    if request.user.is_authenticated():
        return redirect('/home')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            create_authy_user(form)
            context['form'] = RegistrationForm()
            context['message'] = 'User has been created successfully'
        else:
            context['form'] = form

    else:
        form = RegistrationForm()
        context = {
            'form': form
        }
    context['countries'] = CountryCodes.objects.all()
    return render(request, "register.html", context)


def login(request):
    if request.user.is_authenticated():
        return redirect('/home')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(username=email, password=password)
            if user is not None:
                django_login(request, user)
                status = check_user_status(user)
                send_one_touch_request(user)
                if user.profile.authy_status == 'sms':
                    return redirect('/verify')
                return redirect('/home')
            else:
                form.add_error('email', 'Invalid email or password')

    else:
        form = LoginForm()
    context = {
        'form': form
    }
    return render(request, "signin.html", context)


@user_is_entry_author
def home(request):
    return render(request, "home.html")


@login_required
def verify(request):
    user = request.user
    if request.method == 'POST':
        form = VerifyForm(request.POST)
        if form.is_valid():
            token = form.cleaned_data['token']
            verified = verify_authy_token(user.profile.authy_id, token)
            if verified.ok():
                user.profile.authy_status = 'approved'
                user.profile.save()
                return redirect('/home')
    else:
        form = VerifyForm()
        send_authy_token_request(user.profile.authy_id)

    context = {
        'form': form
    }
    return render(request, "verify.html", context)


def logout_view(request):
    logout(request)
    return redirect('/login')


@csrf_exempt
def authy_callback(request):
    data = json.loads(request.body)
    authy_id = data.get('authy_id')
    profile = UserProfile.objects.filter(authy_id=authy_id).first()
    if profile:
        profile.authy_status = data.get('approval_request').get('transaction').get('status')
        request.user.profile.save()
        return HttpResponse(json.dumps({'success': True}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'success': False}), content_type="application/json")
