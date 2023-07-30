from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path(
        "wikipage/partials/history-list/",
        views.WikiPageHistoryPartialView.as_view(),
        name="wikipage-history-list-partial",
    ),
]
