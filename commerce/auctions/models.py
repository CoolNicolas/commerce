from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # Users can watch multiple listings
    watchlisted_items = models.ManyToManyField(
        "Listing", blank=True, related_name="watchers"
    )
    # Users can see their closed listings
    closed_listings = models.ManyToManyField(
        "Listing", blank=True, related_name="closed_by_users"
    )


class Listing(models.Model):
    title = models.CharField(max_length=64)
    
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(blank=True)
    category = models.CharField(max_length=64, blank=True)
    created_by = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="listings"
    )

    is_active = models.BooleanField(default=True)
    winner = models.ForeignKey(
        "User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="won_listings"
    )

    def __str__(self):
        return f"{self.title} by {self.created_by.username}"


class Bid(models.Model):
    listing = models.ForeignKey("Listing", on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.amount} by {self.user}"


class Comment(models.Model):
    listing = models.ForeignKey("Listing", on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f"Comment by {self.user}"
