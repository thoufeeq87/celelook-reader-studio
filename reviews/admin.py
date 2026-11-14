from django.contrib import admin
from .models import Project, ReadingEntry, Evidence, Draft

# Private reading data is user-owned. Avoid making it browsable in the shared admin
# unless you add explicit per-user object permissions for staff.
