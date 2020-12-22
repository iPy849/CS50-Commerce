import math

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import *
from .util import *

#region authentication system 

def index(request):
    user_auctions = None
    if request.user.is_authenticated:
        user_auctions = request.user.auctions.all()

    return render(request, "auctions/index.html",{
        'users': User.objects.all(),
        'auctions': Auction.objects.all(),
        'latest': Auction.objects.order_by('-id')[:4],
        'user_auctions': user_auctions
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

#endregion


#region auctions controls

@authentication_required
def create_auction_view(request):
    if request.method == 'POST':
        new_auction = Auction()
        new_auction.category = AuctionCategory.objects.get(pk=int(request.POST['category']))
        new_auction.title = request.POST['title']
        new_auction.description = request.POST['description']
        new_bid = Bids(bid=float(request.POST['price']))
        new_bid.save()
        new_auction.current_bid = new_bid
        new_auction.image_url = request.POST['image_url']
        new_auction.user = request.user
        new_auction.save()
        return redirect('index')

    return render(request, 'auctions/create_auction.html', {
        'categories': AuctionCategory.objects.order_by('category')
    })

def auction_details_view(request, id):
    auction = Auction.objects.get(pk=id)

    if request.method == 'POST':
        option = int(request.POST['option'])
        if option == 1:
            current_bid = auction.current_bid
            new_bid_value = float(request.POST['bid'])
            if current_bid.bid == new_bid_value:
                return redirect('detail_auction', id=id)
            current_bid.bid = new_bid_value
            current_bid.user = request.user
            current_bid.save()
        else:
            new_comment = Comments()
            new_comment.user = request.user
            new_comment.text = request.POST['comment_text']
            new_comment.save()
            auction.comments.add(new_comment)
            auction.save()

    return render(request, 'auctions/auction.html', {
        'users': User.objects.all(),
        'owner': auction.user == request.user,
        'auction': auction,
        'comments': auction.comments.all(),
        'is_in_watchlist': auction in request.user.watchlist.all(),
        'min_bid': auction.current_bid.bid + math.ceil(auction.current_bid.bid * 0.02)
    })

def delete_auction(request, id):
    auction = Auction.objects.get(pk=id)
    for comment in auction.comments.all():
        comment.delete()
    auction.current_bid.delete()
    auction.delete()
    return redirect('index')

def end_auction(request, id):
    auction = Auction.objects.get(pk=id)
    if auction.current_bid.user:
        auction.active = False
        auction.winner = User.objects.get(pk=auction.current_bid.user.id)
        auction.winner.won = True
        auction.winner.save()
        auction.save()
        return redirect('index')
    else:
        return render(request, 'auctions/auction.html', {
        'message': 'Nobody have pushed this bid. Wait for a bid to close this auction',
        'users': User.objects.all(),
        'owner': auction.user == request.user,
        'auction': auction,
        'comments': auction.comments.all(),
        'is_in_watchlist': auction in request.user.watchlist.all(),
        'min_bid': auction.current_bid.bid + math.ceil(auction.current_bid.bid * 0.02)
    })


def winner_notification(request, id):
    auction = Auction.objects.get(pk=id)
    auction.winner.won = False
    auction.delete()
    return redirect(index)

def add_to_watchlist(request, id):
    auction = Auction.objects.get(pk=id)
    request.user.watchlist.add(auction)
    request.user.save()
    return redirect('detail_auction', id=id)

def delete_from_watchlist(request, id):
    auction = Auction.objects.get(pk=id)
    request.user.watchlist.remove(auction)
    request.user.save()
    return redirect('detail_auction', id=id)

#endregion

#region watchlist and categories

@authentication_required
def watchlist_view(request):
    watclist_items = list(request.user.watchlist.all())
    list.reverse(watclist_items)
    return render(request, 'auctions/watchlist.html', {
        'watchlist': watclist_items,
    })

def category_selection_view(request):
    colors = [
        'primary',
        'secondary',
        'success',
        'danger',
        'warning',
        'info',
        'light',
        'dark',
        'white',
    ]
    pill_menu = []
    categories = AuctionCategory.objects.order_by('category')
    for i in range(0, len(categories)):
        pill_menu.append(
            [ categories[i], colors[i%len(colors)]]
        )
    
    return render(request, 'auctions/categories_selection.html', {
        'categories': pill_menu
    })

def category_view(request, id):
    category = AuctionCategory.objects.get(pk=id)
    return render(request, 'auctions/category.html', {
        'category': category,
        'auctions': category.auctions.order_by('created_at')
    })

#endregion