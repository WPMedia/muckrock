"""
Models for the mailgun app
"""

# Django
from django.db import models


class WhitelistDomain(models.Model):
    """A domain to be whitelisted and always accept emails from them"""

    domain = models.CharField(max_length=255)

    def __str__(self):
        return self.domain
