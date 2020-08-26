"""
Task factories, for testing
"""

# Third Party
import factory

# MuckRock
from muckrock import task


class OrphanTaskFactory(factory.django.DjangoModelFactory):
    """A factory for creating OrphanTask objects."""

    class Meta:
        model = task.models.OrphanTask

    reason = "bs"
    communication = factory.SubFactory(
        "muckrock.foia.factories.FOIACommunicationFactory"
    )
    address = factory.Faker("email")


class SnailMailTaskFactory(factory.django.DjangoModelFactory):
    """A factory for creating SnailMailTask objects."""

    class Meta:
        model = task.models.SnailMailTask

    category = "a"
    communication = factory.SubFactory(
        "muckrock.foia.factories.FOIACommunicationFactory"
    )


class FlaggedTaskFactory(factory.django.DjangoModelFactory):
    """A factory for creating FlaggedTask objects."""

    class Meta:
        model = task.models.FlaggedTask

    user = factory.SubFactory("muckrock.core.factories.UserFactory")
    foia = factory.SubFactory("muckrock.foia.factories.FOIARequestFactory")


class ProjectReviewTaskFactory(factory.django.DjangoModelFactory):
    """A factory for creating ProjectReviewTask objects."""

    class Meta:
        model = task.models.ProjectReviewTask

    project = factory.SubFactory("muckrock.core.factories.ProjectFactory")
    notes = factory.Faker("paragraph")


class ResponseTaskFactory(factory.django.DjangoModelFactory):
    """A factory for creating ResponseTask objects."""

    class Meta:
        model = task.models.ResponseTask

    communication = factory.SubFactory(
        "muckrock.foia.factories.FOIACommunicationFactory"
    )


class StatusChangeTaskFactory(factory.django.DjangoModelFactory):
    """A factory for creating StatusChangeTask objects."""

    class Meta:
        model = task.models.StatusChangeTask

    user = factory.SubFactory("muckrock.core.factories.UserFactory")
    old_status = "done"
    foia = factory.SubFactory("muckrock.foia.factories.FOIARequestFactory")


class NewAgencyTaskFactory(factory.django.DjangoModelFactory):
    """A factory for creating new agency tasks"""

    class Meta:
        model = task.models.NewAgencyTask

    user = factory.SubFactory("muckrock.core.factories.UserFactory")
    agency = factory.SubFactory("muckrock.core.factories.AgencyFactory")


class NewPortalTaskFactory(factory.django.DjangoModelFactory):
    """A factory for creating new portal tasks"""

    class Meta:
        model = task.models.NewPortalTask

    communication = factory.SubFactory(
        "muckrock.foia.factories.FOIACommunicationFactory"
    )
    portal_type = "other"


class ReviewAgencyTaskFactory(factory.django.DjangoModelFactory):
    """A factory for creating review agency tasks"""

    class Meta:
        model = task.models.ReviewAgencyTask

    agency = factory.SubFactory("muckrock.core.factories.AgencyFactory")


class PortalTaskFactory(factory.django.DjangoModelFactory):
    """A factory for creating review agency tasks"""

    class Meta:
        model = task.models.PortalTask

    communication = factory.SubFactory(
        "muckrock.foia.factories.FOIACommunicationFactory"
    )
    category = "u"
