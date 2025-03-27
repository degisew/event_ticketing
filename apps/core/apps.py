import json
from django.apps import AppConfig
from django.conf import settings


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core"

    policies = {}

    def ready(self):
        """Preload policies when the Django core app starts."""
        policy_file_path = getattr(settings, "POLICIES_FILE_PATH", None)
        if policy_file_path:
            try:
                with open(policy_file_path, "r") as f:
                    CoreConfig.policies = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError) as e:
                raise Exception(f"Error loading policies file: {e}")
