from django.db import models
from trust_network.models import *


# Create your models here.
class Borrower(models.Model):
    tn = models.ForeignKey(TrustNetwork, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name

