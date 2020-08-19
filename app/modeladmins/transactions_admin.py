from django.contrib.admin import ModelAdmin
from app.modelforms.transaction_form import TransactionForm
from django.utils.html import mark_safe
from rangefilter.filter import DateRangeFilter


class TransactionAdmin(ModelAdmin):

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_form(self, request, obj=None, **kwargs):
        self.form.apk = None

        if request and request.GET and request.GET.get("apk", None):
            self.form.apk = request.GET.get("apk", None)
        form = super(TransactionAdmin, self).get_form(request, obj, **kwargs)
        return form

    form = TransactionForm
    readonly_fields = ["txn_date", "total_profit"]
    fieldsets = (
        ("Transaction Details", {'fields': (
            "account",
            "amount",
            "txn_type",
            "txn_reason",
            "total_profit",
        )}),
    )

    def show_account(self, request):
        try:
            qs = request.account.get_queryset()
            if len(qs) == 1:
                link = '/admin/app/accounts/%s/change/' % str(qs[0].pk)
                return mark_safe("<b><a href='%s'>" % link + "%s</a></b>" % str(qs[0]))
            return "self"
        except:
            return "error occurred"
    show_account.short_description = "Account"
    show_account.allow_tags = True

    def txn_id(self, request):
        return str(request)
    txn_id.short_description = "Txn ID"

    list_display = ["txn_id", "show_account", "amount", "txn_type", "txn_date"]
    list_filter = (
        "txn_type",
        ("txn_date", DateRangeFilter),
    )
    ordering = ["txn_date"]
