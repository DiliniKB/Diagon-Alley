from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    

class Listing(models.Model):
    catArray = [
        ("PET","Pets"),
        ("BOOK","Books and Stationary"),
        ("WAND","Wands"),
        ("BROOM","Broomsticks"),
        ("CAULDRAN","Cauldrons"),
        ("CLOTHING","Clothings"),
        ("TRICKS","Tricks"),
        ("OTHER","Other")
    ]
    title = models.CharField(max_length=255)
    description = models.TextField()
    currunt_price = models.IntegerField()
    category = models.CharField(choices=catArray,max_length=64)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing")
    image = models.URLField(max_length=255, blank=True)
    watchlist = models.ManyToManyField(User, blank=True, related_name="users")

    def __str__(self) :
        return f"{self.id} {self.title} "

# class Bid(models.Model):
#     listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bid")
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
#     price = models.IntegerField()

# class Watchlist(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
#     listings = models.ManyToManyField(Listing, blank=True, related_name="users")

#     def __str__(self) :
#         return f"{self.user}"
