from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.utils.text import slugify
from .forms import (SignupForm, ProjectForm, PreparationForm, EntryForm,
                    EvidenceForm, ReflectionForm, DraftForm)
from .models import Project, ReadingEntry, Evidence, Draft

CHECKS = [
    ("facts", "Names, events and the edition are fact-checked"),
    ("references", "Page/scene references have been verified"),
    ("original", "Opinions reflect my own actual reading experience"),
    ("balanced", "I explain strengths and weaknesses with examples"),
    ("claims", "I separate the author's account from independently verified facts"),
    ("sensitive", "Sensitive life experiences are treated respectfully"),
    ("spoilers", "Spoilers are avoided or clearly labeled"),
    ("suitability", "Reader suitability and content considerations are covered"),
    ("seo", "Title, headings and article summary are clear"),
    ("disclosure", "Review copies and affiliate relationships are disclosed if relevant"),
    ("proofread", "Article has been proofread and is ready for editorial review"),
]
TABS = [
    ("prepare", "01 · Prepare"), ("read", "02 · Read"), ("reflect", "03 · Reflect"),
    ("evidence", "04 · Evidence"), ("draft", "05 · Draft"), ("publish", "06 · Publish"),
]


def signup(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = SignupForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("dashboard")
    return render(request, "registration/signup.html", {"form": form})


@login_required
def dashboard(request):
    return render(request, "reviews/dashboard.html", {"projects": Project.objects.filter(owner=request.user)})


@login_required
def project_create(request):
    initial = {"title": "The Glass Castle", "author": "Jeannette Walls"} if request.GET.get("example") == "glass-castle" else {}
    form = ProjectForm(request.POST or None, initial=initial)
    if request.method == "POST" and form.is_valid():
        project = form.save(commit=False)
        project.owner = request.user
        project.save()
        messages.success(request, "Project created. Start with your own pre-reading thoughts.")
        return redirect("prepare", pk=project.pk)
    return render(request, "reviews/form.html", {"form": form, "page_title": "Create a memoir project", "help_text": "One project follows one book from first impressions to final review.", "cancel_url": "/"})


def owned(request, pk):
    return get_object_or_404(Project, pk=pk, owner=request.user)


@login_required
def project_workspace(request, pk):
    project = owned(request, pk)
    tab = request.GET.get("tab", "prepare")
    if tab not in dict(TABS):
        tab = "prepare"
    draft = Draft.objects.filter(project=project).first()
    data = {"project": project, "tab": tab, "tabs": TABS, "entries": project.entries.all(),
            "evidence_items": project.evidence_items.all(), "draft": draft,
            "checks": [(key, label, bool(project.checklist.get(key, False))) for key, label in CHECKS],
            "checked_count": sum(bool(project.checklist.get(key, False)) for key, _ in CHECKS),
            "check_total": len(CHECKS)}
    return render(request, "reviews/workspace.html", data)


def project_form(request, pk, form_class, title, tab, field=None):
    project = owned(request, pk)
    instance = getattr(project, field) if field else project
    form = form_class(request.POST or None, instance=instance)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Saved successfully.")
        return redirect(f"{project.get_absolute_url()}?tab={tab}")
    return render(request, "reviews/form.html", {"form": form, "project": project,
                  "page_title": title, "cancel_url": f"{project.get_absolute_url()}?tab={tab}"})


@login_required
def prepare(request, pk):
    return project_form(request, pk, PreparationForm, "Before you read", "prepare")


@login_required
def reflect(request, pk):
    return project_form(request, pk, ReflectionForm, "After finishing: reflect", "reflect")


@login_required
def entry_create(request, pk):
    project = owned(request, pk)
    form = EntryForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        entry = form.save(commit=False)
        entry.project = project
        entry.save()
        if project.status == "planning":
            project.status = "reading"
            project.save(update_fields=["status", "updated_at"])
        messages.success(request, "Your reading session was saved.")
        return redirect(f"{project.get_absolute_url()}?tab=read")
    return render(request, "reviews/form.html", {"form": form, "project": project,
                  "page_title": "New reading session", "help_text": "One or two sentences per field is enough. Do not invent details you can't remember.",
                  "cancel_url": f"{project.get_absolute_url()}?tab=read"})


@login_required
def entry_edit(request, pk, entry_id):
    project = owned(request, pk)
    entry = get_object_or_404(ReadingEntry, pk=entry_id, project=project)
    form = EntryForm(request.POST or None, instance=entry)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Reading entry updated.")
        return redirect(f"{project.get_absolute_url()}?tab=read")
    return render(request, "reviews/form.html", {"form": form, "project": project, "page_title": "Edit reading session", "cancel_url": f"{project.get_absolute_url()}?tab=read"})


@login_required
@require_POST
def entry_delete(request, pk, entry_id):
    project = owned(request, pk)
    get_object_or_404(ReadingEntry, pk=entry_id, project=project).delete()
    messages.success(request, "Reading entry deleted.")
    return redirect(f"{project.get_absolute_url()}?tab=read")


@login_required
def evidence_create(request, pk):
    project = owned(request, pk)
    form = EvidenceForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        item = form.save(commit=False)
        item.project = project
        item.save()
        messages.success(request, "Evidence saved.")
        return redirect(f"{project.get_absolute_url()}?tab=evidence")
    return render(request, "reviews/form.html", {"form": form, "project": project, "page_title": "Add evidence for your review", "help_text": "Point → Scene → Explanation → Reader value. Mark verified only after checking the book.", "cancel_url": f"{project.get_absolute_url()}?tab=evidence"})


@login_required
def evidence_edit(request, pk, evidence_id):
    project = owned(request, pk)
    item = get_object_or_404(Evidence, pk=evidence_id, project=project)
    form = EvidenceForm(request.POST or None, instance=item)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect(f"{project.get_absolute_url()}?tab=evidence")
    return render(request, "reviews/form.html", {"form": form, "project": project, "page_title": "Edit evidence", "cancel_url": f"{project.get_absolute_url()}?tab=evidence"})


@login_required
@require_POST
def evidence_delete(request, pk, evidence_id):
    project = owned(request, pk)
    get_object_or_404(Evidence, pk=evidence_id, project=project).delete()
    return redirect(f"{project.get_absolute_url()}?tab=evidence")


@login_required
def draft_edit(request, pk):
    project = owned(request, pk)
    draft, _ = Draft.objects.get_or_create(project=project)
    form = DraftForm(request.POST or None, instance=draft)
    if request.method == "POST" and form.is_valid():
        form.save()
        if project.status in ("planning", "reading", "reflecting"):
            project.status = "drafting"
            project.save(update_fields=["status", "updated_at"])
        messages.success(request, "Draft saved privately. Nothing was published.")
        return redirect(f"{project.get_absolute_url()}?tab=draft")
    return render(request, "reviews/form.html", {"form": form, "project": project,
                  "page_title": "Write your Celelook review", "help_text": "Write from your notes. Leave sections blank until you have genuine observations. Saving does NOT publish the review.",
                  "cancel_url": f"{project.get_absolute_url()}?tab=draft"})


@login_required
@require_POST
def checklist_update(request, pk):
    project = owned(request, pk)
    permitted = {key for key, _ in CHECKS}
    project.checklist = {key: key in request.POST for key in permitted}
    project.status = "ready" if all(project.checklist.values()) else ("drafting" if Draft.objects.filter(project=project).exists() else project.status)
    project.save(update_fields=["checklist", "status", "updated_at"])
    messages.success(request, "Checklist updated. No content was published.")
    return redirect(f"{project.get_absolute_url()}?tab=publish")


def md_section(title, content):
    return f"## {title}\n\n{content.strip()}\n\n" if content and content.strip() else ""


@login_required
def export_markdown(request, pk):
    project = owned(request, pk)
    draft = Draft.objects.filter(project=project).first()
    if draft is None:
        messages.error(request, "Create a draft before exporting.")
        return redirect(f"{project.get_absolute_url()}?tab=draft")
    title = draft.headline or f"{project.title} by {project.author}: A Celelook Review"
    md = f"# {title}\n\n*Book: {project.title} · Author: {project.author}*\n\n"
    fields = [("Why I read it", draft.introduction), ("Quick verdict", draft.quick_verdict),
              ("What it's about", draft.overview), ("The human experience", draft.struggles),
              ("Resilience and turning points", draft.turning_points),
              ("What stayed with me", draft.lasting_impression),
              ("Writing: strengths and weaknesses", draft.craft),
              ("Before you read", draft.reader_fit), ("Final verdict", draft.final_verdict)]
    for heading, content in fields:
        md += md_section(heading, content)
    md += "\n---\n*Exported from Celelook Reader Studio. Review editorially before publishing.*\n"
    response = HttpResponse(md, content_type="text/markdown; charset=utf-8")
    response["Content-Disposition"] = f'attachment; filename="{slugify(project.title) or "memoir"}-review.md"'
    return response
