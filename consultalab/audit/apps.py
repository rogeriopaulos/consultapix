from django.apps import AppConfig


class AuditConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "consultalab.audit"
    verbose_name = "Admin & Auditoria"
