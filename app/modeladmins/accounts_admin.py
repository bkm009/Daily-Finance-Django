from django.contrib import admin
from django.forms import Textarea
from django.db import models
from django.utils.html import mark_safe
from app.modelforms.account_form import AccountForm


class AccountsAdmin(admin.ModelAdmin):
    form = AccountForm
    fieldsets = (
        ("Personal Information", {'fields': (
            ('particular_name', 'image'),
            ('particular_father_husband_name', 'particular_caste'),
            ('office_contact', 'home_contact'),
            ('particular_addr1', 'particular_addr2'),
        )}),

        ("Guaranteer Information", {'fields': (
            ('guaranteer_name', ),
            ('guaranteer_father_husband_name', 'guaranteer_caste'),
            ('guaranteer_office_contact', 'guaranteer_home_contact'),
            ('guaranteer_addr1', 'guaranteer_addr2'),
        )}),

        ("Loan Information", {'fields': (
            ('loan_type', 'loan_amount', 'loan_rate'),
            ('loan_duration', 'loan_duration_type', 'advance_amount'),
            ('loan_created', 'documents_submitted'),
            ('account_status', 'loan_closed'),
        )})
    )

    def get_form(self, request, obj=None, **kwargs):
        if not obj:
            self.exclude = ('loan_closed', )

        form = super(AccountsAdmin, self).get_form(request, obj, **kwargs)
        return form

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        if obj and obj.account_status == 1:
            return False
        return True

    def account(self, request):
        return str(request.loan_type) + " - " + str(request.pk)
    account.short_description = 'Account'

    def loan_duration_list(self, request):
        return str(request.loan_duration) + " " + str(request.loan_duration_type)
    loan_duration_list.short_description = 'Duration'

    def make_txn(self, request):
        link = '/admin/app/transactions/add/?apk=%s' % str(request.pk)
        return mark_safe("<b><a href='%s'>" % link + "Make Txn</a></b>")

    make_txn.short_description = ""
    make_txn.allow_tags = True

    def view_txn(self, request):
        link = '/admin/app/balancesheet/?account__pk=%s' % str(request.pk)
        return mark_safe("<b><a href='%s'>" % link + "View Balance Sheet</a></b>")

    view_txn.short_description = ""
    view_txn.allow_tags = True

    list_display = ("account", "particular_name", "particular_father_husband_name", "loan_amount", "loan_duration_list",
                    "loan_created", "make_txn", "view_txn", )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 8, 'cols': 40, 'style': 'resize:none;'})},
    }

    ordering = ["loan_created"]
    readonly_fields = ["loan_created", "loan_closed"]
    search_fields = ['particular_name', 'office_contact', 'home_contact']
    list_filter = ['loan_type']

