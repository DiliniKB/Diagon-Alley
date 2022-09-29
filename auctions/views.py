from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Listing, User
from .forms import create_listing


def index(request):
    return render(request, "auctions/index.html", {
      "listings": Listing.objects.all()  
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

def categories(request):
    catArray = [
        "Pets",
        "Books and Stationary",
        "Wands",
        "Broomsticks",
        "Cauldrons",
        "Clothing",
        "Tricks",
        "Other"
    ]

    return render(request, 'auctions/categories.html', {
        'catArray': catArray,
        'listings' : Listing.objects.all()
    })

def create(request):
    # pass
    if request.method == 'POST':
        form = create_listing(request.POST)
        if form.is_valid():
            listing = Listing()
            listing.title = form.cleaned_data['title']
            listing.description = form.cleaned_data['description']
            listing.currunt_price = form.cleaned_data['currunt_price']
            listing.category = form.cleaned_data['category']
            listing.user = User.objects.get(id = request.user.id) 
            listing.image = form.cleaned_data['image']
            listing.save()
            return HttpResponseRedirect(reverse("index"))
    else :
        return render(request, 'auctions/create.html', {
            "form": create_listing()
        })

def listing_view(request, listing_id):
    return render(request, 'auctions/view.html', {
        "listing": Listing.objects.get(id=listing_id),
        "message": ""
    })

def addtoWatchlist(request, listing_id):
    try: 
        listings = Listing.objects.get(id=listing_id)
        user = User.objects.get(id=request.user.id)
        Watchlist.listings.add(user)
        return render(request, "auctions/view.html", {
            "listing": Listing.objects.get(id=listing_id),
            "message": "Succcess"
        })
    except Watchlist.DoesNotExist:
        return render(request, "auctions/view.html", {
                "listing": Listing.objects.get(id=listing_id),
                "message": "No database"
            })
