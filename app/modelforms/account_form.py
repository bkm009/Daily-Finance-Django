from django import forms
from django.utils.timezone import now
from app.model.accounts_model import Accounts
from app.model.transactions_model import Transactions


DISABLED_FIELDS = (
    "loan_type",
    "loan_amount",
    "loan_rate",
    "loan_duration",
    "loan_duration_type",
    "advance_amount",
    "documents_submitted",
    "particular_name",
    "particular_father_husband_name",
    "guaranteer_name",
    "guaranteer_father_husband_name",
)


class AccountForm(forms.ModelForm):
    class Meta:
        model = Accounts
        fields = '__all__'
        widgets = {
            'documents_submitted': forms.widgets.RadioSelect,
        }

    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            for each_field in DISABLED_FIELDS:
                if each_field in self.fields:
                    self.fields[each_field].widget.attrs['disabled'] = True

            if instance.account_status == 1 and 'account_status' in self.fields:
                self.fields['account_status'].widget.attrs['disabled'] = True

    def clean(self):

        if self.instance and self.instance.pk:
            for each_field in DISABLED_FIELDS:
                if each_field in self.changed_data:
                    self.changed_data.remove(each_field)
                if each_field in self.errors:
                    del self.errors[each_field]

        return super(AccountForm, self).clean()

    def save(self, commit=True):
        instance = super(AccountForm, self).save(commit=commit)

        add_txns = False
        if instance and not instance.pk:
            add_txns = True

        # If A/C is closed. Update Loan Closing Date.
        if instance and instance.account_status and instance.account_status == 1:
            instance.loan_closed = now()

        instance.save()
        if add_txns and instance:
            txn_data = {
                "amount": instance.loan_amount,
                "txn_type": "DR",
                "txn_reason": "{} Loan Approved.".format(instance.loan_type)
            }

            if instance.loan_type in ["DS", "FD", "SM", "SS"]:
                txn_data["txn_type"] = "CR"
                txn_data["txn_reason"] = "{} Deposit Opened.".format(instance.loan_type)

            txn = Transactions(**txn_data)
            txn.pk = None
            txn.save()
            txn.account.add(instance)
            txn.save()

            if instance.loan_type in ["ST", "DF"]:
                txn_data = {
                    "amount": instance.advance_amount,
                    "txn_type": "IN",
                    "txn_reason": "Advance Deposited"
                }

                txn = Transactions(**txn_data)
                txn.pk = None
                txn.save()
                txn.account.add(instance)
                txn.save()

                txn_data["txn_type"] = "DR"
                txn_data["txn_reason"] = "Interest Added."
                txn = Transactions(**txn_data)
                txn.pk = None
                txn.save()
                txn.account.add(instance)
                txn.save()

        return instance
