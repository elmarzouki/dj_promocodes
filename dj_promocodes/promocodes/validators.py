from django.utils import timezone
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.serializers import ValidationError
from dj_promocodes.promocodes.models import Promocode

User = get_user_model()  # django auth.user


def validate_redeem(promocode_code, user_id):
    promocode = get_object_or_404(Promocode, code=promocode_code)

    # validate if is_active
    if not promocode.is_active:
        raise ValidationError({"promocode_code": "This promocode isn't active!"})

    # validate redeem dates
    now = timezone.localtime(timezone.now()).date()
    if promocode.start_date > now or promocode.end_date < now:
        raise ValidationError({"promocode_code": "This promocode isn't active!"})

    # validate quantity
    transactions = promocode.transactions.filter(
        status="SUCCESSFUL", promocode__code=promocode_code
    )
    sold = transactions.count()
    if promocode.quantity <= sold:
        raise ValidationError({"promocode_code": "This promocode is already sold!"})

    # validate quantity per user
    user = get_object_or_404(User, pk=user_id)
    sold_frequency = transactions.filter(user=user).count()
    if promocode.frequency_of_use <= sold_frequency:
        raise ValidationError(
            {"promocode_code": "You already used this promocode before!"}
        )
