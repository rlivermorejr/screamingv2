from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View

from django.http import Http404

from django.contrib.auth import login, authenticate, logout
from auth_app.forms import CreateUserForm, LoginForm
from auth_app.models import Account
from django.contrib import messages
from notification_app.models import Notification


def index_page(request):
    """
    This is mainly just so the number of
    notifications shows up on the homepage
    """
    if not request.user.is_authenticated:
        return render(request, 'index.html')
    else:
        cur_user = Account.objects.get(id=request.user.id)
        notif = Notification.objects.filter(
            user_to_notify=cur_user, read=False)
        # return render(request, 'index.html', {'notif': notif})
        return render(request, 'index.html', {'notif': notif})


class CreateUser(View):
    """
    Creates a new user from an
    AbstractUser model. If you are logged in
    and make a new user, it will log you out
    and take you to login page
    """

    def get(self, request):
        form = CreateUserForm()
        return render(request, 'forms/create.html', {'form': form})

    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Account.objects.create_user(
                username=data['username'],
                password=data['password1'],
            )
            logout_user(request)
            return HttpResponseRedirect(reverse('login_page'))
        # if form.has_error:
        #     messages.info(request, "Username already exists!")
        #     return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            messages.info(request, form.errors)
            return HttpResponseRedirect(request.META['HTTP_REFERER'])


def login_user(request):
    """
    Logs the user in and will also provide
    error message if username or password
    is incorrect
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            my_user = authenticate(
                request, username=data['username'], password=data['password'])
            if my_user:
                login(request, my_user)
                return HttpResponseRedirect(reverse('main'))
            else:
                messages.error(request, 'username or password not correct')
                return redirect('login_page')
    form = LoginForm()
    return render(request, 'forms/gen_form.html', {'form': form})


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('main'))


def dev_message(request):
    return render(request, 'dev_message.html')
