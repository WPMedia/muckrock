"""
Filters for the Agency application
"""

# Third Party
import django_filters
from autocomplete_light import shortcuts as autocomplete_light

# MuckRock
from muckrock.agency.models import Agency
from muckrock.jurisdiction.models import Jurisdiction


class AgencyFilterSet(django_filters.FilterSet):
    """Allows agencies to be filtered by jurisdiction."""

    jurisdiction = django_filters.ModelChoiceFilter(
        queryset=Jurisdiction.objects.filter(hidden=False),
        widget=autocomplete_light.ChoiceWidget("JurisdictionAutocomplete"),
    )

    class Meta:
        model = Agency
        fields = ["jurisdiction"]
