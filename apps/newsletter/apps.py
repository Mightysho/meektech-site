from django.apps import AppConfig

class NewsletterConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.newsletter"
    verbose_name = "Meektech Newsletter"

    def ready(self):
        import os
        import sys

        # Avoid starting the scheduler during management commands that shouldn't run background jobs
        disallowed_cmds = (
            "migrate",
            "makemigrations",
            "collectstatic",
            "shell",
            "dbshell",
            "createsuperuser",
            "test",
        )

        if any(cmd in sys.argv for cmd in disallowed_cmds):
            return

        # When using the development autoreloader `runserver`, ensure we start only in the main process
        if os.environ.get("RUN_MAIN") == "false":
            return

        try:
            from .scheduler import start
            start()
        except Exception:
            # Avoid crashing the app if scheduler fails to start; errors are logged in scheduler
            pass