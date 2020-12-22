from django.contrib import admin
from .models import *

class BidsAdmin(admin.ModelAdmin):
    fields = [
        'bid'
    ]

class AuctionAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Auction Info', {
            'fields': (
                'category',
                'title',
                'current_bid',
                'description',
                'image_url',
                'user',
                'active'
            ),
            'classes': ('collapse')
        }),
        ('Metadata', {
            'fields': (
                'comments',
                'users_watchlist',
                'winner'
            )
        })
    )
    

# Register your models here.
admin.site.register(AuctionCategory)
admin.site.register(Auction, AuctionAdmin)
admin.site.register(Bids, BidsAdmin)
admin.site.register(Comments)

admin.site.register(User)

