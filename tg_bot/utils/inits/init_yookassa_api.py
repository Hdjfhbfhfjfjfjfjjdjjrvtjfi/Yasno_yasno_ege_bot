__all__ = ["init_yookassa_api"]
from yookassa import Configuration


def init_yookassa_api(account_id: str, secret_key: str):
    Configuration.configure(account_id, secret_key)
