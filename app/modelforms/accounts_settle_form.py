from django import forms
from django.core.validators import MinValueValidator
from django.utils.timezone import now
from app.model.accounts_model import Accounts
from app.model.transactions_model import Transactions


class AccountsSettleForm(forms.ModelForm):

    ac = forms.ModelChoiceField(label=u"Account", required=True,
                                queryset=Accounts.objects.filter(account_status=0, loan_type__in=['DF', 'ST','MT']))
    tr_remark = forms.CharField(label=u"Settlement Remark", required=False)
    tr_amount = forms.FloatField(label=u"Settlement Amount", required=True, validators=[MinValueValidator(0)])

    def clean(self):
        ac = self.cleaned_data.get("ac", None)
        tr_amount = self.cleaned_data.get("tr_amount", None)

        if ac.loan_amount > tr_amount:
            self.add_error(field='tr_amount',
                           error='Settlement Accounts should be Equal or Greater than Principal Amount')

        return super(AccountsSettleForm, self).clean()

    def save(self, commit=True):
        instance = super(AccountsSettleForm, self).save(commit=commit)

        ac = self.cleaned_data.get("ac")
        amount = self.cleaned_data.get("tr_amount")
        remark = self.cleaned_data.get("tr_remark")

        txn_data = {
            "amount": ac.loan_amount,
            "txn_type": "CR",
            "txn_reason": "Account Settled. Remark : {}".format(remark),
            "txn_date": instance.txn_date,
        }

        # Credit Principal Amount
        txn = Transactions(**txn_data)
        txn.pk = None
        txn.save()
        txn.account.add(ac)
        txn.save()

        txn_data = {
            "amount": amount - ac.loan_amount,
            "txn_type": "CR",
            "txn_reason": "Account Settled. Interest Added. Remark : {}".format(remark),
            "txn_date": instance.txn_date,
        }

        # Credit Interest Amount
        txn = Transactions(**txn_data)
        txn.pk = None
        txn.save()
        txn.account.add(ac)
        txn.save()

        total_due = 0.0
        total_paid = 0.0

        for txn in Transactions.objects.filter(account=ac):
            if txn.txn_type == "DR":
                total_due += txn.amount
            else:
                total_paid += txn.amount

        rem = total_due - total_paid

        if rem > 0:
            txn_data = {
                "amount": rem,
                "txn_type": "CR",
                "txn_reason": "Account Settled. Interest Waiver. Remark : {}".format(remark),
                "txn_date": instance.txn_date,
            }

            # Credit Interest Amount
            txn = Transactions(**txn_data)
            txn.pk = None
            txn.save()
            txn.account.add(ac)
            txn.save()

        ac.loan_closed = now()
        ac.account_status = 1
        ac.save()

        return txn
