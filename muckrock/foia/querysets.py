"""
QuerySets for the FOIA application
"""

# Django
from django.contrib.auth.models import AnonymousUser
from django.db import models
from django.db.models import Count, F, Max, OuterRef, Q, Subquery, Sum
from django.utils import timezone
from django.utils.text import slugify

# Standard Library
from datetime import date, datetime, time
from itertools import groupby

# MuckRock
from muckrock.agency.constants import STALE_REPLIES


class PreloadFileQuerysetMixin:
    """Mixin for preloading related files"""

    files_path = "files"
    comm_id = "id"

    def __init__(self, *args, **kwargs):
        super(PreloadFileQuerysetMixin, self).__init__(*args, **kwargs)
        self._preload_files_amt = 0
        self._preload_files_done = False

    def _clone(self):
        """Add _preload_files_amt to vlaues to copy over in a clone"""
        # pylint: disable=protected-access
        clone = super(PreloadFileQuerysetMixin, self)._clone()
        clone._preload_files_amt = self._preload_files_amt
        return clone

    def preload_files(self, limit=11):
        """Preload up to limit files for the communications
        Mark as needing to be preloaded - actually preloading will be done lazily
        """
        # pylint: disable=protected-access
        self._preload_files_amt = limit
        return self

    def _do_preload_files(self):
        """Do the preloading of the files lazily"""
        # pylint: disable=import-outside-toplevel
        from muckrock.foia.models.file import FOIAFile

        comm_ids = [getattr(i, self.comm_id) for i in self._result_cache]
        if comm_ids:
            files = FOIAFile.objects.preload(comm_ids, self._preload_files_amt)
            for obj in self._result_cache:
                self._process_preloaded_files(obj, files)
        self._preload_files_done = True

    def _process_preloaded_files(self, obj, files):
        """What to do with the preloaded files for each record"""
        obj.display_files = files.get(obj.pk, [])

    def _fetch_all(self):
        """Override fetch all to lazily preload files if needed"""
        super(PreloadFileQuerysetMixin, self)._fetch_all()
        if self._preload_files_amt > 0 and not self._preload_files_done:
            self._do_preload_files()


class FOIARequestQuerySet(models.QuerySet):
    """Object manager for FOIA requests"""

    # pylint: disable=too-many-public-methods

    def get_done(self):
        """Get all FOIA requests with responses"""
        return self.filter(status__in=["partial", "done"]).exclude(datetime_done=None)

    def get_viewable(self, user):
        """Get all viewable FOIA requests for given user"""

        if user.is_staff:
            return self.all()

        if user.is_authenticated:
            # Requests are visible if you own them, have view or edit permissions,
            # or if they are not embargoed
            query = (
                Q(composer__user=user)
                | Q(pk__in=user.edit_access.all())
                | Q(pk__in=user.read_access.all())
                | ~Q(embargo=True)
            )
            # agency users may also view requests for their agency
            if user.profile.is_agency_user:
                query = query | Q(agency=user.profile.agency)
            # organizational users may also view requests from their org that are shared
            query = query | Q(
                composer__user__profile__org_share=True,
                composer__organization__in=user.organizations.all(),
            )
            return self.filter(query)
        else:
            # anonymous user, filter out embargoes
            return self.exclude(embargo=True)

    def get_public(self):
        """Get all publically viewable FOIA requests"""
        return self.get_viewable(AnonymousUser())

    def get_overdue(self):
        """Get all overdue FOIA requests"""
        return self.filter(status__in=["ack", "processed"], date_due__lt=date.today())

    def get_followup(self):
        """Get requests that need follow up emails sent"""
        return (
            self.filter(
                status__in=["ack", "processed"],
                date_followup__lte=date.today(),
                disable_autofollowups=False,
            )
            # Exclude requests which should be emailed or faxed,
            # but need to have their email address or fax number updated.
            # This is to not overwhelm snail mail tasks with autogenerated
            # messages while trying to find new contact info
            .exclude(
                Q(email__status="error", fax=None)
                | Q(email=None, fax__status="error")
                | Q(email__status="error", fax__status="error")
            )
        )

    def get_open(self):
        """Get requests which we are awaiting a response from"""
        return self.filter(status__in=["ack", "processed", "appealing"])

    def organization(self, organization):
        """Get requests belonging to an organization's members."""
        return (
            self.select_related("agency__jurisdiction__parent__parent")
            .filter(composer__organization=organization)
            .order_by("-composer__datetime_submitted")
        )

    def select_related_view(self):
        """Select related models for viewing"""
        return self.select_related(
            "agency__jurisdiction__parent__parent", "composer__user", "crowdfund"
        )

    def get_public_file_count(self, limit=None):
        """Annotate the public file count"""
        if limit is not None:
            foias = list(self[:limit])
        else:
            foias = list(self)

        count_qs = (
            self.model.objects.filter(
                id__in=[f.pk for f in foias], communications__files__access="public"
            )
            .values_list("id")
            .annotate(Count("communications__files"))
        )

        counts = dict(count_qs)

        for foia in foias:
            foia.public_file_count = counts.get(foia.pk, 0)
        return foias

    def get_featured(self, user):
        """Get featured requests"""
        return (
            self.get_viewable(user)
            .filter(featured=True)
            .select_related_view()
            .get_public_file_count()
        )

    def get_processing_days(self):
        """Get the number of processing days"""
        return (
            self.filter(status="submitted")
            .exclude(date_processing=None)
            .aggregate(days=Sum(date.today() - F("date_processing")))["days"]
        )

    def get_submitted_range(self, start, end):
        """Get requests submitted within a date range"""
        return self.filter(composer__datetime_submitted__range=(start, end))

    def get_today(self):
        """Get requests submitted today"""
        midnight = time(tzinfo=timezone.get_current_timezone())
        today_midnight = datetime.combine(date.today(), midnight)
        return self.filter(composer__datetime_submitted__gte=today_midnight)

    def exclude_org_users(self):
        """Exclude requests made by org users"""
        return self.filter(composer__organization__individual=True)

    def create_new(self, composer, agency):
        """Create a new request and submit it"""
        if composer.agencies.count() > 1:
            title = "%s (%s)" % (composer.title, agency.name)
        else:
            title = composer.title
        if agency.jurisdiction.days:
            calendar = agency.jurisdiction.get_calendar()
            date_due = calendar.business_days_from(
                date.today(), agency.jurisdiction.days
            )
        else:
            date_due = None
        proxy_info = agency.get_proxy_info()
        foia = self.create(
            status="submitted",
            title=title,
            slug=slugify(title),
            agency=agency,
            embargo=composer.embargo,
            permanent_embargo=composer.permanent_embargo,
            composer=composer,
            date_due=date_due,
            missing_proxy=proxy_info["missing_proxy"],
        )
        foia.tags.set(*composer.tags.all())
        foia.create_initial_communication(
            proxy_info.get("from_user", composer.user), proxy=proxy_info["proxy"]
        )
        foia.process_attachments(composer.user, composer=True)

    def get_stale(self):
        """Get stale requests"""
        # pylint: disable=import-outside-toplevel
        from muckrock.foia.models import FOIACommunication

        with_response = (
            self.filter(
                communications__response=False,
                communications__datetime__gt=Subquery(
                    FOIACommunication.objects.filter(foia=OuterRef("pk"), response=True)
                    .order_by()
                    .values("foia")
                    .annotate(max=Max("datetime"))
                    .values("max")
                ),
            )
            .annotate(count=Count("communications"))
            .filter(count__gt=STALE_REPLIES, status__in=["processed", "appealing"])
        )
        without_response = self.annotate(count=Count("communications")).filter(
            status="ack", count__gt=STALE_REPLIES
        )
        return with_response.union(without_response)


