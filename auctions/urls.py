from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create_listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/<int:listing_id>", views.toggle_watchlist, name="toggle_watchlist"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("close/<int:listing_id>", views.close_auction, name="close_auction"),
    path("close_auction/<int:listing_id>/", views.close_auction, name="close_auction"),
    path("close/<int:listing_id>", views.closed_listings, name="close_listing"),
    path("closed/", views.closed_listings, name="closed_listings"),
    path("categories/", views.categories, name="categories"),
    path("category/<str:category_name>/", views.listings_by_category, name="category"),


    
    
    
    
    
    
    
]
