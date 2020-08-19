from django.core.management.base import BaseCommand
from django.utils.timezone import now, datetime, make_aware
from app.model.accounts_model import Accounts
from app.models import InterestTrack
from app.model.transactions_model import Transactions


def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month


class Command(BaseCommand):
    def handle(self, *args, **options):
        account_ids = Transactions.objects.exclude(account__pk=None).values_list('account__pk', flat=True).distinct()
        today = now()
        for each_qs in account_ids:
            account = Accounts.objects.filter(pk=each_qs, account_status=0, loan_type__in=['DS', 'FD', 'SM', 'SS', 'MT'])
            if len(account) == 1:
                total_months = abs(diff_month(today, account[0].loan_created))
                for month in range(1, total_months+1):
                    i_date = datetime(
                        year=account[0].loan_created.year,
                        month=account[0].loan_created.month + month,
                        day=account[0].loan_created.day,
                    )

                    i_date = make_aware(i_date)

                    it = InterestTrack.objects.filter(interest_added=i_date, account=account[0])
                    if len(it) == 0:
                        txn_data = {
                            "amount": max(0.0, account[0].loan_amount * account[0].loan_rate * 0.01),
                            "txn_type": "CR",
                            "txn_reason": "Interest Added.",
                            "txn_date": i_date,
                        }

                        if account[0].loan_type in ["MT"]:
                            txn_data["txn_type"] = "DR"

                        txn = Transactions(**txn_data)
                        txn.pk = None
                        txn.save()
                        txn.account.add(account[0])
                        txn.save()

                        it_data = {
                            "interest_added": i_date,
                        }
                        i_t = InterestTrack(**it_data)
                        i_t.pk = None
                        i_t.save()

                        i_t.account.add(account[0])
                        i_t.save()
