from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    TemplateView,
    UpdateView,
)
from django.urls import reverse_lazy

from .forms import (
    AwardForm,
    CommitteeWorkForm,
    EditorialBoardForm,
    ExamForm,
    GrantForm,
    GrantLinkFormSet,
    GrantReviewForm,
    PublicationLinkFormSet,
    PublicationForm,
    LectureForm,
    SupervisionForm,
)
from .models import (
    Award,
    EditorialBoard,
    Exam,
    Grant,
    GrantLink,
    GrantReview,
    CommitteeWork,
    Lecture,
    Publication,
    PublicationLink,
    Supervision,
)


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"


class AwardListView(LoginRequiredMixin, ListView):
    model = Award
    template_name = "claims/awards.html"
    context_object_name = "awards"

    def get_queryset(self):
        return Award.objects.filter(user_id=self.request.user)


class AwardCreateView(LoginRequiredMixin, CreateView):
    model = Award
    form_class = AwardForm
    template_name = "claims/award_form.html"
    success_url = reverse_lazy("award_list")

    def form_valid(self, form):
        award = form.save(commit=False)
        award.user_id = self.request.user
        award.save()
        return super().form_valid(form)


class AwardUpdateView(LoginRequiredMixin, UpdateView):
    model = Award
    form_class = AwardForm
    template_name = "claims/award_form.html"
    success_url = reverse_lazy("award_list")


class AwardDeleteView(LoginRequiredMixin, DeleteView):
    model = Award
    queryset = Award.objects.all()
    template_name = "claims/confirm_delete.html"
    success_url = reverse_lazy("award_list")


class PublicationListView(LoginRequiredMixin, ListView):
    model = Publication
    template_name = "claims/publications.html"
    context_object_name = "publications"


class PublicationInline:
    form_class = PublicationForm
    model = Publication
    template_name = "claims/publication_form.html"
    success_url = reverse_lazy("publication_list")

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        self.object = form.save()

        for name, formset in named_formsets.items():
            formset_save_func = getattr(
                self, "formset_{0}_valid".format(name), None
            )
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        return redirect("publication_list")

    def formset_links_valid(self, formset):
        links = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for link in links:
            link.publication = self.object
            link.save()


class PublicationCreateView(LoginRequiredMixin, PublicationInline, CreateView):
    def get_context_data(self, **kwargs):
        ctx = super(PublicationCreateView, self).get_context_data(**kwargs)
        ctx["named_formsets"] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        if self.request.method == "GET":
            return {"links": PublicationLinkFormSet(prefix="links")}
        else:
            return {
                "links": PublicationLinkFormSet(
                    self.request.POST or None,
                    self.request.FILES or None,
                    prefix="links",
                )
            }


class PublicationUpdateView(LoginRequiredMixin, PublicationInline, UpdateView):
    def get_context_data(self, **kwargs):
        ctx = super(PublicationUpdateView, self).get_context_data(**kwargs)
        ctx["named_formsets"] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        if self.request.method == "GET":
            return {"links": PublicationLinkFormSet(prefix="links")}
        else:
            return {
                "links": PublicationLinkFormSet(
                    self.request.POST or None,
                    self.request.FILES or None,
                    prefix="links",
                )
            }


class PublicationDeleteView(LoginRequiredMixin, DeleteView):
    model = Publication
    queryset = Publication.objects.all()
    template_name = "claims/confirm_delete.html"
    success_url = reverse_lazy("publication_list")


class PublicationLinkDeleteView(LoginRequiredMixin, DeleteView):
    model = PublicationLink
    queryset = PublicationLink.objects.all()
    template_name = "claims/confirm_delete.html"


class GrantListView(LoginRequiredMixin, ListView):
    model = Grant
    template_name = "claims/grants.html"
    context_object_name = "grants"


class GrantInline:
    form_class = GrantForm
    model = Grant
    template_name = "claims/grant_form.html"
    success_url = reverse_lazy("grant_list")

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        self.object = form.save()

        for name, formset in named_formsets.items():
            formset_save_func = getattr(
                self, "formset_{0}_valid".format(name), None
            )
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        return redirect("grant_list")

    def formset_links_valid(self, formset):
        links = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for link in links:
            link.grant = self.object
            link.save()


