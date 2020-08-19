from django.contrib.admin import ModelAdmin
from rangefilter.filter import DateRangeFilter


class BalanceSheetAdmin(ModelAdmin):

    add_url = None
    opening_balance = 0.0
    closing_balance = 0.0

    def changelist_view(self, request, extra_context=None):
        BalanceSheetAdmin.opening_balance = 0.0
        BalanceSheetAdmin.closing_balance = 0.0
        return super(BalanceSheetAdmin, self).changelist_view(request, extra_context)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def txn_id(self, request):
        return str(request)
    txn_id.short_description = "Txn ID"

    def credit_txn(self, request):
        try:
            if request.txn_type == "CR" or request.txn_type == "IN":
                BalanceSheetAdmin.opening_balance = BalanceSheetAdmin.closing_balance
                BalanceSheetAdmin.closing_balance += request.amount
                return str(request.amount)
        except:
            pass
        return "-"
    credit_txn.short_description = "Credit"

    def debit_txn(self, request):
        try:
            if request.txn_type == "DR" or request.txn_type == "PR":
                BalanceSheetAdmin.opening_balance = BalanceSheetAdmin.closing_balance
                BalanceSheetAdmin.closing_balance -= request.amount
                return str(request.amount)
        except:
            pass
        return "-"
    debit_txn.short_description = "Debit"

    def opening(self, request):
        return str(BalanceSheetAdmin.opening_balance)
    opening.short_description = "Opening Balance"

    def closing(self, request):
        return str(BalanceSheetAdmin.closing_balance)
    closing.short_description = "Closing Balance"

    def txn_desc(self, request):
        if request.txn_type == "PR":
            return "Penalty"
        return str(request.txn_reason)
    txn_desc.short_description = "Remark"

    list_display = ("txn_id", "txn_date", "credit_txn", "debit_txn", "txn_desc", "opening", "closing", )
    ordering = ["txn_date"]
    list_filter = (
        "txn_date",
        ("txn_date", DateRangeFilter),
    )
