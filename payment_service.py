import stripe
from config import settings

stripe.api_key = settings.stripe_secret_key

def create_payment_intent(amount: float, booking_id: int):
    """Create a Stripe payment intent for booking payment"""
    try:
        intent = stripe.PaymentIntent.create(
            amount=int(amount * 100),  # Convert to cents
            currency="usd",
            metadata={
                "booking_id": booking_id,
                "studio": "GLOSS x GIGGLES"
            }
        )
        return {
            "client_secret": intent.client_secret,
            "payment_intent_id": intent.id,
            "amount": amount
        }
    except stripe.error.StripeError as e:
        raise Exception(f"Payment error: {str(e)}")

def confirm_payment(payment_intent_id: str):
    """Confirm payment intent"""
    try:
        intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        return {
            "status": intent.status,
            "amount": intent.amount / 100,
            "payment_intent_id": intent.id
        }
    except stripe.error.StripeError as e:
        raise Exception(f"Payment confirmation error: {str(e)}")
