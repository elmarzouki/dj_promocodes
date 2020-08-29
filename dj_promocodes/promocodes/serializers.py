from rest_framework import serializers
from dj_promocodes.promocodes.models import Promocode, Balance


class PromocodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promocode
        fields = (
            "title",
            "description",
            "quantity",
            "code",
            "start_date",
            "end_date",
            "frequency_of_use",
            "is_active",
            "benefits",
        )
