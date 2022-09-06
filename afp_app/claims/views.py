from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate

from afp_app.claims.models import Award
from afp_app.claims.forms import AwardForm


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
            return redirect("/home")
    else:
        form = AwardForm()

    return render(request, "award/create_award.html", {"form": form})
