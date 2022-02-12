from uuid import UUID
from django.db import models
from trust_network.models import *
import random
import uuid
# Create your models here.

def borrower_rand():
    rand = random.randint(1000,9000)
    return "BR-"+str(rand)


class Borrower(models.Model):
    borrower_id = models.UUIDField(default=uuid.uuid4, editable=False)
    channel_borrower_uid = models.CharField(max_length=100, null=True, blank=True)
    tn = models.ForeignKey(TrustNetwork, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.borrower_id) +"-"+ self.first_name+" " + self.last_name

