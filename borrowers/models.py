from django.db import models
from trust_network.models import *
import random

# Create your models here.

def borrower_rand():
    rand = random.randint(1000,9000)
    return "BR-"+str(rand)


class Borrower(models.Model):
    borrower_id = models.CharField(max_length=20, default=borrower_rand, editable=False, blank=True)
    channel_borrower_uid = models.CharField(max_length=100)
    tn = models.ForeignKey(TrustNetwork, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.borrower_id

