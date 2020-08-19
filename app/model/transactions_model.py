from django.core import validators
from django.db import models
from django.db.models import Sum
from django.utils.timezone import now
from .accounts_model import Accounts


TXN_TYPES = (
    ("DR", "DEBIT"),
    ("CR", "CREDIT"),
    ("PR", "PENALTY"),
    ("IN", "INTEREST"),
)


class Transactions(models.Model):
    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'

    account = models.ManyToManyField(Accounts, verbose_name=u"Account", help_text="Select Account for Transaction",
                                     blank=False, related_name="txn_account_relationship")

    amount = models.FloatField(verbose_name=u"Amount of Entry", help_text="Enter received Amount", blank=False,
                               validators=[validators.MinValueValidator(0.0)])

    txn_date = models.DateTimeField(auto_created=True, default=now)
    txn_reason = models.CharField(verbose_name=u"Transaction Remark", max_length=512, null=True, blank=True,
                                  help_text="Remark for Transaction")

    txn_type = models.CharField(verbose_name=u"Transaction Type", max_length=5, choices=TXN_TYPES, default="CR",
                                blank=False, null=True, help_text="Type of Transaction")

    @property
    def total_profit(self):
        try:
            if self and self.pk:
                return None

            tp = Transactions.objects.filter(txn_type__in=["PR", "IN"]).aggregate(Sum("amount"))['amount__sum']
            return tp
        except:
            return None

    def __str__(self):
        return "Txn - %s" % self.pk


class AccountTransfer(Transactions):
    class Meta:
        proxy = True
        verbose_name = 'Account Transfer'
        verbose_name_plural = 'Account Transfer'


class AccountSettlement(Transactions):
    class Meta:
        proxy = True
        verbose_name = 'Account Settlement'
        verbose_name_plural = 'Account Settlement'
