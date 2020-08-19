from django.contrib import admin
from django.contrib.auth.models import Group, User
from app.model.accounts_model import Accounts
from app.modeladmins.accounts_admin import AccountsAdmin

from app.model.transactions_model import AccountSettlement, AccountTransfer, Transactions
from app.modeladmins.transactions_admin import TransactionAdmin
from app.modeladmins.accounts_transfer import AccountTransferAdmin
from app.modeladmins.account_settlement_admin import AccountSettlementAdmin

from app.model.balancesheet_model import BalanceSheet
from app.modeladmins.balancesheet_admin import BalanceSheetAdmin

# Register your model here.
admin.site.register(Accounts, AccountsAdmin)
admin.site.register(Transactions, TransactionAdmin)
admin.site.register(BalanceSheet, BalanceSheetAdmin)
admin.site.register(AccountTransfer, AccountTransferAdmin)
admin.site.register(AccountSettlement, AccountSettlementAdmin)

admin.site.unregister(User)
admin.site.unregister(Group)

admin.site.site_header = 'Cash Book'
admin.site.site_title = "Home"
admin.site.index_title = "Cash Book"
admin.site.index_template = 'admin/index.html'
admin.site.site_url = None
