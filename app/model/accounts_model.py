from django.db import models
from django.core import validators
from django.utils.timezone import now
from datetime import datetime as dt


ACCOUNT_CHOICES = (
    ('DF', 'DF'),
    ('DS', 'DS'),
    ('FD', 'FD'),
    ('MT', 'MT'),
    ('SM', 'SM'),
    ('SS', 'SS'),
    ('ST', 'ST'),
)

LOAN_PERIODS = (
    ("days", "Day (s)"),
    ("months", "Month (s)"),
    ("years", "Year (s)"),
)

DOCUMENTS_TYPE = (
    ('0', "Stamp"),
    ('1', "Blank Cheque"),
    ('2', "Aadhaar Card"),
    ('3', "PAN Card"),
    ('4', "Driving License"),
    ('5', "Voter ID Card"),
    ('6', "Others"),
)


ACCOUNT_STATUS = (
    (0, 'Active'),
    (1, 'Closed'),
)


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    if instance.pk is not None:
        return 'user_{0}/{1}'.format(instance.pk, filename)
    return 'temp/{}_{}'.format(int(dt.timestamp(now())), filename)


# Create your model here.
class Accounts(models.Model):
    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'

    particular_name = models.CharField(verbose_name=u"Particular Name", max_length=256, blank=False, null=True,
                                       help_text="Account Particular Name")
    particular_father_husband_name = models.CharField(verbose_name=u"Father/Husband Name", max_length=256, null=True,
                                                      blank=False, help_text="Particular's Father/Husband Name")
    particular_caste = models.CharField(verbose_name=u"Caste", max_length=128, blank=True, null=True,
                             help_text="Particular's Caste")

    office_contact = models.CharField(verbose_name=u"Office Contact", max_length=20, blank=False, null=True,
                                      help_text="Office Contact Number", validators=[validators.integer_validator])
    home_contact = models.CharField(verbose_name=u"Home Contact", max_length=20, blank=True, null=True,
                                    help_text="Home Contact Number", validators=[validators.integer_validator])

    image = models.ImageField(verbose_name=u"Particular Picture", null=True, blank=True,
                              validators=[validators.FileExtensionValidator(allowed_extensions=["png", "jpg", "jpeg"])],
                              help_text="Photograph of Particular", upload_to=user_directory_path)

    particular_addr1 = models.TextField(verbose_name=u"Correspondence Address", blank=False, null=True,
                                        help_text="Correspondence Address of Particular")

    particular_addr2 = models.TextField(verbose_name=u"Permanent Address", blank=True, null=True,
                                        help_text="Permanent Address of Particular. Leave Empty if same as Correspondence Address.")
    # Guaranteer Details
    guaranteer_name = models.CharField(verbose_name=u"Guaranteer Name", max_length=256, blank=False, null=True,
                                       help_text="Account Guaranteer Name")
    guaranteer_father_husband_name = models.CharField(verbose_name=u"Father/Husband Name", max_length=256, null=True,
                                                      blank=False, help_text="Guaranteer's Father/Husband Name")
    guaranteer_caste = models.CharField(verbose_name=u"Caste", max_length=128, null=True, blank=True,
                             help_text="Guaranteer's Caste")

    guaranteer_office_contact = models.CharField(verbose_name=u"Office Contact", max_length=20, blank=False, null=True,
                                      help_text="Office Contact Number", validators=[validators.integer_validator])
    guaranteer_home_contact = models.CharField(verbose_name=u"Home Contact", max_length=20, blank=True, null=True,
                                    help_text="Home Contact Number", validators=[validators.integer_validator])

    guaranteer_addr1 = models.TextField(verbose_name=u"Correspondence Address", blank=False, null=True,
                                        help_text="Correspondence Address of Particular")

    guaranteer_addr2 = models.TextField(verbose_name=u"Permanent Address", blank=True, null=True,
                                        help_text="Permanent Address of Particular. Leave Empty if same as Correspondence Address.")

    # Loan Details
    loan_type = models.CharField(verbose_name=u"Loan Type", max_length=4, choices=ACCOUNT_CHOICES, null=True,
                                 help_text="Loan Account Type", blank=False, default="DF")
    loan_amount = models.BigIntegerField(verbose_name=u"Loan Amount", blank=False, null=True,
                                         validators=[validators.integer_validator],
                                         help_text="Amount of Loan")
    loan_rate = models.FloatField(verbose_name=u"Interest Rate (in %)", blank=False, null=True,
                                  validators=[validators.MaxValueValidator(100.0), validators.MinValueValidator(0.0)],
                                  help_text="Interest Rate of Loan (in %). Applied Monthly basis.")

    loan_duration = models.BigIntegerField(verbose_name=u"Loan Period", blank=False, null=True,
                                           validators=[validators.integer_validator],
                                           help_text="Period of Loan")
    loan_duration_type = models.CharField(verbose_name=u"Loan Period Type", max_length=8, blank=False, null=True,
                                          help_text="Loan Period Type", choices=LOAN_PERIODS, default="days")

    advance_amount = models.BigIntegerField(verbose_name=u"Advance Amount", blank=False, null=True,
                                            validators=[validators.integer_validator], default=0,
                                            help_text="Advance Amount of Loan")

    documents_submitted = models.CharField(verbose_name=u"Documents Submitted", max_length=5, null=True, blank=True,
                                           help_text="List of Submitted Documents", choices=DOCUMENTS_TYPE)

    loan_created = models.DateTimeField(verbose_name=u"Loan Creation Date", auto_created=True, null=True, default=now)
    account_status = models.IntegerField(verbose_name=u"Status of Account", choices=ACCOUNT_STATUS, default=0,
                                         help_text="Status of Account")
    loan_closed = models.DateTimeField(verbose_name=u"Loan Closing Date", null=True)

    def __str__(self):
        return "%s" % self.particular_name + " /O %s" % self.particular_father_husband_name + \
               " (%s" % self.loan_type + " - %s)" % self.pk

    @staticmethod
    def get_object(ctx=None):
        if not ctx:
            return None

        try:
            t = Accounts.objects.filter(**ctx).first()
            return t
        except:
            return None
