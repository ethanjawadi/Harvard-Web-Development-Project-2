from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .models import User, Listing, Category
from .forms import ListingForm
from django.contrib.auth.decorators import login_required


def index(request):
    active_listings = Listing.objects.filter(active=True)
    categories = Category.objects.all()
    return render(request, "auctions/index.html", {"active_listings": active_listings, "categories": categories})


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
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.creator = request.user
            listing.save()
            return redirect('index')
    else:
        form = ListingForm()
    categories = Category.objects.all()
    return render(request, 'auctions/create_listing.html', {'form': form, 'categories': categories})

def listing_detail(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    
    # Check if the listing is in the user's watchlist
    on_watchlist = False
    if request.user.is_authenticated and listing in request.user.watchlist.all():
        on_watchlist = True

    # Handle add/remove from watchlist
    if request.method == 'POST':
        if 'toggle_watchlist' in request.POST:
            if on_watchlist:
                request.user.watchlist.remove(listing)
            else:
                request.user.watchlist.add(listing)
            return redirect('listing_detail', listing_id=listing_id)

    categories = Category.objects.all()
    return render(request, 'auctions/listing_detail.html', {'listing': listing, 'on_watchlist': on_watchlist, 'categories': categories})

@login_required
def watchlist(request):
    categories = Category.objects.all()
    return render(request, 'auctions/watchlist.html', {'watchlist': request.user.watchlist.all(), 'categories': categories})

def category_view(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    listings = Listing.objects.filter(category=category, active=True)
    categories = Category.objects.all()
    return render(request, 'auctions/category.html', {'category': category, 'listings': listings, 'categories': categories})