class FOIAComposerQuerySet(models.QuerySet):
    """Custom Query Set for FOIA Composers"""

    def get_viewable(self, user):
        """Return all composers viewable to the user"""
        if user.is_staff:
            return self.all()

        if user.is_authenticated:
            # you can view if
            # * you are the owner
            # * you are a read or edit collaborator on at least one foia
            # * the request is public
            #   * not a draft
            #   * at leats one foia request is not embargoed
            query = (
                Q(user=user)
                | Q(foias__read_collaborators=user)
                | Q(foias__edit_collaborators=user)
                | (~Q(status="started") & Q(foias__embargo=False))
            )
            # organizational users may also view requests from their org
            # that are shared
            query = query | Q(user__profile__org_share=True, organization__users=user)
            return self.filter(query)
        else:
            # anonymous user, filter out drafts and embargoes
            return self.exclude(status="started").filter(foias__embargo=False)

    def get_or_create_draft(self, user, organization):
        """Return an existing blank draft or create one"""
        draft = self.filter(
            user=user,
            organization=organization,
            title="Untitled",
            slug="untitled",
            status="started",
            agencies=None,
            requested_docs="",
            edited_boilerplate=False,
            datetime_submitted=None,
            embargo=False,
            permanent_embargo=False,
            parent=None,
            tags=None,
            num_monthly_requests=0,
            num_reg_requests=0,
        ).first()
        if draft:
            draft.datetime_created = timezone.now()
            draft.save()
            return draft
        else:
            return self.create(user=user, organization=organization)


class FOIACommunicationQuerySet(PreloadFileQuerysetMixin, models.QuerySet):
    """Object manager for FOIA Communications"""

    prefetch_fields = ("emails", "faxes", "mails", "web_comms", "portals")

    def visible(self):
        """Hide hidden communications"""
        return self.filter(hidden=False)

    def preload_list(self):
        """Preload the relations required for displaying a list of communications"""
        return self.prefetch_related(*self.prefetch_fields).preload_files()

    def get_viewable(self, user):
        """Get all viewable FOIA communications for given user"""
        # This is only used for filtering API view

        if user.is_staff:
            return self.all()

        if user.is_authenticated:
            # Requests are visible if you own them, have view or edit permissions,
            # or if they are not embargoed
            query = (
                Q(foia__composer__user=user)
                | Q(foia__in=user.edit_access.all())
                | Q(foia__in=user.read_access.all())
                | Q(foia__embargo=False)
            )
            # organizational users may also view requests from their org that are shared
            query = query | Q(
                foia__composer__user__profile__org_share=True,
                foia__composer__organization__in=user.organizations.all(),
            )
            return self.filter(query)
        else:
            # anonymous user, filter out embargoes
            return self.filter(foia__embargo=False)


class FOIAFileQuerySet(models.QuerySet):
    """Custom Queryset for FOIA Files"""

    def preload(self, comm_ids, limit=11):
        """Preload the top limit files for the communications in comm_ids"""
        file_qs = self.raw(
            """
            SELECT rank_filter.* FROM (
                SELECT foia_foiafile.*, ROW_NUMBER() OVER (
                    PARTITION BY comm_id ORDER BY foia_foiafile.datetime DESC
                ) FROM foia_foiafile
                WHERE comm_id IN %s
            ) rank_filter WHERE ROW_NUMBER <= %s
            """,
            [tuple(comm_ids), limit],
        )
        return {
            comm_id: list(files)
            for comm_id, files in groupby(file_qs, lambda f: f.comm_id)
        }
