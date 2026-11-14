from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .models import Draft, Project, ReadingEntry


class ReaderStudioTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.owner = User.objects.create_user("reader1", password="TestPass12345!")
        self.other = User.objects.create_user("reader2", password="TestPass12345!")
        self.project = Project.objects.create(owner=self.owner, title="The Glass Castle", author="Jeannette Walls")

    def test_login_required(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)

    def test_private_project_is_not_visible_to_other_user(self):
        self.client.force_login(self.other)
        response = self.client.get(reverse("project_workspace", args=[self.project.pk]))
        self.assertEqual(response.status_code, 404)

    def test_private_entry_cannot_be_deleted_by_other_user(self):
        entry = ReadingEntry.objects.create(project=self.project, section="Opening")
        self.client.force_login(self.other)
        response = self.client.post(reverse("entry_delete", args=[self.project.pk, entry.pk]))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(ReadingEntry.objects.filter(pk=entry.pk).exists())

    def test_entry_create_updates_project_status(self):
        self.client.force_login(self.owner)
        response = self.client.post(reverse("entry_create", args=[self.project.pk]), {
            "section": "Opening", "pages": "1-10", "facts": "A scene described in the book",
            "reaction": "I was curious", "question": "What happens next?", "writing": "A contrasting opening",
            "themes": "family"})
        self.assertEqual(response.status_code, 302)
        self.project.refresh_from_db()
        self.assertEqual(self.project.status, "reading")
        self.assertEqual(self.project.entries.count(), 1)

    def test_export_is_private_and_draft_only(self):
        Draft.objects.create(project=self.project, headline="My honest review", final_verdict="Thoughtful and complex.")
        url = reverse("export_markdown", args=[self.project.pk])
        self.client.force_login(self.other)
        self.assertEqual(self.client.get(url).status_code, 404)
        self.client.force_login(self.owner)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("My honest review", response.content.decode())
        self.assertIn("Thoughtful and complex.", response.content.decode())

    def test_checklist_requires_post(self):
        self.client.force_login(self.owner)
        response = self.client.get(reverse("checklist_update", args=[self.project.pk]))
        self.assertEqual(response.status_code, 405)
