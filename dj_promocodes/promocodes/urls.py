from django.urls import path

from dj_promocodes.promocodes.views import PromocodeDetailView

app_name = "promocodes"

urlpatterns = [
    path(
        "promocode/<str:promocode_code>",
        PromocodeDetailView.as_view(),
        name="promocode-detail-view",
    ),
]
