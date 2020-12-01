from django.http import HttpResponseRedirect

from django.shortcuts import render
from django.contrib.auth import logout as do_logout
from django.contrib.auth import login as do_login
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm

# login functions
def login(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                do_login(request, user)
                return HttpResponseRedirect('/watcher')

    return render(request, "users/login.html", {'form': form})


def logout(request):
    do_logout(request)
    return HttpResponseRedirect('/users/login')