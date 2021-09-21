from django.db import models
from helpers.models import TrackingModel
from authentication.models import User

# Create your models here.
class FinancialInstitution(models.Model):
    Name = models.CharField(max_length=250)
    DailyInterestRate = models.FloatField()
    MonthlyInterestRate = models.FloatField()
    EmailAddress = models.EmailField(max_length=250)
    PhoneNumber = models.CharField(max_length=250)
    VerificationStatus = models.CharField(max_length=32)
    InstitutionalStatus = models.CharField(max_length=32)
    Image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.Name

    



