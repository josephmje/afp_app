from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render


@login_required
def logoutaccount(request):
    logout(request)
    return redirect("home")


def loginaccount(request):
    if request.method == "GET":
        return render(
            request, "loginaccount.html", {"form": AuthenticationForm}
        )
    else:
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is None:
            return render(
                request,
                "loginaccount.html",
                {
                    "form": AuthenticationForm(),
                    "error": "username and password do not match",
                },
            )
        else:
            login(request, user)
            return redirect("home")
