from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("projects/new/", views.project_create, name="project_create"),
    path("projects/<int:pk>/", views.project_workspace, name="project_workspace"),
    path("projects/<int:pk>/prepare/", views.prepare, name="prepare"),
    path("projects/<int:pk>/reading/new/", views.entry_create, name="entry_create"),
    path("projects/<int:pk>/reading/<int:entry_id>/edit/", views.entry_edit, name="entry_edit"),
    path("projects/<int:pk>/reading/<int:entry_id>/delete/", views.entry_delete, name="entry_delete"),
    path("projects/<int:pk>/reflect/", views.reflect, name="reflect"),
    path("projects/<int:pk>/evidence/new/", views.evidence_create, name="evidence_create"),
    path("projects/<int:pk>/evidence/<int:evidence_id>/edit/", views.evidence_edit, name="evidence_edit"),
    path("projects/<int:pk>/evidence/<int:evidence_id>/delete/", views.evidence_delete, name="evidence_delete"),
    path("projects/<int:pk>/draft/", views.draft_edit, name="draft_edit"),
    path("projects/<int:pk>/checklist/", views.checklist_update, name="checklist_update"),
    path("projects/<int:pk>/export/", views.export_markdown, name="export_markdown"),
]
