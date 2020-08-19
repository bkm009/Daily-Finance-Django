from django.contrib.admin import ModelAdmin
from app.modelforms.accounts_transfer_form import AccountsTransferForm


class AccountTransferAdmin(ModelAdmin):

    def has_view_or_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    form = AccountsTransferForm
    exclude = ["account", "amount", "txn_date", "txn_reason", "txn_type"]
    fieldsets = (
        ("Transfer Details", {'fields': (
            ("ac_from", "ac_to"),
            ("tr_amount", "tr_remark"),
        )}),
    )
