from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Project, ReadingEntry, Evidence, Draft

INPUT = "w-full rounded-xl border border-stone-300 bg-white px-3 py-2.5 text-sm text-stone-900 placeholder:text-stone-400 focus:border-teal-700 focus:outline-none focus:ring-2 focus:ring-teal-100"
TEXTAREA = INPUT + " min-h-24"


class StyledFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            widget.attrs["class"] = INPUT if not isinstance(widget, forms.Textarea) else TEXTAREA
            if isinstance(widget, forms.Textarea):
                widget.attrs.setdefault("rows", 3)


class SignupForm(StyledFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]


class ProjectForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Project
        fields = ["title", "author", "edition"]


class PreparationForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Project
        fields = ["why_read", "what_know", "curiosity"]
        labels = {
            "why_read": "Why do I want to read this book?",
            "what_know": "What do I already know? (It's okay to write 'nothing yet')",
            "curiosity": "What would I like to discover?",
        }


class EntryForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = ReadingEntry
        fields = ["section", "pages", "facts", "reaction", "question", "writing", "themes"]
        labels = {"section": "Chapter / session", "pages": "Pages or ebook location",
                  "facts": "F — What happened? (facts)", "reaction": "R — What did I feel or think?",
                  "question": "Q — What do I wonder about?", "writing": "What did I notice about the writing?",
                  "themes": "Possible themes (optional)"}


class EvidenceForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Evidence
        fields = ["point", "scene", "interpretation", "reader_value", "reference", "verified"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["verified"].widget.attrs["class"] = "h-4 w-4 accent-teal-700"


class ReflectionForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Project
        fields = ["reflection_summary", "reflection_moments", "reflection_changed", "reflection_strengths",
                  "reflection_weaknesses", "reflection_resilience", "reflection_recommend"]
        labels = {
            "reflection_summary": "What is this memoir really about, in my own words?",
            "reflection_moments": "Which three moments stayed with me?",
            "reflection_changed": "How did my interpretation change while reading?",
            "reflection_strengths": "What worked well in the storytelling?",
            "reflection_weaknesses": "What didn't work, or what did I question?",
            "reflection_resilience": "How does the book portray survival, resilience, or starting over?",
            "reflection_recommend": "Who should read this, and who might prefer something else?",
        }


class DraftForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Draft
        fields = ["headline", "introduction", "quick_verdict", "overview", "struggles", "turning_points",
                  "lasting_impression", "craft", "reader_fit", "final_verdict"]
        labels = {"headline": "Working SEO headline", "introduction": "Why I picked up this memoir",
                  "quick_verdict": "My quick verdict", "overview": "What is this book about? (spoiler-light)",
                  "struggles": "The human experience: key struggles and themes",
                  "turning_points": "Resilience and turning points — avoid forced happy endings",
                  "lasting_impression": "What stayed with me — grounded in scenes",
                  "craft": "How well is it written? Strengths and weaknesses",
                  "reader_fit": "Before you read: who it's for and content considerations",
                  "final_verdict": "Final verdict and recommendation"}
