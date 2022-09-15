from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.context_processors import csrf

from crispy_forms.utils import render_crispy_form

from afp_app.claims.forms import (
    AwardForm,
    EditorialBoardForm,
    GrantReviewForm,
    LectureForm,
    PromotionForm,
)
from afp_app.claims.models import Award, EditorialBoard, GrantReview, Lecture, Promotion


@login_required(login_url="/accounts/login")
def home(request):
    """View function for home page of site."""

    return render(request, "home.html")


@login_required(login_url="/accounts/login")
def award_list(request):
    award_list = Award.objects.filter(user_id=request.user)
    return render(request, "claims/award_list.html", {"awards": award_list})


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
    return render(request, "claims/model_form.html", {"form": form})


@login_required(login_url="/accounts/login")
def edit_award(request, pk):
    award = get_object_or_404(Award, pk=pk)
    if request.method == "POST":
        form = AwardForm(request.POST, instance=award)
        if form.is_valid():
            form.save()
            messages.success(request, "Award updated sucessfully!")
            return redirect("/awards")
    else:
        form = AwardForm(instance=award)
    return render(request, "claims/model_form.html", {"form": form, "award": award})


@login_required(login_url="/accounts/login")
def delete_award(request, pk):
    award = get_object_or_404(Award, pk=pk)
    award.delete()
    messages.success(request, "Award deleted successfully!")
    return redirect("/awards")
