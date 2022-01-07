from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.forms.widgets import NumberInput
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from .models import User, Category, Listing, Bid, Comment


class NewListingForm(forms.Form):
    title = forms.CharField(required=True, max_length=100, widget=forms.TextInput())
    description = forms.CharField(required=True, widget=forms.Textarea())
    starting_bid = forms.FloatField(required=True, min_value=0, widget=forms.NumberInput())
    image = forms.CharField(required=True, widget=forms.TextInput())
    category = forms.CharField(required=True, widget=forms.TextInput())

class PlaceBidForm(forms.Form):
  amount = forms.FloatField(required=True, widget=NumberInput())

def index(request):
    Listing.objects.all()
    return render(request, "auctions/index.html", {
        'listings': Listing.objects.all()
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


def listing_list(request):
    print()


def listing_details(request, id):
    listing = Listing.objects.get(id=id)
    if listing.bid_set.all().count() > 0:
      winning_bid = listing.bid_set.order_by('-amount')[0]
    else:
      winning_bid = None
    return render(request, "auctions/listing_details.html", {
        "listing": listing,
        "bids": listing.bid_set.all(),
        "winning_bid": winning_bid,
        "comments": listing.comment_set.all(),
        "placeBidForm": PlaceBidForm()
    })


@login_required
def listing_create(request):
    if request.method == 'POST':
        form = NewListingForm(request.POST)
        if form.is_valid():
            form.clean()
            title = form.cleaned_data['title'].capitalize()
            description = form.cleaned_data['description'].capitalize()
            starting_bid = form.cleaned_data['starting_bid']
            image = form.cleaned_data['image']
            form_category = form.cleaned_data['category'].capitalize()
            category = Category.objects.filter(name=form_category)
            if category.exists():
                category = category[0]
            else:
              category = Category(name=form_category).save()
            listing = Listing(title=title, description=description, starting_bid=starting_bid,image=image, user=request.user, category=category)
            listing.save()
            return HttpResponseRedirect(reverse("listing_details", args=[listing.id]))

    else:
        form = NewListingForm()
        return render(request, 'auctions/listing_create.html', {'form': form})


@login_required
def listing_terminate(request, id):
  if request.method == 'POST':
    listing = Listing.objects.get(id=id)
    if request.user == listing.user:
      winner = listing.bid_set.order_by('-amount')[0].user
      listing.winner = winner
      listing.terminated = True
      listing.save()
      return HttpResponseRedirect(reverse("listing_details", args=[listing.id]))
  else:
    return HttpResponseRedirect(reverse("auctions/index.html", {
        'listings': Listing.objects.all()
    }))


@login_required
def bid_add(request, id):
    if request.method == 'POST':
      form = PlaceBidForm(request.POST)
      if form.is_valid():
        form.clean()
        amount = form.cleaned_data['amount']
        listing = Listing.objects.get(pk=id)
        if listing.bid_set.all().count() > 0:
          winning_bid = listing.bid_set.order_by('-amount')[0]
          if amount > winning_bid.amount:
            bid = Bid(amount=amount, listing=listing, user=request.user)
        elif listing.bid_set.all().count() == 0:
          bid = Bid(amount=amount, listing=listing, user=request.user)
        bid.save()
        return HttpResponseRedirect(reverse("listing_details", args=[listing.id]))


@login_required
def watchlist(request):
    print()


@login_required
def watchlist_add(request, id):
    listing = Listing.objects.get(pk=id)
    user = request.user
    if listing not in user.watch_list.all():
      user.watch_list.add(listing)
    return HttpResponseRedirect(reverse("listing_details", args=[listing.id]))


@login_required
def watchlist_remove(request, id):
    user = request.user
    listing = Listing.objects.get(pk=id)
    user.watch_list.remove(listing)
    return HttpResponseRedirect(reverse("listing_details", args=[listing.id]))
