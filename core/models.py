from datetime import datetime

from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    """
    Base abstract Model for all other models to inherit, includes created_at field.
    """

    created_at = models.DateTimeField(_('Created at'), default=datetime.now)

    class Meta:
        abstract = True


class Service(BaseModel):
    """
    Stores a single Service entry.
    """

    class StateType(models.IntegerChoices):
        WORKING = 1, 'WORKING'
        NOT_WORKING = 2, 'NOT WORKING'
        UNSTABLE = 3, 'UNSTABLE'

    name = models.CharField(_('Name'), max_length=255)
    slug_name = models.SlugField(_('Slugified name'), max_length=255)
    state = models.SmallIntegerField(_('State'), choices=StateType.choices)
    description = models.TextField(_('Description'), max_length=1000)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self._state.adding:
            self.slug_name = slugify(self.name)

        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')
        indexes = [
                   models.Index(fields=['slug_name', 'created_at']),
                   models.Index(fields=['created_at']),
                   ]

