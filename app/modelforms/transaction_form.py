from django import forms
from app.model.transactions_model import Transactions
from app.model.accounts_model import Accounts


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transactions
        fields = '__all__'
        widgets = {
            'account': forms.Select,
        }

    def __init__(self, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)

        if hasattr(self, "apk") and self.apk is not None:
            apk = Accounts.get_object({"pk": self.apk})
            if not apk:
                for k in list(self.fields.keys()):
                    self.fields[k].widget.attrs['disabled'] = True

            self.fields['account'] = forms.CharField(initial=str(apk), widget=forms.TextInput(attrs={'disabled': True}))

        else:
            self.fields['account'] = forms.CharField(initial="(self)", widget=forms.TextInput(attrs={'disabled': True}))

    def clean(self):
        if "account" in self.errors:
            del self.errors["account"]

        if "account" in self.changed_data:
            self.changed_data.remove("account")

        if hasattr(self, "apk") and self.apk is not None:
            apk = Accounts.get_object({"pk": self.apk})
            if not apk:
                for k in list(self.fields.keys()):
                    self.fields[k].widget.attrs['disabled'] = True

            self.fields['account'] = forms.CharField(initial=str(apk), widget=forms.TextInput(attrs={'disabled': True}))

        else:
            self.fields['account'] = forms.CharField(initial="(self)", widget=forms.TextInput(attrs={'disabled': True}))

            tp = self.instance.total_profit
            amount = self.cleaned_data.get("amount", None)
            txn_type = self.cleaned_data.get("txn_type", None)

            if tp is None and txn_type == 'DR':
                self.add_error(field='total_profit', error='Try Again')

            if amount and tp and txn_type == 'DR':
                if amount > tp:
                    self.add_error(field='amount', error='Amount can not be greater than Total Profit')

    def save(self, commit=True):
        instance = super(TransactionForm, self).save(commit=commit)
        apk = None
        if hasattr(self, "apk") and self.apk is not None:
            apk = Accounts.get_object({"pk": self.apk})

        instance.save()
        instance.account.add(apk)
        return instance
