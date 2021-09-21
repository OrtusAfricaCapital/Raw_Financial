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
    InstitutionalLimit = models.DecimalField(max_digits=13, decimal_places=4)
    RevolvingLimit = models.DecimalField(max_digits=13, decimal_places=4)
    DailyInterestRate = models.FloatField()
    MonthlyInterestRate = models.FloatField()
    Logo = models.ImageField(null=True, blank=True)
    Description = models.TextField()
    CreatedBy = models.ForeignKey(User, on_delete=models.CASCADE)
    TrustNetworkCategory = models.CharField(max_length=32)
    RequiresApproval = models.CharField(max_length=10, choices=REQUIRES_APPROVAL)
    RequiredApproval = models.CharField(max_length=32)
    Domains = models.TextField()

    def __str__(self):
        return self.Name


