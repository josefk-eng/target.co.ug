from django.contrib import admin
from . import models


class RatingAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

# Register your models here.
# Register your models here.
admin.site.register(models.Category)
admin.site.register(models.Season)
admin.site.register(models.Banner)
admin.site.register(models.Csv)
admin.site.register(models.Product,RatingAdmin)
admin.site.register(models.Employee)
admin.site.register(models.Order)
admin.site.register(models.OrderProduct)
admin.site.register(models.District)
admin.site.register(models.Division)
admin.site.register(models.Parish)
admin.site.register(models.Village)
admin.site.register(models.Street)
