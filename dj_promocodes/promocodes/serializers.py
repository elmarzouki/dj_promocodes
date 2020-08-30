from rest_framework import serializers
from django.contrib.auth import get_user_model
from dj_promocodes.promocodes import validators
from dj_promocodes.promocodes.models import Promocode, Balance, Invoice, Transaction

User = get_user_model()  # django auth.user


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
            # "available_redeem",
        )


class PaySerializer(serializers.Serializer):
    amount = serializers.IntegerField(required=True, min_value=0)
    promocode_code = serializers.CharField(required=True)
    user_id = serializers.CharField(required=True)

    def validate(self, data):
        promocode_code = data.get("promocode_code")
        user_id = data.get("user_id")
        validators.validate_redeem(promocode_code, user_id)
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "name",
        )


class TransactionSerializer(serializers.ModelSerializer):
    promocode = PromocodeSerializer()
    user = UserSerializer()

    class Meta:
        model = Transaction
        fields = (
            "uuid",
            "payment_for",
            "pay_using",
            "status",
            "user",
            "promocode",
        )


class InvoiceSerializer(serializers.ModelSerializer):
    transaction = TransactionSerializer()

    class Meta:
        model = Invoice
        fields = (
            "transaction",
            "status",
            "user_name",
            "user_email",
            "transaction_uuid",
            "promocode_title",
            "promocode_code",
        )