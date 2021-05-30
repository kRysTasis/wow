from django.db import models
from django.utils.translation import ugettext_lazy as _

class TimeStampModel(models.Model):


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    enable = models.BooleanField(default=True)
    deleted = models.BooleanField(
        _('Delete Flag'),
        default=False,
        help_text=_(
            'Designates whether the column was deleted or not'
        )
    )

    class Meta:
        abstract = True
