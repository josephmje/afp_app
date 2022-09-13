from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from afp_app.claims.models import Award
from afp_app.claims.forms import AwardForm


@login_required(login_url="/accounts/login")
def home(request):
    """View function for home page of site."""

    return render(request, "home.html")


@login_required(login_url="/accounts/login")
def list_awards(request):
    award_list = Award.objects.filter(user_id=request.user)
    return render(request, "claims/awards/awards.html", {"awards": award_list})


@login_required(login_url="/accounts/login")
def add_award(request):
    if request.method == "POST":
        form = AwardForm(request.POST)
        if form.is_valid():
            award = form.save(commit=False)
            award.user_id = request.user
            award.save()
            return redirect("/awards")
    else:
        form = AwardForm()

    return render(request, "claims/awards/add_award.html", {"form": form})


@login_required(login_url="/accounts/login")
def edit_award(request, uuid):
    award = Award.objects.get(uuid=uuid)
    if request.method == "POST":
        award = Award.objects.get(id=request.POST.get("uuid"))
        if award != None:
            form = AwardForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Award updated sucessfully!")
                return redirect("/awards")
            else:
                form = AwardForm()

    return render(request, "claims/awards/add_award.html", {"form": form})


@login_required(login_url="/accounts/login")
def delete_award(request, uuid):
    award = Award.objects.get(uuid=uuid)
    award.delete()
    messages.success(request, "Award deleted successfully!")
    return redirect("/awards")
