"""
App config for foia
"""

# Django
from django.apps import AppConfig


class FOIAConfig(AppConfig):
    """Configures the foia application to use activity streams"""

    name = "muckrock.foia"

    def ready(self):
        """Registers requests and communications with the activity streams plugin"""
        # pylint: disable=invalid-name, import-outside-toplevel
        from actstream import registry as action

        from watson import search
        import django.utils.html
        import re
        import muckrock.foia.signals  # pylint: disable=unused-import,unused-variable

        FOIARequest = self.get_model("FOIARequest")
        FOIACommunication = self.get_model("FOIACommunication")
        FOIANote = self.get_model("FOIANote")
        action.register(FOIARequest)
        action.register(FOIACommunication)
        action.register(FOIANote)
        search.register(FOIARequest.objects.get_public())
        # monkey patch the word_split regex so urlize works better
        django.utils.html.word_split_re = re.compile(r'([\s<>\(\)\[\]"\']+)')
