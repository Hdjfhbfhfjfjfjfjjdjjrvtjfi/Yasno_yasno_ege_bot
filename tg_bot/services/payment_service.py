__all__ = ["PaymentService"]
from typing import ClassVar, Any

from yookassa.payment import Payment, PaymentResponse


class PaymentService:
    """Service class for handling YooKassa payments.
    
    This class provides methods to create, check, and retrieve payment information
    from the YooKassa payment system. It encapsulates the payment logic and
    provides a clean interface for payment operations.

    :cvar _PAYMENT_SUCCEED_STATUS: Status indicating successful payment
    :ivar _payment: Payment object from YooKassa
    """
    
    _PAYMENT_SUCCEED_STATUS: ClassVar[str] = "succeeded"

    def __init__(self, payment: PaymentResponse) -> None:
        """Initialize the payment service with a YooKassa payment object.
        
        :param payment: A PaymentResponse object from YooKassa
        :return: None
        """
        self._payment: PaymentResponse = payment

    def __str__(self) -> str:
        """Return the payment information as a JSON string.
        
        :return: JSON representation of the payment
        """
        return self._payment.json()

    @property
    def payment_url(self) -> str:
        """Get the payment URL for redirecting the user to payment page.
        
        :return: URL for payment confirmation
        """
        return self._payment.confirmation.confirmation_url

    @property
    def is_succeed(self) -> bool:
        """Check if the payment was successful.
        
        :return: True if payment succeeded, False otherwise
        """
        return self._payment.status == self._PAYMENT_SUCCEED_STATUS

    @property
    def payment_id(self) -> str:
        """Get the unique identifier of the payment.
        
        :return: Payment ID
        """
        return self._payment.id

    @property
    def label(self) -> str:
        """Get the payment label from metadata.
        
        :return: Payment label stored in metadata
        """
        return self._payment.metadata['label']

    @classmethod
    def create_payment(cls, price: int, label: str, bot_link: str) -> "PaymentService":
        """Create a new payment in YooKassa.
        
        :param price: Payment amount in rubles
        :param label: Payment label for identification
        :param bot_link: Return URL after payment completion
        :return: New payment service instance with created payment
        """
        payment_data: dict[str, Any] = {
            "amount": {
                "value": price,
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": bot_link
            },
            "capture": True,
            "description": "Оплата услуги",
            "metadata": {
                "label": label
            },
        }
        return cls(Payment.create(payment_data))

    @classmethod
    def get_payment_by_id(cls, payment_id: str) -> "PaymentService":
        """Retrieve a payment by its ID.
        
        :param payment_id: Unique identifier of the payment
        :return: Payment service instance with retrieved payment
        """
        return cls(Payment.find_one(payment_id))
