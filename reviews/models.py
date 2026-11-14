from django.conf import settings
from django.db import models


class Project(models.Model):
    STATUS_CHOICES = [("planning", "Before reading"), ("reading", "Reading"),
                      ("reflecting", "Reflecting"), ("drafting", "Drafting"), ("ready", "Ready to publish")]
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="memoir_projects")
    title = models.CharField(max_length=240)
    author = models.CharField(max_length=180)
    edition = models.CharField(max_length=160, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="planning")
    why_read = models.TextField(blank=True)
    what_know = models.TextField(blank=True)
    curiosity = models.TextField(blank=True)
    reflection_summary = models.TextField(blank=True)
    reflection_moments = models.TextField(blank=True)
    reflection_changed = models.TextField(blank=True)
    reflection_strengths = models.TextField(blank=True)
    reflection_weaknesses = models.TextField(blank=True)
    reflection_resilience = models.TextField(blank=True)
    reflection_recommend = models.TextField(blank=True)
    checklist = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("project_workspace", kwargs={"pk": self.pk})


class ReadingEntry(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="entries")
    section = models.CharField(max_length=220)
    pages = models.CharField(max_length=100, blank=True)
    facts = models.TextField(blank=True)
    reaction = models.TextField(blank=True)
    question = models.TextField(blank=True)
    writing = models.TextField(blank=True)
    themes = models.CharField(max_length=250, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at", "id"]

    def __str__(self):
        return self.section


class Evidence(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="evidence_items")
    point = models.CharField(max_length=300, help_text="The point you want to make in your review")
    scene = models.TextField(help_text="What the book actually shows")
    interpretation = models.TextField(blank=True, help_text="Why you think it supports your point")
    reader_value = models.TextField(blank=True, help_text="Why this matters to a potential reader")
    reference = models.CharField(max_length=150, blank=True, help_text="Chapter/page for your edition")
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at", "id"]


class Draft(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name="draft")
    headline = models.CharField(max_length=250, blank=True)
    introduction = models.TextField(blank=True)
    quick_verdict = models.TextField(blank=True)
    overview = models.TextField(blank=True)
    struggles = models.TextField(blank=True)
    turning_points = models.TextField(blank=True)
    lasting_impression = models.TextField(blank=True)
    craft = models.TextField(blank=True)
    reader_fit = models.TextField(blank=True)
    final_verdict = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Draft: {self.project.title}"
