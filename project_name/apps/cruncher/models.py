import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class UniversalModelMixin(models.Model):
    """Universal primary key mixin

    This mixin changes the primary key of a model to UUID field.
    Using UUID as primary key could help application scalability
    and could make migrating to micro-service, or exporting or importing data easier,
    by using a universally unique identifier for object that without fear of collision.
    """

    id = models.UUIDField(
        verbose_name=_("universal unique id"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text=_("Universally unique object identifier"),
    )

    class Meta:
        abstract = True


class TimestampedModelMixin(models.Model):
    """Timestamp mixin

    This mixin adds a timestamp to model for create and update events
    """

    created = models.DateTimeField(
        _("created at"),
        auto_now_add=True,
        help_text=_("This is the timestamp of the object creation."),
    )
    updated = models.DateTimeField(
        _("updated at"),
        auto_now=True,
        help_text=_("This is the timestamp of the object update"),
    )

    class Meta:
        ordering = ["-created"]
        abstract = True
