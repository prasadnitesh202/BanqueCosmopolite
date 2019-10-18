
def hasMinbalance(acc_model, amount):
    acc = Account.objects.get(pk=acc_model)
    acctype = acc.acc_type
    accamount = acc.acc_balance
    minBal = AccountType.objects.get(pk=acctype).minbal_type
    if accamount - amount >= minBal:
        return True
    else:
        return False


def updatesenderbal(acc_model, amount):
    acc = Account.objects.get(pk=acc_model)
    acc.acc_balance = acc.acc_balance - amount
    acc.save()


def updatereceiverbal(acc_model, amount):
    acc = Account.objects.get(pk=acc_model)
    acc.acc_balance = acc.acc_balance + amount
    acc.save()
