from django.db import models
from app.model.accounts_model import Accounts


class InterestTrack(models.Model):
    account = models.ManyToManyField(Accounts, related_name="int_account_relationship")
    interest_added = models.DateTimeField(null=False)
