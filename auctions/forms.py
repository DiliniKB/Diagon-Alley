# from xml.parsers.expat import model
from django.forms import ModelForm
from .models import Listing

class create_listing(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', "description", "currunt_price", "category", "image"]
