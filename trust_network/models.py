from django.db import models
from helpers.models import TrackingModel
from authentication.models import User
from channel.models import Channel

# Create your models here.
REQUIRES_APPROVAL = (
    ("yes","yes"),
    ("no","no"),
)



class TrustNetwork(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    Name = models.CharField(max_length=250)
    InstitutionalLimit = models.DecimalField(max_digits=13, decimal_places=4, null=True, blank=True)
    RevolvingLimit = models.DecimalField(max_digits=13, decimal_places=4, null=True, blank=True)
    DailyInterestRate = models.FloatField(blank=True, null=True)
    MonthlyInterestRate = models.FloatField(blank=True, null=True)
    Logo = models.ImageField(null=True, blank=True)
    Description = models.TextField()
    CreatedBy = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    TrustNetworkCategory = models.CharField(max_length=32, blank=True, null=True)
    RequiresApproval = models.CharField(max_length=10, choices=REQUIRES_APPROVAL, null=True, blank=True)
    RequiredApproval = models.CharField(max_length=32, blank=True, null=True)
    Domains = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.Name


