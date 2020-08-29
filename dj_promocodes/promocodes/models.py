from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from model_utils.models import SoftDeletableModel, TimeStampedModel


User = get_user_model()  # django auth.user
BOOL_CHOICES = [(True, "Yes"), (False, "No")]  # for dashboard readability


class TitleField(models.SlugField):
    """Custom Title field to lowercase the passed title value"""

    def __init__(self, *args, **kwargs):
        super(TitleField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        return str(value).lower()


# class PromocodesManager(models.Manager):
#     now = timezone.localtime(timezone.now())

#     def get_queryset(self):
#         return (
#             super(PromocodesManager, self)
#             .get_queryset()
#             .filter(
#                 is_active=True,
#                 start_date__lte=now,
#                 end_date__gte=now,
#             )
#         )


class Promocodes(SoftDeletableModel, TimeStampedModel):
    # custom manager to get valid promocodes
    # objects = PromocodesManager()

    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(blank=False, null=False)
    quantity = models.PositiveIntegerField(default=100)
    code = TitleField(
        max_length=20,
        unique=True,
        help_text="Unique title to identify this promocode (No spaces allowed. Lowercase letters)",
    )
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)
    frequency_of_use = models.PositiveIntegerField(default=100)
    is_active = models.BooleanField(default=True, choices=BOOL_CHOICES)

    class Meta:
        verbose_name = _("Promocode")
        verbose_name_plural = _("Promocodes")

    def __str__(self):
        return self.code

    # relations over JSONField
    @property
    def benefits(self):
        return self.balance_set.values_list("value", flat=True)


class Balance(TimeStampedModel):
    promocode = models.ForeignKey(
        Promocodes,
        on_delete=models.PROTECT,
    )
    value = models.IntegerField()


class Transaction(TimeStampedModel):
    STATUS_CHOICES = [
        ("SUCCESSFUL", "Successful"),
        ("FAILED", "Failed"),
        ("REFUNDED", "Refunded"),
        ("VOIDED", "Voided"),
        ("PENDING", "Pending"),
    ]
    PAY_USING_CHOICES = [
        ("CASH", "Cash"),
        ("CARD", "Card"),
    ]
    PAY_FOR_CHOICES = [
        ("BILL", "Bill"),
        ("SERVICE", "Service"),
    ]
    uuid = models.CharField(max_length=100, editable=False, null=True, unique=False)
    payment_for = models.CharField(
        max_length=40, choices=PAY_FOR_CHOICES, default="BILL"
    )
    pay_using = models.CharField(
        max_length=7, choices=PAY_USING_CHOICES, default="CARD"
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="PENDING")
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        related_name="transactions",
    )
    promocode = models.ForeignKey(
        Promocodes,
        on_delete=models.SET_NULL,
        related_name="transactions",
        null=True,
        blank=True,
    )
    # TODO:// add transaction amount

    def __str__(self):
        return self.uuid

    class Meta:
        ordering = ["-modified"]
        verbose_name = _("Transaction")
        verbose_name_plural = _("Transactions")


class Invoice(TimeStampedModel, SoftDeletableModel):
    transaction = models.OneToOneField(
        Transaction,
        on_delete=models.SET_NULL,
        related_name="invoice",
        null=True,
    )
    status = models.CharField(max_length=10, null=False, blank=False)
    user_name = models.CharField(max_length=255, null=False, blank=False)
    user_email = models.EmailField(null=True, blank=True)
    transaction_uuid = models.CharField(max_length=100, editable=False, unique=False)

    promocode_title = models.CharField(max_length=255, null=True, blank=True)
    promocode_code = models.CharField(max_length=255, null=True, blank=True)

    # TODO:// add transaction amount before promocode and after promocode

    class Meta:
        verbose_name = _("Invoice")
        verbose_name_plural = _("Invoice")