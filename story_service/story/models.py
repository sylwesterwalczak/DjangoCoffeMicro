from django.db import models
from django.utils.translation import ugettext_lazy as _


class Ingredient(models.Model):
    UNIT_CHOICE = (
        (1,  _('ml')),
        (2, _('g')),
    )
    name = models.CharField(max_length=50, null=False, blank=False)
    sku_nubmer = models.CharField(max_length=50, null=False, blank=False)
    quantity = models.PositiveIntegerField(default=0)

    supplier = models.PositiveSmallIntegerField(
        null=True,
        blank=True
    )
    unit = models.PositiveSmallIntegerField(
        choices=UNIT_CHOICE,
        default=1,
    )

    @property
    def label(self):
        return f'{self.name} - {self.quantity} {self.get_unit_display()}'

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.label