class GrantCreateView(LoginRequiredMixin, GrantInline, CreateView):
    def get_context_data(self, **kwargs):
        ctx = super(GrantCreateView, self).get_context_data(**kwargs)
        ctx["named_formsets"] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        if self.request.method == "GET":
            return {"links": GrantLinkFormSet(prefix="links")}
        else:
            return {
                "links": GrantLinkFormSet(
                    self.request.POST or None,
                    self.request.FILES or None,
                    prefix="links",
                )
            }


class GrantUpdateView(LoginRequiredMixin, GrantInline, UpdateView):
    def get_context_data(self, **kwargs):
        ctx = super(GrantUpdateView, self).get_context_data(**kwargs)
        ctx["named_formsets"] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        if self.request.method == "GET":
            return {"links": GrantLinkFormSet(prefix="links")}
        else:
            return {
                "links": GrantLinkFormSet(
                    self.request.POST or None,
                    self.request.FILES or None,
                    prefix="links",
                )
            }


class GrantDeleteView(LoginRequiredMixin, DeleteView):
    model = Grant
    queryset = Grant.objects.all()
    template_name = "claims/confirm_delete.html"
    success_url = reverse_lazy("grant_list")


class GrantLinkDeleteView(LoginRequiredMixin, DeleteView):
    model = GrantLink
    queryset = GrantLink.objects.all()
    template_name = "claims/confirm_delete.html"


class GrantReviewListView(LoginRequiredMixin, ListView):
    model = GrantReview
    template_name = "claims/grant_reviews.html"
    context_object_name = "grantreviews"

    def get_queryset(self):
        return GrantReview.objects.filter(user_id=self.request.user)


class GrantReviewCreateView(LoginRequiredMixin, CreateView):
    model = GrantReview
    form_class = GrantReviewForm
    template_name = "claims/grant_review_form.html"
    success_url = reverse_lazy("grantreview_list")

    def form_valid(self, form):
        grantreview = form.save(commit=False)
        grantreview.user_id = self.request.user
        grantreview.save()
        return super().form_valid(form)


class GrantReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = GrantReview
    form_class = GrantReviewForm
    template_name = "claims/grant_review_form.html"
    success_url = reverse_lazy("grantreview_list")


class GrantReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = GrantReview
    queryset = GrantReview.objects.all()
    template_name = "claims/confirm_delete.html"
    success_url = reverse_lazy("grantreview_list")


class EditorialBoardListView(LoginRequiredMixin, ListView):
    model = EditorialBoard
    template_name = "claims/editorial_boards.html"
    context_object_name = "editorial_boards"

    def get_queryset(self):
        return EditorialBoard.objects.filter(user_id=self.request.user)


class EditorialBoardCreateView(LoginRequiredMixin, CreateView):
    model = EditorialBoard
    form_class = EditorialBoardForm
    template_name = "claims/editorial_board_form.html"
    success_url = reverse_lazy("editorial_board_list")

    def form_valid(self, form):
        editorial_board = form.save(commit=False)
        editorial_board.user_id = self.request.user
        editorial_board.save()
        return super().form_valid(form)


class EditorialBoardUpdateView(LoginRequiredMixin, UpdateView):
    model = EditorialBoard
    form_class = EditorialBoardForm
    template_name = "claims/editorial_board_form.html"
    success_url = reverse_lazy("editorial_board_list")


class EditorialBoardDeleteView(LoginRequiredMixin, DeleteView):
    model = EditorialBoard
    queryset = EditorialBoard.objects.all()
    template_name = "claims/confirm_delete.html"
    success_url = reverse_lazy("editorial_board_list")


class CommitteeListView(LoginRequiredMixin, ListView):
    model = CommitteeWork
    template_name = "claims/committees.html"
    context_object_name = "committees"

    def get_queryset(self):
        return CommitteeWork.objects.filter(user_id=self.request.user)


