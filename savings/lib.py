from functools import reduce

def get_registration_total(transactions):
    registration_transactions = filter(lambda x: x['transactiontype'] == "REG", transactions)
    registraion_amounts = map(lambda x: float(x['amount']), registration_transactions)
    return reduce(lambda x, y: x + y, registraion_amounts)
