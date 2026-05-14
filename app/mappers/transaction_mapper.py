from app.dto.transaction_dto import TransactionOut
from app.models.transaction import Transaction


def transaction_to_out(transaction: Transaction) -> TransactionOut:
    return TransactionOut.model_validate(transaction)
