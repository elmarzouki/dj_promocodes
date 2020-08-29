import uuid as uuid
from rest_framework import renderers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveAPIView
from django.contrib.auth import get_user_model
from dj_promocodes.promocodes.models import Promocode, Transaction, Invoice
from dj_promocodes.promocodes.serializers import (
    PromocodeSerializer,
    PaySerializer,
    InvoiceSerializer,
)

User = get_user_model()  # django auth.user


class PromocodeDetailView(RetrieveAPIView):
    model = Promocode
    serializer_class = PromocodeSerializer
    renderer_classes = [
        renderers.JSONRenderer,
        renderers.BrowsableAPIRenderer,
        renderers.TemplateHTMLRenderer,
    ]

    def get_object(self):
        return get_object_or_404(Promocode, code=self.kwargs["promocode_code"])


class Pay(APIView):
    renderer_classes = [
        renderers.JSONRenderer,
        renderers.BrowsableAPIRenderer,
        renderers.TemplateHTMLRenderer,
    ]

    def post(self, request, *args, **kwargs):
        # serialization
        serializer = PaySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # get req data
        amount = serializer.validated_data.get("amount")
        promocode_code = serializer.validated_data.get("promocode_code")
        user_id = serializer.validated_data.get("user_id")

        user = User.objects.get(pk=user_id)
        promocode = Promocode.objects.get(code=promocode_code)
        # create a PENDING transaction
        transaction = Transaction.objects.create(
            uuid=str(uuid.uuid4()),
            user=user,
            promocode=promocode,
        )
        # assuming we got a successfull callback from the paid card
        transaction.status = "SUCCESSFUL"
        transaction.save()
        # create an invoice
        invoice = Invoice.objects.create(
            transaction=transaction,
            status=transaction.status,
            user_name=user.username,
            user_email=user.email,
            transaction_uuid=transaction.uuid,
            promocode_title=promocode.title,
            promocode_code=promocode.code,
        )
        invoice_serializer = InvoiceSerializer(invoice)
        return Response(invoice_serializer.data)