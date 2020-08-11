# -*- coding: utf-8 -*-
"""
Admin for data set application
"""

# Django
from django import forms
from django.contrib import admin
from django.contrib.auth.models import User

# Third Party
from reversion.admin import VersionAdmin

# MuckRock
from muckrock.core import autocomplete
from muckrock.dataset.models import DataField, DataSet


class DataFieldInline(admin.TabularInline):
    """Inline for a data field"""

    model = DataField
    prepopulated_fields = {"slug": ("name",)}
    extra = 0


class DataSetForm(forms.ModelForm):
    """Form with autocomplete for user"""

    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=autocomplete.ModelSelect2(
            url="user-autocomplete", attrs={"data-placeholder": "User?"}
        ),
    )

    class Meta:
        model = DataSet
        fields = "__all__"


class DataSetAdmin(VersionAdmin):
    """Admin for a data set"""

    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "user", "created_datetime")
    list_filter = ("status",)
    date_hieracrhy = "created_datetime"
    search_fields = ("name",)
    readonly_fields = ("created_datetime", "status")
    form = DataSetForm
    inlines = [DataFieldInline]
    save_on_top = True


admin.site.register(DataSet, DataSetAdmin)
