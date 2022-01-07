from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/create",views.listing_create, name="listing_create"),
    path("listing/item/<str:id>", views.listing_details, name="listing_details"),
    path("listing/terminate/<str:id>/", views.listing_terminate, name="listing_terminate"),
    path("listing/bid/<str:id>", views.bid_add, name="bid_add"),
    path("watchlist", views.watchlist, name='watchlist'),
    path("watchlist/<str:id>/add", views.watchlist_add, name='watchlist_add'),
    path("watchlist/<str:id>remove", views.watchlist_remove, name='watchlist_remove')
]
