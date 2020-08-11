"""
Filters for the project application
"""

# Django
from django.contrib.auth.models import User

# Third Party
import django_filters
from autocomplete_light import shortcuts as autocomplete_light

# MuckRock
from muckrock.core import autocomplete
from muckrock.project.models import Project
from muckrock.tags.models import Tag


class ProjectFilterSet(django_filters.FilterSet):
    """Allows a project to be filtered by whether it's featured or by its user."""

    contributors = django_filters.ModelMultipleChoiceFilter(
        queryset=User.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(
            url="user-autocomplete",
            attrs={"data-placeholder": "Search users", "data-minimum-input-length": 2},
        ),
    )
    tags = django_filters.ModelMultipleChoiceFilter(
        name="tags__name",
        queryset=Tag.objects.all(),
        label="Tags",
        widget=autocomplete.ModelSelect2Multiple(
            url="tag-autocomplete", attrs={"data-placeholder": "Search tags"}
        ),
    )

    class Meta:
        model = Project
        fields = ["contributors"]
