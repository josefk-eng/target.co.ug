from django.contrib import admin
from .models import UserToken


# class RatingAdmin(admin.ModelAdmin):
#     readonly_fields = ('id',)


# Register your models here.
admin.site.register(UserToken)
