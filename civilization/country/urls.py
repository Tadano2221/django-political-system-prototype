from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "country/<int:country_id>/",
        views.public_state,
        name="public_state",
    ),

    path(
        "country/<int:country_id>/system/",
        views.system_view,
        name="system_view",
    )
]