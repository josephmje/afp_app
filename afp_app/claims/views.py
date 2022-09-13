from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from django.contrib import messages

from afp_app.claims.models import Award
from afp_app.claims.forms import AwardForm


def list_awards(request):
    award_list = Award.objects.all()
    return render(request, "claims/awards/awards.html", {"awards": award_list})


@login_required(login_url="/accounts/login")
def home(request):
    """View function for home page of site."""

    all_award = Award.objects.all().order_by("-created_at")
    return render(request, "home.html", {"award": all_award})


#    # Generate counts of some of the main objects
#    num_awards = Award.objects.all().count()

#    context = {
#        "num_awards": num_awards,
#    }

#    return render(request, "home.html", context=context)


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


def view_award(request, uid):
    award = Award.objects.get(uid=uid)
    if award != None:
        return render(
            request, "claims/awards/edit_award.html", {"award": award}
        )


def edit_award(request, uid):
    award = Award.objects.get(id=uid)
    if request.method == "POST":
        award = Award.objects.get(id=request.POST.get("uid"))
        if award != None:
            form = AwardForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Award updated sucessfully!")
                return redirect("/awards")
            else:
                form = AwardForm()

    return render(request, "claims/awards/add_award.html", {"form": form})


def delete_award(request, uid):
    award = Award.objects.get(id=uid)
    award.delete()
    messages.success(request, "Award deleted successfully!")
    return redirect("/awards")
