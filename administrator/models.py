from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _
from django.contrib.auth.models import User


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

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     img = PIL.Image.open(self.image)
    #     arr = io.BytesIO()
    #     img.save(arr, format='PNG')
    #     out = remove(arr.getvalue())
    #     with io.BytesIO(out) as f:
    #         img.save(f, format='PNG')
    #     FCMManager.sendpush("Category", "{}".format(self.pk))


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
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
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
