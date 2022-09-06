from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate

from afp_app.claims.models import Award
from afp_app.claims.forms import AwardForm, PromotionForm


@login_required(login_url="/accounts/login")
def home(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_awards = Award.objects.all().count()

    context = {
        "num_awards": num_awards,
    }

    return render(request, "home.html", context=context)


class AwardListView(ListView):
    """Generic class-based view for a list of awards."""

    model = Award
    context_object_name = "award_list"
    paginate_by = 10


class AwardDetailView(DetailView):
    model = Award


@login_required(login_url="/accounts/login")
def create_award(request):
    if request.method == "POST":
        form = AwardForm(request.POST)
        if form.is_valid():
            award = form.save(commit=False)
            award.user_id = request.user
            award.save()
            return redirect("/")
    else:
        form = AwardForm()

    return render(request, "claims/awards/add_award.html", {"form": form})


@login_required(login_url="/accounts/login")
def update_award(request, pk):
    award = Award.objects.get(id=pk)
    form = AwardForm(instance=award)

    if request.method == "POST":
        form = AwardForm(request.POST, instance=award)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = AwardForm()

    return render(request, "claims/awards/add_award.html", {"form": form})


def delete_award(request, pk):
    context = {}
    return render(request, "claims/awards/delete.html", context)
