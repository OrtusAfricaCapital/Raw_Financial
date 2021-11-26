from django.db import models
from django.utils.translation import deactivate
from helpers.models import TrackingModel

# Create your models here.
class Channel(models.Model):
    ChannelName = models.CharField(max_length=250)
    Logo = models.ImageField(null=True, blank=True)
    WebHook = models.CharField(max_length=250)
    EmailAddress = models.EmailField(max_length=250, unique=True)
    PhoneNumber = models.CharField(max_length=25)
    ShortDescription = models.TextField(max_length=250)
    LongDescription = models.TextField(max_length=512)
    DeactivatedOn = models.DateTimeField(null=True, blank=True)
    ApiKey = models.CharField(max_length=36)

    def __str__(self):
        return self.ChannelName



