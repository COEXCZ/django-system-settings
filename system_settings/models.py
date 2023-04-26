from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.utils.translation import gettext_lazy as _


class SystemSettings(models.Model):

    name = models.CharField(
        max_length=256,
        db_index=True,
        unique=True,
        verbose_name=_('general-core-system_settings-name-label')
    )
    options = models.JSONField(
        default=dict,
        encoder=DjangoJSONEncoder,
        verbose_name=_('general-core-system_settings-options-label')
    )

    class Meta:
        verbose_name = _('general-core-system_settings-singular')
        verbose_name_plural = _('general-core-system_settings-plural')

    def __str__(self):
        return self.name
