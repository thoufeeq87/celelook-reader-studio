# Celelook Reader Studio

A beginner-friendly, private Django memoir reading and review workflow.

**Stack:** Python 3.11+, Django 5.2+, SQLite (development), Tailwind CSS (development CDN).

## What it does

1. Create a memoir project (with a prefilled *The Glass Castle* option).
2. Record **before-reading** thoughts: why, what you know, and what you're curious about.
3. Save **reading sessions** with Fact / Reaction / Question, writing observations and page references.
4. Complete an **after-reading reflection** about the memoir, including strengths and weaknesses.
5. Collect an **evidence bank** with Point → Scene → Explanation → Reader value and a verified toggle.
6. Draft a **Celelook review** using guided editorial sections.
7. Complete a **prepublication checklist**, then **download Markdown** for review and separate publication.

All reading data belongs to the logged-in user. No automatic publishing, scraping, AI-generated claims or public review pages are included.

## Run locally

```bash
cd celelook_reader
python -m venv .venv
# macOS / Linux:
source .venv/bin/activate
# Windows PowerShell:
# .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/`, create an account and choose **Use this book** to start *The Glass Castle*.

Optional checks:

```bash
python manage.py check
python manage.py test
```

## Integrating into an existing Celelook site

If Celelook already runs Django, move the `reviews` app into that project, add `reviews` to `INSTALLED_APPS`, include `reviews.urls` under a suitable prefix like `/studio/`, and merge the templates with your site's base template. Don't overwrite your existing settings or user data. Add migrations and test within your current project.

## Production notes (important)

This is a **starter with Railway-compatible deployment settings**, not a security-audited production application.

- Tailwind's Play CDN is used only for easy local evaluation. For production, install Tailwind CSS and compile a versioned, purged CSS asset into Django static files (then remove the Play CDN script). See https://tailwindcss.com/docs/installation.
- Set `DJANGO_SECRET_KEY` to a long random value, `DJANGO_DEBUG=0`, proper `DJANGO_ALLOWED_HOSTS` and `DJANGO_CSRF_TRUSTED_ORIGINS`.
- Run behind HTTPS with a production WSGI/ASGI server and an appropriate static-files setup.
- Use PostgreSQL, backups, appropriate access controls, secure password reset and account policies before inviting real users.
- Consider privacy policies, deletion/export of private notes, rate limiting, audit logs and review ownership if this becomes a multi-user product.
- The status "Ready to publish" only reflects checked boxes; it is not an automatic independent fact check.
- No book content or third-party quotations are bundled; write original notes and verify any book quotations from your own copy.

## Environment variables

| Variable | Example | Description |
|---|---|---|
| `DJANGO_SECRET_KEY` | long-random-string | Required for production |
| `DJANGO_DEBUG` | `0` | Disable Django debug in production |
| `DJANGO_ALLOWED_HOSTS` | `celelook.com,www.celelook.com` | Comma-separated allowed hosts |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | `https://celelook.com` | Trusted POST origins |
| `DJANGO_SECURE_SSL_REDIRECT` | `1` | HTTPS redirect in production |
| `DJANGO_HSTS_SECONDS` | `3600` | HSTS duration |

## Folder structure

- `celelook/` — Django project settings and routing
- `reviews/models.py` — books, reading entries, evidence and review drafts
- `reviews/forms.py` — guided forms
- `reviews/views.py` — authenticated CRUD, checklist, Markdown export
- `reviews/templates/` — Tailwind UI
- `reviews/migrations/` — initial database schema

## Suggested future upgrades

Autosaving, chapter progress tracking, PDF export, editorial review approvals, optional AI coaching that never fabricates firsthand reactions, and live publication integration with your existing Celelook CMS.

## Railway deployment

This repository includes `railway.toml`, `Procfile` and a pinned Python version for a Railway service.

1. Create a private GitHub repository and upload all files at the root (not an outer folder).
2. In Railway, deploy that repository as a new service.
3. Add a **new PostgreSQL service dedicated to Reader Studio** and reference its `DATABASE_URL` from the Django service. Do **not** reuse or delete your existing Celelook database.
4. Set `DJANGO_SECRET_KEY` to a unique random string; `DJANGO_DEBUG=0`; `DJANGO_ALLOWED_HOSTS` to the assigned Railway domain (or `.up.railway.app` for a temporary test); `DJANGO_CSRF_TRUSTED_ORIGINS` to the full HTTPS URL.
5. Generate a public domain and check deployment logs, migrations, login and saved notes.

The present UI loads Tailwind Play CDN, which is intended for development. Replace it with a built static CSS asset before using as a full production app. Do not invite users or store sensitive reading notes until production review, backups and account controls are completed.
