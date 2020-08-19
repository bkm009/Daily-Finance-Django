from django import forms
from django.core.validators import MinValueValidator
from app.model.accounts_model import Accounts
from app.model.transactions_model import Transactions


class AccountsTransferForm(forms.ModelForm):

    ac_from = forms.ModelChoiceField(label=u"Transfer From", queryset=Accounts.objects.all(), required=True)
    ac_to = forms.ModelChoiceField(label=u"Transfer To", queryset=Accounts.objects.all(), required=True)
    tr_remark = forms.CharField(label=u"Transfer Remark", required=False)
    tr_amount = forms.FloatField(label=u"Amount to Transfer", required=True, validators=[MinValueValidator(0)])

    def clean(self):

        ac_1 = self.cleaned_data.get("ac_from", None)
        ac_2 = self.cleaned_data.get("ac_to", None)

        if ac_1 is not None and ac_2 is not None:
            if ac_1 == ac_2:
                self.add_error(field='ac_to', error='Transfer Accounts can not be Similar')

        return super(AccountsTransferForm, self).clean()

    def save(self, commit=True):
        instance = super(AccountsTransferForm, self).save(commit=commit)

        ac_from = self.cleaned_data.get("ac_from")
        ac_to = self.cleaned_data.get("ac_to")
        amount = self.cleaned_data.get("tr_amount")
        remark = "Account Transfer to {}. ".format(ac_to) + self.cleaned_data.get("tr_remark")

        txn_data = {
            "amount": amount,
            "txn_type": "DR",
            "txn_reason": remark,
            "txn_date": instance.txn_date,
        }

        # Debit A/C
        txn = Transactions(**txn_data)
        txn.pk = None
        txn.save()
        txn.account.add(ac_from)
        txn.save()

        # Debit A/C
        txn_data["txn_type"] = "CR"
        txn_data["txn_reason"] = "Account Transfer from {}. ".format(ac_from) + self.cleaned_data.get("tr_remark")

        txn = Transactions(**txn_data)
        txn.pk = None
        txn.save()
        txn.account.add(ac_to)
        txn.save()

        return txn


