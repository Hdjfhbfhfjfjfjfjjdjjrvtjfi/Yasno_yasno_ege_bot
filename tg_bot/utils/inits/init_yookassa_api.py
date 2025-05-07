__all__ = ["init_yookassa_api"]
from yookassa import Configuration


def init_yookassa_api(account_id: str, secret_key: str) -> None:
    """Initialize the YooKassa API with account credentials.

    :param account_id: YooKassa account identifier
    :param secret_key: YooKassa API secret key for authentication
    :return: None
    """
    Configuration.configure(account_id, secret_key)
