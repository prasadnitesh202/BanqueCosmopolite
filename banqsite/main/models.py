from django.db import models
from random import randint
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .helpers import *


class Branch(models.Model):
    branch_id = models.AutoField(primary_key=True)
    br_abbr = models.CharField(max_length=3, unique=True)
    br_addr = models.TextField()
    br_city = models.CharField(max_length=50)
    latitude = models.DecimalField(max_digits=9, decimal_places=5)
    longitude = models.DecimalField(max_digits=9, decimal_places=5)
    br_email = models.EmailField()
    br_phone = models.CharField(max_length=10)

    class Meta:
        unique_together = ('latitude', 'longitude')

    def __str__(self):
        return str(self.br_abbr)


"""
br_abbr is branch abbreviation, unique letter code
"""


class AccountType(models.Model):
    acc_types = (
        ('CA', 'Current Account'),
        ('SA', 'Savings Account'),
        ('RD', 'Reccuring Deposit'),
        ('FD', 'Fixed Deposit'),
        ('ZB', 'Zero Balance')
    )
    acc_type = models.CharField(
        primary_key=True, max_length=2, choices=acc_types
        )

    ca_min, sa_min, rd_min, fd_min, zb_min = 0, 1, 2, 3, 4
    minbal_types = (
        (ca_min, 'CA_min'),
        (sa_min, 'SA_min'),
        (rd_min, 'RD_min'),
        (fd_min, 'FD_min'),
        (zb_min, 'ZB_min')
    )
    minbal_type = models.IntegerField(unique=True, choices=minbal_types)

    ca_roi, sa_roi, rd_roi, fd_roi, zb_roi = 0, 1, 2, 3, 4
    roi_types = (
        (ca_roi, 'CA_roi'),
        (sa_roi, 'SA_roi'),
        (rd_roi, 'RD_roi'),
        (fd_roi, 'FD_roi'),
        (zb_roi, 'ZB_roi')
    )
    roi_type = models.DecimalField(
        unique=True, max_digits=5, decimal_places=2, choices=roi_types
        )

    def __str__(self):
        return str(self.acc_type)


class BankUser(models.Model):
    userid = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    u_phone = models.CharField(max_length=10)
    birth_date = models.DateField()
    credit_score = models.IntegerField()

    
    def __str__(self):
        return str(self.user)



# class BankUser(models.Model):
#     user_id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=100)
#     email = models.CharField(max_length=100)
#     password = models.CharField(max_length=100)
#     phone = models.IntegerField()
#     acc_no = models.ForeignKey(Account, on_delete=models.CASCADE)
#     dob = models.DateField('Date of Birth', default=datetime.now)

#     def __str__(self):
#         return str(self.name)


class Account(models.Model):
    acc_no = models.AutoField(primary_key=True)
    mother_branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    acc_type = models.ForeignKey(AccountType, on_delete=models.CASCADE)
    acc_balance = models.BigIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    user_id = models.ForeignKey(BankUser, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.acc_no)

    def save(self):
        if not self.acc_no:
            is_unique = False
            while not is_unique:
                acc_no = randint(10000000000, 99999999999)  # 11 digits
                is_unique = (Account.objects.filter(
                    acc_no=acc_no).count() == 0)
            self.acc_no = acc_no
        super(Account, self).save()


class Card(models.Model):

    card_types = (
        ('C', 'Credit'),
        ('D', 'Debit'),
        )

    card_id = models.AutoField(primary_key=True)
    acc_no = models.ForeignKey(Account, on_delete=models.CASCADE)
    card_no = models.IntegerField()
    card_type = models.CharField(max_length=1, choices=card_types)
    valid_from = models.DateField(default=datetime.now)
    valid_thru = models.DateField()
    cvv = models.CharField(max_length=3)
    img=models.ImageField(upload_to='images/',default='/images/download.jpg')

    class Meta:
        unique_together = ('card_type', 'acc_no')

    def __str__(self):
        return str(self.card_id)


class Atm(models.Model):
    atm_id = models.AutoField(primary_key=True)
    atm_city = models.CharField(max_length=50)
    atm_addr = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=5)
    longitude = models.DecimalField(max_digits=9, decimal_places=5)

    class Meta:
        unique_together = ('latitude', 'longitude')

    def __str__(self):
        return str(self.atm_id)


class Loan(models.Model):
    loan_id = models.AutoField(primary_key=True)
    acc_no = models.ForeignKey(Account, on_delete=models.CASCADE)
    branch_id = models.ForeignKey(Branch, on_delete=models.CASCADE)
    amount = models.BigIntegerField()
    interest = models.DecimalField(max_digits=5, decimal_places=2)
    num_installments = models.IntegerField()
    amount_paid = models.BigIntegerField()
    installments_paid = models.IntegerField()
    loan_cleared = models.BooleanField(default=False)

    def __str__(self):
        return str(self.loan_id)


class Transaction(models.Model):
    txn_types = ( ('A', 'Paid by Credit Card'), ('B', 'Paid by Debit Card'), ('C', 'Cash Transfer'))
    transaction_id = models.AutoField(primary_key=True)
    date_time = models.DateTimeField(default=datetime.now())
    paid_from = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='paid_from')
    paid_to = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='paid_to')
    amount = models.BigIntegerField()
    txn_type = models.CharField(max_length=1, choices=txn_types)
    about_txn = models.TextField()

    def save(self):
        paid_fromacc = self.paid_from
        paid_toacc = self.paid_to
        acc = paid_fromacc
        acctype = acc.acc_type
        accamount = acc.acc_balance
        minBal = AccountType.objects.get(pk=acctype).minbal_type
        if accamount - self.amount >= minBal:
            paid_fromacc.acc_balance = paid_fromacc.acc_balance - self.amount
            paid_fromacc.save()
            paid_toacc.acc_balance = paid_toacc.acc_balance + self.amount
            paid_toacc.save()
        else:
            print('raise validation error in form')
        super(Transaction, self).save()

    def __str__(self):
        return str(self.transaction_id)