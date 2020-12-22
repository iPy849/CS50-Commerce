from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('winner_notification/<int:id>', views.winner_notification, name="winner_notification"),
    path("watchlist", views.watchlist_view, name="watchlist"),
    path("categories_selection", views.category_selection_view, name="category_selection"),
    path("category/<int:id>", views.category_view, name="category"),
    path('new', views.create_auction_view, name='create_auction'),
    path('auction/<int:id>', views.auction_details_view, name='detail_auction'),
    path('auction/<int:id>/delete_auction', views.delete_auction, name='delete_auction'),
    path('auction/<int:id>/end_auction', views.end_auction, name='end_auction'),
    path('auction/<int:id>/add_watchlist', views.add_to_watchlist, name='add_to_watchlist'),
    path('auction/<int:id>/delete_watchlist', views.delete_from_watchlist, name='delete_from_watchlist'),
]
