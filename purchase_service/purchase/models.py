import os
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField

from .producer import publish

User = get_user_model()


class PurchaseOrder(models.Model):
    STATUS_CHOICE = (
        (1, _("New")),  # Nowe
        (2, _("Pending")),  # W przygotowaniu
        (3, _("Ready")),  # Gotowe
        (4, _("Retrieved")),  # Odebrane
        (5, _("Canceled")),  # Anulowane
    )
    items = ArrayField(models.IntegerField(), null=True, blank=True)
    status = models.PositiveIntegerField(
        choices=STATUS_CHOICE,
        default=1
    )
    order_number = models.CharField(max_length=50)
    client_name = models.CharField(max_length=50, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    created_by = models.PositiveSmallIntegerField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.order_number} - {self.get_status_display()}"


def post_save_message(sender, instance, created, **kwargs):
    message_queue = os.environ.get('MESSAGE_QUEUE')

    publish(
        'created',
        {
            "order_number": instance.order_number,
            "message": "Nowy status: %s" % instance.get_status_display()
        },
        message_queue
    )


post_save.connect(post_save_message, sender=PurchaseOrder)
