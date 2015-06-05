"""
Models for the Task application
"""

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q

from datetime import datetime

import logging

from muckrock.foia.models import FOIARequest, STATUS
from muckrock.agency.models import Agency
from muckrock.jurisdiction.models import Jurisdiction

class Task(models.Model):
    """A base task model for fields common to all tasks"""
    date_created = models.DateTimeField(auto_now_add=True)
    date_done = models.DateTimeField(blank=True, null=True)
    resolved = models.BooleanField(default=False)
    assigned = models.ForeignKey(User, blank=True, null=True, related_name="assigned_tasks")
    resolved_by = models.ForeignKey(User, blank=True, null=True, related_name="resolved_tasks")

    class Meta:
        ordering = ['date_created']

    def __unicode__(self):
        return u'Task: %d' % (self.pk)

    def resolve(self, user=None):
        """Resolve the task"""
        self.resolved = True
        self.resolved_by = user
        self.date_done = datetime.now()
        self.save()

    def assign(self, user):
        """Assign the task"""
        self.assigned = user
        self.save()

class GenericTask(Task):
    """A generic task"""
    # pylint: disable=no-member
    subject = models.CharField(max_length=255)
    body = models.TextField(blank=True)

    def __unicode__(self):
        return self.subject

class OrphanTask(Task):
    """A communication that needs to be approved before showing it on the site"""
    # pylint: disable=no-member
    reasons = (('bs', 'Bad Sender'),
               ('ib', 'Incoming Blocked'),
               ('ia', 'Invalid Address'))
    reason = models.CharField(max_length=2, choices=reasons)
    communication = models.ForeignKey('foia.FOIACommunication')
    address = models.CharField(max_length=255)

    template_name = 'task/orphan.html'

    def __unicode__(self):
        return u'%s: %s' % (self.get_reason_display(), self.communication.foia)

    def move(self, foia_pks):
        """Moves the comm and creates a ResponseTask for it"""
        moved_comms = self.communication.move(foia_pks)
        for moved_comm in moved_comms:
            ResponseTask.objects.create(communication=moved_comm)
        return

    def reject(self):
        """Simply resolves the request. Should do something to spam addresses."""
        # pylint: disable=no-self-use
        return

class SnailMailTask(Task):
    """A communication that needs to be snail mailed"""
    # pylint: disable=no-member
    categories = (('a', 'Appeal'), ('n', 'New'),
                  ('u', 'Update'), ('f', 'Followup'))
    category = models.CharField(max_length=1, choices=categories)
    communication = models.ForeignKey('foia.FOIACommunication')

    def __unicode__(self):
        return u'%s: %s' % (self.get_category_display(), self.communication.foia)

    def set_status(self, status):
        """Set the status of the comm and FOIA affiliated with this task"""
        comm = self.communication
        foia = comm.foia
        foia.status = status
        foia.update()
        foia.save()
        comm.status = foia.status
        #comm.date = datetime.now()
        comm.save()

    def update_date(self):
        """Sets the date of the communication to today"""
        comm = self.communication
        comm.date = datetime.now()
        comm.save()
        comm.foia.update()

class RejectedEmailTask(Task):
    """A FOIA request has had an outgoing email rejected"""
    categories = (('b', 'Bounced'), ('d', 'Dropped'))
    category = models.CharField(max_length=1, choices=categories)
    foia = models.ForeignKey('foia.FOIARequest', blank=True, null=True)
    email = models.EmailField(blank=True)
    error = models.TextField(blank=True)

    def __unicode__(self):
        return u'%s: %s' % (self.get_category_display(), self.foia)

    def agencies(self):
        """Get the agencies who use this email address"""
        return Agency.objects.filter(Q(email__iexact=self.email) |
                                     Q(other_emails__icontains=self.email))

    def foias(self):
        """Get the FOIAs who use this email address"""
        return FOIARequest.objects\
                .filter(Q(email__iexact=self.email) |
                        Q(other_emails__icontains=self.email))\
                .filter(status__in=['ack', 'processed', 'appealing',
                                    'fix', 'payment'])


class StaleAgencyTask(Task):
    """An agency has gone stale"""
    agency = models.ForeignKey(Agency)

    def __unicode__(self):
        return u'Stale Agency: %s' % (self.agency)


