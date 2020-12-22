from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    won = models.BooleanField(null=False, default=False)

    def auctions_won(self):
        return list(self.won_auctions.all())


class AuctionCategory(models.Model):
    category = models.CharField(max_length=30, unique=True, null=False)

    def __str__(self):
        return self.category


class Bids(models.Model):
    bid = models.FloatField(null=False)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return f'{self.bid}'


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', null=True)
    text = models.TextField(editable=True)
    datetime = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self):
        return self.text


class Auction(models.Model):
    title = models.CharField(max_length=100, null=False)
    description = models.TextField(editable=True)
    category = models.ForeignKey( AuctionCategory, on_delete=models.DO_NOTHING, related_name='auctions', null=False)
    current_bid = models.ForeignKey(Bids, on_delete=models.CASCADE, related_name='auctions')
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='auctions', null=True)
    comments = models.ManyToManyField(Comments, blank=True, related_name='auctions')
    image_url = models.URLField(null=True)
    active = models.BooleanField(null=False, default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    users_watchlist = models.ManyToManyField(User, blank=True, related_name='watchlist')
    winner = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='won_auctions', blank=True, null=True)

    def __str__(self):
        return f'{self.category}: {self.title} -> {self.current_bid}'