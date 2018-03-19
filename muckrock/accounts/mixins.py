"""
View mixins
"""

# Django
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

# Standard Library
from datetime import date

# MuckRock
from muckrock.accounts.models import Profile
from muckrock.accounts.utils import mailchimp_subscribe, unique_username
from muckrock.message.tasks import welcome_miniregister
from muckrock.utils import generate_key


def split_name(name):
    """Splits a full name into a first and last name."""
    # infer first and last names from the full name
    # limit first and last names to 30 characters each
    if ' ' in name:
        first_name, last_name = name.rsplit(' ', 1)
        first_name = first_name[:30]
        last_name = last_name[:30]
    else:
        first_name = name[:30]
        last_name = ''
    return first_name, last_name


class MiniregMixin(object):
    """A mixin to expose miniregister functionality to a view"""

    def miniregister(self, full_name, email, newsletter=False):
        """Create a new user from their full name and email and login"""
        password = generate_key(12)
        full_name = full_name.strip()
        username = unique_username(full_name)
        first_name, last_name = split_name(full_name)
        # create a new User
        user = User.objects.create_user(
            username,
            email,
            password,
            first_name=first_name,
            last_name=last_name
        )
        # create a new Profile
        Profile.objects.create(
            user=user,
            acct_type='basic',
            monthly_requests=settings.MONTHLY_REQUESTS.get('basic', 0),
            date_update=date.today()
        )
        # send the new user a welcome email
        welcome_miniregister.delay(user)
        user = authenticate(
            username=user.username,
            password=password,
        )
        login(self.request, user)
        if newsletter:
            mailchimp_subscribe(self.request, user.email)
        return user