class FlaggedTask(Task):
    """A user has flagged a request, agency or jurisdiction"""
    user = models.ForeignKey(User)
    text = models.TextField()
    foia = models.ForeignKey('foia.FOIARequest', blank=True, null=True)
    agency = models.ForeignKey(Agency, blank=True, null=True)
    jurisdiction = models.ForeignKey(Jurisdiction, blank=True, null=True)

    def __unicode__(self):
        if self.foia:
            return u'Flagged: %s' % (self.foia)
        if self.agency:
            return u'Flagged: %s' % (self.agency)
        if self.jurisdiction:
            return u'Flagged: %s' % (self.jurisdiction)
        return u'Flagged: <None>'


class NewAgencyTask(Task):
    """A new agency has been created and needs approval"""
    user = models.ForeignKey(User, blank=True, null=True)
    agency = models.ForeignKey(Agency)

    def __unicode__(self):
        return u'New Agency: %s' % (self.agency)

    def pending_requests(self):
        """Returns the requests to be acted on"""
        return FOIARequest.objects.filter(agency=self.agency)

    def approve(self):
        """Approves agency, resends pending requests, and resolves"""
        self.agency.approved = True
        self.agency.save()
        # resend the first comm of each foia associated to this agency
        for foia in self.pending_requests():
            comms = foia.communications.all()
            if comms.count():
                first_comm = comms[0]
                first_comm.resend(self.agency.get_email())

    def reject(self, replacement_agency):
        """Resends pending requests to replacement agency and resolves"""
        for foia in self.pending_requests():
            # first switch foia to use replacement agency
            foia.agency = replacement_agency
            foia.save()
            comms = foia.communications.all()
            if comms.count():
                first_comm = comms[0]
                first_comm.resend(replacement_agency.email)

class ResponseTask(Task):
    """A response has been received and needs its status set"""
    # pylint: disable=no-member
    communication = models.ForeignKey('foia.FOIACommunication')

    def __unicode__(self):
        return u'Response: %s' % (self.communication.foia)

    def move(self, foia_pks):
        """Moves the associated communication to a new request"""
        return self.communication.move(foia_pks)

    def set_tracking_id(self, tracking_id):
        """Sets the tracking ID of the communication's request"""
        if type(tracking_id) is not type(unicode()):
            raise ValueError('Tracking ID should be a unicode string.')
        comm = self.communication
        if not comm.foia:
            raise ValueError('The task communication is an orphan.')
        foia = comm.foia
        foia.tracking_id = tracking_id
        foia.save()

    def set_status(self, status):
        """Sets status of comm and foia"""
        comm = self.communication
        # check that status is valid
        if status not in [status_set[0] for status_set in STATUS]:
            raise ValueError('Invalid status.')
        # save comm first
        comm.status = status
        #if status in ['ack', 'processed', 'appealing']:
        #    comm.date = datetime.now()
        comm.save()
        # save foia next
        foia = comm.foia
        foia.status = status
        if status in ['rejected', 'no_docs', 'done', 'abandoned']:
            foia.date_done = comm.date
        foia.update()
        foia.save()
        logging.info('Request #%d status changed to "%s"', foia.id, status)

class FailedFaxTask(Task):
    """A fax for this communication failed"""
    # pylint: disable=no-member
    communication = models.ForeignKey('foia.FOIACommunication')

    def __unicode__(self):
        return u'Failed Fax: %s' % (self.communication.foia)

class StatusChangeTask(Task):
    """A user has the status on a request"""

    user = models.ForeignKey(User)
    old_status = models.CharField(max_length=255)
    foia = models.ForeignKey('foia.FOIARequest')

    def __unicode__(self):
        return u'StatusChange: %s' % self.foia

class PaymentTask(Task):
    """Created when the fee for a request has been paid"""
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    user = models.ForeignKey(User)
    foia = models.ForeignKey('foia.FOIARequest')

    def __unicode__(self):
        return u'Payment: %s for %s' % (self.amount, self.foia)

class CrowdfundTask(Task):
    """Created when a crowdfund is finished"""
    crowdfund = models.ForeignKey('crowdfund.CrowdfundRequest')

    def __unicode__(self):
        return u'Crowdfund: %s' % self.crowdfund

class MultiRequestTask(Task):
    """Created when a multirequest is created and needs approval."""
    multirequest = models.ForeignKey('foia.FOIAMultiRequest')

    def __unicode__(self):
        return u'Multi-Request: %s' % self.multirequest
