import io
from os import remove

import PIL
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from api import FCMManager
from api.models import UserToken
import uuid


# Create your models here.
class Season(models.Model):
    name = models.CharField(max_length=200)
    isActive = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Season")
        verbose_name_plural = _("Seasons")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Season_detail", kwargs={"pk": self.pk})


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, default="")
    date_added = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='img/cats', blank=True, default='default.png')
    availability = models.BooleanField(default=False)
    season = models.ForeignKey(Season, blank=True, null=True, on_delete=models.CASCADE)
    ui = models.CharField(max_length=100, default="")

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categorys")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Category_detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # img = PIL.Image.open(self.image)
        # arr = io.BytesIO()
        # img.save(arr, format='PNG')
        # out = remove(arr.getvalue())
        # with io.BytesIO(out) as f:
        #     img.save(f, format='PNG')
        FCMManager.sendpush("Category", "{}".format(self.pk))


# class Item(models.Model):
#     name = models.CharField(max_length=50)
#     description = models.CharField(max_length=100, blank=True, null=True)
#     tag = models.CharField(max_length=100, default="general")
#     price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
#     date_added = models.DateTimeField(auto_now_add=True)
#     image = models.ImageField(blank=True, upload_to='img/items')
#     category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
#     availability = models.BooleanField(default=False)
#     unit = models.CharField(default="kg", max_length=20)
#
#     class Meta:
#         verbose_name = _("Item")
#         verbose_name_plural = _("Items")
#
#     def __str__(self):
#         return self.name
#
#     def get_absolute_url(self):
#         return reverse("Item_detail", kwargs={"pk": self.pk})


class Banner(models.Model):
    header = models.CharField(max_length=500)
    caption = models.CharField(max_length=500)
    image = models.ImageField(upload_to='img/banners')
    tags = models.CharField(max_length=1000, default="")
    isMain = models.BooleanField(default=False)
    buttonAlign = models.CharField(max_length=20, default='left')

    class Meta:
        verbose_name = _("Banner")
        verbose_name_plural = _("Banners")

    def __str__(self):
        return self.header

    def get_absolute_url(self):
        return reverse("Banner_detail", kwargs={"pk": self.pk})


class Csv(models.Model):
    file_name = models.FileField(upload_to="csv/")
    uploaded = models.DateTimeField(auto_now_add=True)
    is_activated = models.BooleanField(default=False)

    def __str__(self):
        return f"File id: {self.id}"


class Product(models.Model):
    number = models.IntegerField(default=0)
    stockId = models.BigIntegerField(default=0)
    serialNumber = models.BigIntegerField(default=0)
    name = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)
    cost_price = models.IntegerField(default=0.0)
    price = models.IntegerField(default=0.0)
    department = models.CharField(max_length=200)  # define department
    image = models.ImageField(upload_to="products/", default='default.png')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=0)
    availability = models.BooleanField(default=False)
    unit = models.CharField(default="kg", max_length=20)
    description = models.CharField(max_length=100, blank=True, null=True)
    tag = models.CharField(max_length=100, default="untagged")
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Product")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(f"category/{self.category.pk}", kwargs={"pk": self.pk})


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100, default="Sales")

    class Meta:
        verbose_name = _("Employee")
        verbose_name_plural = _("Employee")

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("Employee_detail", kwargs={"pk": self.pk})


ORDER_STATUS = (
    ("Placed", "Placed"),
    ("Processed", "Processed"),
    ("Delivered", "Delivered"),
    ("Completed", "Completed"),
)


class Order(models.Model):
    identification = models.ForeignKey(UserToken, on_delete=models.CASCADE)
    price = models.IntegerField(default=0.0)
    date_added = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default="Placed")
    items = models.CharField(max_length=1000, default="")
    address = models.CharField(max_length=1000, default="")
    contact = models.CharField(max_length=1000, default="")
    contactName = models.CharField(max_length=1000, default="")
    orderId = models.IntegerField(default=0)
    remoteOrderId = models.IntegerField(default=0)

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Order")

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("Order", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    class Meta:
        unique_together = ('order', 'product')


class District(models.Model):
    name = models.CharField(max_length=50)
    isActive = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("District")
        verbose_name_plural = _("District")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("District_detail", kwargs={"pk": self.pk})


class Division(models.Model):
    name = models.CharField(max_length=50)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    isActive = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Division")
        verbose_name_plural = _("Division")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Division_detail", kwargs={"pk": self.pk})


class Parish(models.Model):
    name = models.CharField(max_length=50)
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    isActive = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("parish")
        verbose_name_plural = _("parish")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("parish_detail", kwargs={"pk": self.pk})


class Village(models.Model):
    name = models.CharField(max_length=50)
    parish = models.ForeignKey(Parish, on_delete=models.CASCADE)
    isActive = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("village")
        verbose_name_plural = _("village")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("village_detail", kwargs={"pk": self.pk})


class Street(models.Model):
    name = models.CharField(max_length=50)
    village = models.ForeignKey(Village, on_delete=models.CASCADE)
    isActive = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("street")
        verbose_name_plural = _("street")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("street_detail", kwargs={"pk": self.pk})
