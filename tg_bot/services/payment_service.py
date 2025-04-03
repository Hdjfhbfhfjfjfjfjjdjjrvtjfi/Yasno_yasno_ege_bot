__all__ = ["PaymentService"]
from yookassa.payment import Payment, PaymentResponse


class PaymentService:
    _PAYMENT_SUCCEED_STATUS = "succeeded"
    _payment: PaymentResponse

    def __init__(self, payment: PaymentResponse):
        self._payment = payment

    def __str__(self):
        return self._payment.json()

    @property
    def payment_url(self) -> str:
        return self._payment.confirmation.confirmation_url

    @property
    def is_succeed(self) -> bool:
        return self._payment.status == self._PAYMENT_SUCCEED_STATUS

    @property
    def payment_id(self) -> str:
        return self._payment.id

    @property
    def label(self) -> str:
        return self._payment.metadata['label']

    @classmethod
    def create_payment(cls, price: int, label: str, bot_link: str) -> "PaymentService":
        return cls(Payment.create({
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
        }))

    @classmethod
    def get_payment_by_id(cls, payment_id: str) -> "PaymentService":
        return PaymentService(Payment.find_one(payment_id))
