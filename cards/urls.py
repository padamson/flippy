# cards/urls.py

from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path(
        "",
        TemplateView.as_view(template_name="home.html"),
        name="home"
    ),
    path(
        "all/{object_list}/",
        views.CardListView.as_view(template_name="all.html"),
        name="card-list"
    ),
]
