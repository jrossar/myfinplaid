from .models import Transactions

#transaction_list = Transactions.objects.all()
transaction_list = ''

for t in transaction_list:
    print(t)
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')


def save_transactions(transaction):
    if transaction['transaction_id'] is None:
        transaction['transaction_id'] = 'N/A'
    if transaction['category'] is None:
        transaction['category'] = 'N/A'
    if transaction['name'] is None:
        transaction['name'] = 'N/A'
    if transaction['pending'] is None:
        transaction['pending'] = 'N/A'
    transaction = Transactions(
        transaction_id=transaction['transaction_id'],
        category=transaction['category'],
        name=transaction['name'],
        amount=transaction['amount'],
        pending=transaction['pending'],
        iso_currency_code=transaction['iso_currency_code'],
        account_id=transaction['account_id']
    )
    transaction.save()
