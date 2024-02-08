from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules
from django.core.management import call_command
from django.utils import timezone

class PopulatedbConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'populateDB'
    def ready(self):
        from . import signals
        # Importing tasks here to ensure they are registered
        #autodiscover_modules('tasks')
        # Start the background task scheduler
        #from background_task.models import Task
        #Task.objects.filter(run_at__lte=timezone.now()).delete()  # Clear any pending tasks
        #call_command('process_tasks')