class CommitteeCreateView(LoginRequiredMixin, CreateView):
    model = CommitteeWork
    form_class = CommitteeWorkForm
    template_name = "claims/committee_form.html"
    success_url = reverse_lazy("committee_list")

    def form_valid(self, form):
        committee = form.save(commit=False)
        committee.user_id = self.request.user
        committee.save()
        return super().form_valid(form)


class CommitteeUpdateView(LoginRequiredMixin, UpdateView):
    model = CommitteeWork
    form_class = CommitteeWorkForm
    template_name = "claims/committee_form.html"
    success_url = reverse_lazy("committee_list")


class CommitteeDeleteView(LoginRequiredMixin, DeleteView):
    model = CommitteeWork
    queryset = CommitteeWork.objects.all()
    template_name = "claims/confirm_delete.html"
    success_url = reverse_lazy("committee_list")


class LectureListView(LoginRequiredMixin, ListView):
    model = Lecture
    template_name = "claims/lectures.html"
    context_object_name = "lectures"

    def get_queryset(self):
        return Lecture.objects.filter(user_id=self.request.user)


class LectureCreateView(LoginRequiredMixin, CreateView):
    model = Lecture
    form_class = LectureForm
    template_name = "claims/lecture_form.html"
    success_url = reverse_lazy("lecture_list")

    def form_valid(self, form):
        lecture = form.save(commit=False)
        lecture.user_id = self.request.user
        lecture.save()
        return super().form_valid(form)


class LectureUpdateView(LoginRequiredMixin, UpdateView):
    model = Lecture
    form_class = LectureForm
    template_name = "claims/lecture_form.html"
    success_url = reverse_lazy("lecture_list")


class LectureDeleteView(LoginRequiredMixin, DeleteView):
    model = Lecture
    queryset = Lecture.objects.all()
    template_name = "claims/confirm_delete.html"
    success_url = reverse_lazy("lecture_list")


class ExamListView(LoginRequiredMixin, ListView):
    model = Exam
    template_name = "claims/exams.html"
    context_object_name = "exams"

    def get_queryset(self):
        return Exam.objects.filter(user_id=self.request.user)


class ExamCreateView(LoginRequiredMixin, CreateView):
    model = Exam
    form_class = ExamForm
    template_name = "claims/exam_form.html"
    success_url = reverse_lazy("exam_list")

    def form_valid(self, form):
        exam = form.save(commit=False)
        exam.user_id = self.request.user
        exam.save()
        return super().form_valid(form)


class ExamUpdateView(LoginRequiredMixin, UpdateView):
    model = Exam
    form_class = ExamForm
    template_name = "claims/exam_form.html"
    success_url = reverse_lazy("exam_list")


class ExamDeleteView(LoginRequiredMixin, DeleteView):
    model = Exam
    queryset = Exam.objects.all()
    template_name = "claims/confirm_delete.html"
    success_url = reverse_lazy("exam_list")


class SupervisionListView(LoginRequiredMixin, ListView):
    model = Supervision
    template_name = "claims/supervision.html"
    context_object_name = "supervisions"

    def get_queryset(self):
        return Supervision.objects.filter(user_id=self.request.user)


class SupervisionCreateView(LoginRequiredMixin, CreateView):
    model = Supervision
    form_class = SupervisionForm
    template_name = "claims/supervision_form.html"
    success_url = reverse_lazy("supervision_list")

    def form_valid(self, form):
        supervision = form.save(commit=False)
        supervision.user_id = self.request.user
        supervision.save()
        return super().form_valid(form)


class SupervisionUpdateView(LoginRequiredMixin, UpdateView):
    model = Supervision
    form_class = SupervisionForm
    template_name = "claims/supervision_form.html"
    success_url = reverse_lazy("supervision_list")


class SupervisionDeleteView(LoginRequiredMixin, DeleteView):
    model = Supervision
    queryset = Supervision.objects.all()
    template_name = "claims/confirm_delete.html"
    success_url = reverse_lazy("supervision_list")
