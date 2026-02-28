from django.contrib.auth.apps import AuthConfig as DjangoAuthConfig


class AuthConfig(DjangoAuthConfig):
    """Project-level AppConfig to customize the Django auth app display name.

    This overrides the default verbose_name ("Authentication and Authorization")
    so templates and admin UI show the shorter "Auth and Authorization" text.
    """

    verbose_name = "Auth and Authorization"
