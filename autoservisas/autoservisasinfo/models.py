from django.contrib.auth import get_user_model
from datetime import date
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.db.models import Sum
from django.utils.html import format_html
from PIL import Image
from tinymce.models import HTMLField

User = get_user_model()

class AutomobilioModelis(models.Model):
    car = models.CharField(_("car"), max_length=100)
    car_model = models.CharField(_("model"), max_length=100)
    car_description = HTMLField(_("Description"),  max_length=8000, blank=True, null=True)
    
    class Meta:
        verbose_name = _("automobilio Modelis")
        verbose_name_plural = _("automobiliu modeliai")
    
    car_image = models.ImageField(
        _("car_image"),
        upload_to='autoservisas/cars_images',
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'{self.car} - {self.car_model}'

    def get_absolute_url(self):
        return reverse("automobilioModelis_detail", kwargs={"pk": self.pk})


class Automobilis(models.Model):
    car_number = models.CharField(_("car_number"), max_length=10, blank=False, default=None)
    vin_number = models.CharField(_("vin_number"), max_length=17, blank=False, default=None)
    car_model = models.ForeignKey(
        AutomobilioModelis,
        verbose_name=_("automobilio modelis"),
        on_delete=models.CASCADE,
        related_name='automobiliai',
        )
    
    user = models.ForeignKey(
        User, 
        verbose_name=_("user"), 
        on_delete=models.CASCADE,
        related_name='automobilis',
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ['user']
        verbose_name = _("automobilis")
        verbose_name_plural = _("klientu automobiliai")

    def __str__(self):
        return f'{self.car_model}'

    def get_absolute_url(self):
        return reverse("automobilis_detail", kwargs={"pk": self.pk})  
    

class Paslauga(models.Model):
    name = models.CharField(_("name"), max_length=50)
    price = models.FloatField(_("price"))
    
    class Meta:
        verbose_name = _("paslauga")
        verbose_name_plural = _("paslaugos")

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse("paslauga_detail", kwargs={"pk": self.pk})


class Uzsakymas(models.Model):
    order_date = models.DateField(_("order_date"), auto_now=False, auto_now_add=False)
    price = models.FloatField(_("price"), default=0)
    car = models.ForeignKey(
        Automobilis,
        verbose_name=_("automobilis"),
        on_delete=models.CASCADE,
        related_name='uzsakymai',
        )
    
    class Meta:
        verbose_name = _("uzsakymas")
        verbose_name_plural = _("uzsakymai")
    
    STATUS_CHOICES = (
        (0, _('Confirmed')),
        (1, _('In Progress')),
        (2, _('Finished')),
        (3, _('Canceled')),
    )

    status = models.PositiveSmallIntegerField(
        _("status"),
        choices=STATUS_CHOICES, 
        default=0,
        db_index=True
    )

    @property
    def is_overdue(self):
        if self.order_date and date.today() > self.order_date:
            return True
        return False
    
    @property
    def user(self):
        return self.car.user

    def __str__(self):
        return f'Data: {self.order_date}. Kliento info: {self.car.user} {self.car} {self.get_status_display()}'

    def get_absolute_url(self):
        return reverse("uzsakymas_detail", kwargs={"pk": self.pk})
    

class UzsakymoEilute(models.Model):
    paslauga = models.ForeignKey(
        Paslauga,
        verbose_name=_("paslaugos"),
        on_delete=models.CASCADE,
        related_name='uzsakymoEilutes'
        )
    uzsakymas = models.ForeignKey(
        Uzsakymas,
        verbose_name=_("uzsakymai"),
        on_delete=models.CASCADE,
        related_name='uzsakymoEilutes'
        )
    count = models.IntegerField(_("count"))
    total_price = models.FloatField(_("total_price"), default=0)

    class Meta:
        verbose_name = _("uzsakymo Eilute")
        verbose_name_plural = _("uzsakymo Eilutes")

    new_line = '\n'

    def save(self, *args, **kwargs):
        if self.total_price == 0:
            self.price = self.paslauga.price if self.paslauga.price is not None else 0
            self.count = self.count if self.count is not None else 0
            self.total_price = self.price * self.count
        user = get_user_model().objects.get(pk=self.uzsakymas.user.pk)
        self.user = user
        
        super().save(*args, **kwargs)
    
    @staticmethod
    def calculate_total_price(orders):
        total_price = sum(order.total_price for order in orders)
        return total_price

    def __str__(self):
        return f'Paslauga: {self.paslauga}. Paslaugų kiekis: {self.count}. {self.new_line} Užsakymas: {self.uzsakymas} {self.new_line} Bendra kaina: {self.total_price}'

    def get_absolute_url(self):
        return reverse("uzsakymoEilute_detail", kwargs={"pk": self.pk})


class OrderComment(models.Model):
    order = models.ForeignKey(
        Uzsakymas,
        verbose_name=_("order"),
        on_delete=models.CASCADE,
        related_name='comments',
        )
    
    commentator = models.ForeignKey(
        User,
        verbose_name=_("commentator"),
        on_delete=models.SET_NULL,
        related_name='order_comments',
        null=True,
        blank=True,
        )
    
    commented_at = models.DateTimeField(_("Commented"), auto_now_add=True)
    content = models.TextField(_("content"), max_length=4000)

    class Meta:
        ordering = ["-commented_at"]
        verbose_name = _("order comment")
        verbose_name_plural = _("order comments")

    def __str__(self):
        return f"{self.commented_at}: {self.commentator}"

    def get_absolute_url(self):
        return reverse("ordercomment_detail", kwargs={"pk": self.pk})

