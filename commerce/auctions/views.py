from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User

from django.shortcuts import render, redirect
from .models import Listing
from django.contrib.auth.decorators import login_required

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


from decimal import Decimal
from .models import Listing, Bid, Comment
from django.contrib import messages


from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Listing


def index(request):


    listings = Listing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {
        "listings": listings
        
    })
    
    




def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    
    


@login_required
def create_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        image_url = request.POST["image_url"]
        category = request.POST["category"]

        listing = Listing.objects.create(
            title=title,
            description=description,
            starting_bid=starting_bid,
            image_url=image_url,
            category=category,
            created_by=request.user
        )

        return redirect("index")

    return render(request, "auctions/create.html")


@login_required
def watchlist(request):
    listings = request.user.watchlisted_items.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })


@login_required
def toggle_watchlist(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    user = request.user

    if listing in user.watchlisted_items.all():
        user.watchlisted_items.remove(listing)  # remove from watchlist
    else:
        user.watchlisted_items.add(listing)     # add to watchlist

    return redirect("index")




def listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    
    bids = listing.bids.all()
    comments = listing.comments.all()

    highest_bid = bids.order_by("-amount").first()

    current_price = highest_bid.amount if highest_bid else listing.starting_bid

    error = None


    if request.method == "POST" and "bid" in request.POST:
        
        if request.user == listing.created_by:
            error = "You cannot bid on your own listing."
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "current_price": current_price,
                "comments": comments,
                "error": error
            })
        
        if not request.user.is_authenticated:
            return redirect("login")

        bid_amount = Decimal(request.POST["bid"])

        if highest_bid:
            if bid_amount <= highest_bid.amount:
                error = "Bid must be higher than current bid."
            else:
                Bid.objects.create(
                    listing=listing,
                    user=request.user,
                    amount=bid_amount
                )
                return redirect("listing", listing_id=listing.id)
        else:
            if bid_amount < listing.starting_bid:
                error = "Bid must be at least the starting bid."
            else:
                Bid.objects.create(
                    listing=listing,
                    user=request.user,
                    amount=bid_amount
                )
                return redirect("listing", listing_id=listing.id)

    if request.method == "POST" and "comment" in request.POST:
            
        if request.user.is_authenticated:
            Comment.objects.create(
                listing=listing,
                user=request.user,
                content=request.POST["comment"]
            )
            return redirect("listing", listing_id=listing.id)



    return render(request, "auctions/listing.html", {
        "listing": listing,
        "current_price": current_price,
        "comments": comments,
        "error": error
    })


@login_required
def close_auction(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)

    # Only creator can close
    if request.user != listing.created_by:
        return redirect("listing", listing_id=listing.id)

    # Get highest bid
    highest_bid = listing.bids.order_by("-amount").first()

    if highest_bid:
        listing.winner = highest_bid.user
    else:
        listing.winner = None  # No winner if no bids

    listing.is_active = False
    listing.save()

    return redirect("listing", listing_id=listing.id)




@login_required
def closed_listings(request):
    # Only show listings the current user won
    closed_listings = Listing.objects.filter(is_active=False, winner=request.user)

    return render(request, "auctions/close.html", {
        "closed_listings": closed_listings
    })


    
    
def categories(request):
    # Get distinct categories (ignore empty ones)
    categories = Listing.objects.exclude(category="").values_list(
        "category", flat=True
    ).distinct()

    return render(request, "auctions/categories.html", {
        "categories": categories
    })
    
    
def listings_by_category(request, category_name):
    listings = Listing.objects.filter(
        category=category_name,
        is_active=True
    )

    return render(request, "auctions/category.html", {
        "listings": listings,
        "category_name": category_name
    })

    
    
    
    


