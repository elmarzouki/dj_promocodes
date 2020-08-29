from django.contrib import admin
from dj_promocodes.promocodes.models import Promocode


@admin.register(Promocode)
class PromocodeAdmin(admin.ModelAdmin):
    list_per_page = 50

    def get_fields(self, request, obj):
        pass