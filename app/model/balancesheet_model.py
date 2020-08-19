from app.model.transactions_model import Transactions


class BalanceSheet(Transactions):
    class Meta:
        verbose_name = "BalanceSheet"
        verbose_name_plural = "BalanceSheet"
        proxy = True
