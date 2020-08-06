"""
URL mappings for the Task application
"""

# Django
from django.conf.urls import url
from django.views.generic.base import RedirectView

# MuckRock
from muckrock.task import views

urlpatterns = [
    url(r"^$", RedirectView.as_view(url="/task/response/"), name="task-list"),
    url(r"^orphan/$", views.OrphanTaskList.as_view(), name="orphan-task-list"),
    url(r"^orphan/(?P<pk>\d+)/$", views.OrphanTaskList.as_view(), name="orphan-task"),
    url(
        r"^snail-mail/$", views.SnailMailTaskList.as_view(), name="snail-mail-task-list"
    ),
    url(
        r"^snail-mail/(?P<pk>\d+)/$",
        views.SnailMailTaskList.as_view(),
        name="snail-mail-task",
    ),
    url(
        r"^review-agency/$",
        views.ReviewAgencyTaskList.as_view(),
        name="review-agency-task-list",
    ),
    url(
        r"^review-agency/(?P<pk>\d+)/$",
        views.ReviewAgencyTaskList.as_view(),
        name="review-agency-task",
    ),
    url(r"^portal/$", views.PortalTaskList.as_view(), name="portal-task-list"),
    url(r"^portal/(?P<pk>\d+)/$", views.PortalTaskList.as_view(), name="portal-task"),
    url(
        r"^new-portal/$", views.NewPortalTaskList.as_view(), name="new-portal-task-list"
    ),
    url(
        r"^new-portal/(?P<pk>\d+)/$",
        views.NewPortalTaskList.as_view(),
        name="new-portal-task",
    ),
    url(r"^flagged/$", views.FlaggedTaskList.as_view(), name="flagged-task-list"),
    url(
        r"^flagged/(?P<pk>\d+)/$", views.FlaggedTaskList.as_view(), name="flagged-task"
    ),
    url(
        r"^new-agency/$", views.NewAgencyTaskList.as_view(), name="new-agency-task-list"
    ),
    url(
        r"^new-agency/(?P<pk>\d+)/$",
        views.NewAgencyTaskList.as_view(),
        name="new-agency-task",
    ),
    url(r"^response/$", views.ResponseTaskList.as_view(), name="response-task-list"),
    url(
        r"^response/(?P<pk>\d+)/$",
        views.ResponseTaskList.as_view(),
        name="response-task",
    ),
    url(
        r"^status-change/$",
        views.StatusChangeTaskList.as_view(),
        name="status-change-task-list",
    ),
    url(
        r"^status-change/(?P<pk>\d+)/$",
        views.StatusChangeTaskList.as_view(),
        name="status-change-task",
    ),
    url(r"^crowdfund/$", views.CrowdfundTaskList.as_view(), name="crowdfund-task-list"),
    url(
        r"^crowdfund/(?P<pk>\d+)/$",
        views.CrowdfundTaskList.as_view(),
        name="crowdfund-task",
    ),
    url(
        r"^multirequest/$",
        views.MultiRequestTaskList.as_view(),
        name="multirequest-task-list",
    ),
    url(
        r"^multirequest/(?P<pk>\d+)/$",
        views.MultiRequestTaskList.as_view(),
        name="multirequest-task",
    ),
    url(
        r"^project-review/$",
        views.ProjectReviewTaskList.as_view(),
        name="projectreview-task-list",
    ),
    url(
        r"^project-review/(?P<pk>\d+)/$",
        views.ProjectReviewTaskList.as_view(),
        name="projectreview-task",
    ),
    url(
        r"^payment-info/$",
        views.PaymentInfoTaskList.as_view(),
        name="payment-info-task-list",
    ),
    url(
        r"^payment-info/(?P<pk>\d+)/$",
        views.PaymentInfoTaskList.as_view(),
        name="payment-info-task",
    ),
    # tasks for a specific request
    url(
        r"^request/(?P<pk>\d+)/$",
        views.RequestTaskList.as_view(),
        name="request-task-list",
    ),
    url(r"^snail-mail/pdf/$", views.snail_mail_bulk_pdf, name="snail-mail-bulk-pdf",),
    url(r"^snail-mail/pdf/(?P<pk>\d+)/$", views.snail_mail_pdf, name="snail-mail-pdf",),
    url(
        r"^review-agency-ajax/(?P<pk>\d+)/$",
        views.review_agency_ajax,
        name="review-agency-ajax",
    ),
    url(r"^assign-to/$", views.assign_to, name="task-assign",),
    url(
        r"^bulk-new-agency/$",
        views.BulkNewAgency.as_view(),
        name="task-bulk-new-agency",
    ),
]
