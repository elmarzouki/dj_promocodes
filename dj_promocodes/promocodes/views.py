from rest_framework import renderers
from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveAPIView
from dj_promocodes.promocodes.models import Promocode
from dj_promocodes.promocodes.serializers import PromocodeSerializer


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
