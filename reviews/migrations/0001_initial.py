# Generated for Celelook Reader Studio starter application.
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(name="Project", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("title", models.CharField(max_length=240)), ("author", models.CharField(max_length=180)),
            ("edition", models.CharField(blank=True, max_length=160)),
            ("status", models.CharField(choices=[("planning", "Before reading"), ("reading", "Reading"), ("reflecting", "Reflecting"), ("drafting", "Drafting"), ("ready", "Ready to publish")], default="planning", max_length=20)),
            ("why_read", models.TextField(blank=True)), ("what_know", models.TextField(blank=True)), ("curiosity", models.TextField(blank=True)),
            ("reflection_summary", models.TextField(blank=True)), ("reflection_moments", models.TextField(blank=True)),
            ("reflection_changed", models.TextField(blank=True)), ("reflection_strengths", models.TextField(blank=True)),
            ("reflection_weaknesses", models.TextField(blank=True)), ("reflection_resilience", models.TextField(blank=True)),
            ("reflection_recommend", models.TextField(blank=True)), ("checklist", models.JSONField(blank=True, default=dict)),
            ("created_at", models.DateTimeField(auto_now_add=True)), ("updated_at", models.DateTimeField(auto_now=True)),
            ("owner", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="memoir_projects", to=settings.AUTH_USER_MODEL)),
        ], options={"ordering": ["-updated_at"]}),
        migrations.CreateModel(name="ReadingEntry", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("section", models.CharField(max_length=220)), ("pages", models.CharField(blank=True, max_length=100)),
            ("facts", models.TextField(blank=True)), ("reaction", models.TextField(blank=True)),
            ("question", models.TextField(blank=True)), ("writing", models.TextField(blank=True)),
            ("themes", models.CharField(blank=True, max_length=250)), ("created_at", models.DateTimeField(auto_now_add=True)),
            ("project", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="entries", to="reviews.project")),
        ], options={"ordering": ["created_at", "id"]}),
        migrations.CreateModel(name="Evidence", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("point", models.CharField(help_text="The point you want to make in your review", max_length=300)),
            ("scene", models.TextField(help_text="What the book actually shows")),
            ("interpretation", models.TextField(blank=True, help_text="Why you think it supports your point")),
            ("reader_value", models.TextField(blank=True, help_text="Why this matters to a potential reader")),
            ("reference", models.CharField(blank=True, help_text="Chapter/page for your edition", max_length=150)),
            ("verified", models.BooleanField(default=False)), ("created_at", models.DateTimeField(auto_now_add=True)),
            ("project", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="evidence_items", to="reviews.project")),
        ], options={"ordering": ["created_at", "id"]}),
        migrations.CreateModel(name="Draft", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("headline", models.CharField(blank=True, max_length=250)),
            ("introduction", models.TextField(blank=True)), ("quick_verdict", models.TextField(blank=True)),
            ("overview", models.TextField(blank=True)), ("struggles", models.TextField(blank=True)),
            ("turning_points", models.TextField(blank=True)), ("lasting_impression", models.TextField(blank=True)),
            ("craft", models.TextField(blank=True)), ("reader_fit", models.TextField(blank=True)),
            ("final_verdict", models.TextField(blank=True)), ("updated_at", models.DateTimeField(auto_now=True)),
            ("project", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="draft", to="reviews.project")),
        ]),
    ]
