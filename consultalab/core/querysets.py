from django.db import models


class AppModelCustomQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_void=False)

    def inactive(self):
        return self.filter(is_void=True)
