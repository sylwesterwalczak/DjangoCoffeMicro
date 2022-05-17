from django.db import models


class Component(models.Model):

    ingredient = models.PositiveSmallIntegerField(
        null=True,
        blank=True
    )
    quantity = models.IntegerField(default=1)
    name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f'{self.name} - {self.quantity}'


class MenuItem(models.Model):

    name = models.CharField(max_length=50, null=False, blank=False)
    price_net = models.DecimalField(max_digits=6, decimal_places=2)
    ingredients = models.ManyToManyField(
        Component,
        blank=True,
        related_name='component'
    )
    tax = models.DecimalField(max_digits=4, decimal_places=2, default=23)

    @property
    def price_gros(self):
        return "{:.2f}".format(self.price_net * self.tax/100 + self.price_net)

    def __str__(self):
        return f"{self.name} {self.price_gros} PLN"


class Menu(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    items = models.ManyToManyField(MenuItem)
