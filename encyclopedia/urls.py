from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry_title>", views.entry_details, name="details"),
    path("search", views.entry_search, name="search"),
    path("add", views.entry_add, name="add"),
    path("edit/<str:entry_title>", views.edit_entry, name='edit_entry'),
    path("random", views.randon_entry, name='random')
]
