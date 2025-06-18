from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.db.models import EmailField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractUser):
    """
    Default custom user model for ConsultaLab.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]
    email = EmailField(_("email address"), unique=True)
    username = None  # type: ignore[assignment]

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})

    class Meta(AbstractUser.Meta):
        permissions = (
            (
                "access_admin_section",
                "Pode acessar a seção de Administração & Auditoria",
            ),
            ("can_request_pix", "Pode realizar consultas de PIX"),
            ("can_request_ccs", "Pode realizar consultas de CCS"),
        )

    def get_user_permissions(self):
        perm_map = {
            "users.access_admin_section": {
                "text": "admin",
                "badge_class": "primary",
            },
            "users.can_request_pix": {
                "text": "pix",
                "badge_class": "success",
            },
            "users.can_request_ccs": {
                "text": "ccs",
                "badge_class": "info",
            },
        }
        return [
            {"text": label["text"], "badge_class": label["badge_class"]}
            for perm, label in perm_map.items()
            if self.has_perm(perm)
        ]
