"""
App config for projects
"""

# Django
from django.apps import AppConfig


class ProjectConfig(AppConfig):
    """Configures the project application to use activity streams"""

    name = "muckrock.project"

    def ready(self):
        """Registers the application with the activity streams plugin"""
        # pylint: disable=invalid-name, import-outside-toplevel
        from actstream import registry as action
        from watson import search

        Project = self.get_model("Project")
        action.register(Project)
        search.register(Project.objects.get_public())
