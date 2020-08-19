from django.contrib.admin import ModelAdmin
from app.modelforms.accounts_settle_form import AccountsSettleForm


class AccountSettlementAdmin(ModelAdmin):

    def has_view_or_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    form = AccountsSettleForm
    exclude = ["account", "amount", "txn_date", "txn_reason", "txn_type"]
    fieldsets = (
        ("Settlement Details", {'fields': (
            ("ac", ),
            ("tr_amount", "tr_remark"),
        )}),
    )
