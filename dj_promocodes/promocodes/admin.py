from django.contrib import admin
from django.contrib.sites.models import Site
from django.contrib.auth.models import Group
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialToken, SocialAccount, SocialApp
from dj_promocodes.promocodes.models import Promocode, Balance


@admin.register(Promocode)
class PromocodeAdmin(admin.ModelAdmin):
    list_per_page = 50


@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    list_per_page = 50


admin.site.unregister(Site)
admin.site.unregister(Group)
admin.site.unregister(EmailAddress)
admin.site.unregister(SocialToken)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialApp)