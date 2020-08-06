"""
Serilizers for the task application API
"""

# Django
from django.contrib.auth.models import User

# Third Party
from rest_framework import serializers

# MuckRock
from muckrock.agency.models import Agency
from muckrock.foia.models import FOIACommunication, FOIARequest
from muckrock.jurisdiction.models import Jurisdiction
from muckrock.task.models import (
    FlaggedTask,
    NewAgencyTask,
    OrphanTask,
    ResponseTask,
    SnailMailTask,
    Task,
)


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Task model"""

    assigned = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), style={"base_template": "input.html"}
    )
    orphantask = serializers.PrimaryKeyRelatedField(
        queryset=OrphanTask.objects.all(), style={"base_template": "input.html"}
    )
    snailmailtask = serializers.PrimaryKeyRelatedField(
        queryset=SnailMailTask.objects.all(), style={"base_template": "input.html"}
    )
    flaggedtask = serializers.PrimaryKeyRelatedField(
        queryset=FlaggedTask.objects.all(), style={"base_template": "input.html"}
    )
    newagencytask = serializers.PrimaryKeyRelatedField(
        queryset=NewAgencyTask.objects.all(), style={"base_template": "input.html"}
    )
    responsetask = serializers.PrimaryKeyRelatedField(
        queryset=ResponseTask.objects.all(), style={"base_template": "input.html"}
    )

    class Meta:
        model = Task
        fields = (
            "id",
            "date_created",
            "date_done",
            "resolved",
            "assigned",
            "orphantask",
            "snailmailtask",
            "rejectedemailtask",
            "flaggedtask",
            "newagencytask",
            "responsetask",
        )


class OrphanTaskSerializer(serializers.ModelSerializer):
    """Serializer for OrphanTask model"""

    assigned = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), style={"base_template": "input.html"}
    )
    resolved_by = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), style={"base_template": "input.html"}
    )
    communication = serializers.PrimaryKeyRelatedField(
        queryset=FOIACommunication.objects.all(), style={"base_template": "input.html"}
    )

    class Meta:
        model = OrphanTask
        fields = "__all__"


class SnailMailTaskSerializer(serializers.ModelSerializer):
    """Serializer for SnailMailTask model"""

    assigned = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), style={"base_template": "input.html"}
    )
    resolved_by = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), style={"base_template": "input.html"}
    )
    communication = serializers.PrimaryKeyRelatedField(
        queryset=FOIACommunication.objects.all(), style={"base_template": "input.html"}
    )
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), style={"base_template": "input.html"}
    )

    class Meta:
        model = SnailMailTask
        fields = "__all__"


class FlaggedTaskSerializer(serializers.ModelSerializer):
    """Serializer for FlaggedTask model"""

    assigned = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), style={"base_template": "input.html"}
    )
    resolved_by = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), style={"base_template": "input.html"}
    )
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), style={"base_template": "input.html"}
    )
    foia = serializers.PrimaryKeyRelatedField(
        queryset=FOIARequest.objects.all(), style={"base_template": "input.html"}
    )
    agency = serializers.PrimaryKeyRelatedField(
        queryset=Agency.objects.all(), style={"base_template": "input.html"}
    )
    jurisdiction = serializers.PrimaryKeyRelatedField(
        queryset=Jurisdiction.objects.all(), style={"base_template": "input.html"}
    )

    class Meta:
        model = FlaggedTask
        fields = "__all__"


class NewAgencyTaskSerializer(serializers.ModelSerializer):
    """Serializer for NewAgencyTask model"""

    assigned = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), style={"base_template": "input.html"}
    )
    resolved_by = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), style={"base_template": "input.html"}
    )
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), style={"base_template": "input.html"}
    )
    agency = serializers.PrimaryKeyRelatedField(
        queryset=Agency.objects.all(), style={"base_template": "input.html"}
    )

    class Meta:
        model = NewAgencyTask
        fields = "__all__"


class ResponseTaskSerializer(serializers.ModelSerializer):
    """Serializer for ResponseTask model"""

    assigned = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), style={"base_template": "input.html"}
    )
    resolved_by = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), style={"base_template": "input.html"}
    )
    communication = serializers.PrimaryKeyRelatedField(
        queryset=FOIACommunication.objects.all(), style={"base_template": "input.html"}
    )

    class Meta:
        model = ResponseTask
        fields = "__all__"
