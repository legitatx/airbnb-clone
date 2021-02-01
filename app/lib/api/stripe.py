import stripe
from os import getenv
from fastapi import HTTPException

stripe.api_key = getenv("STRIPE_SECRET_KEY")


def connect(code: str):
    res = stripe.OAuth.token(grant_type="authorization_code", code=code)
    return res


def charge(amount: int, source: str, stripe_account: str):
    try:
        stripe.Charge.create(
            amount=amount,
            currency="usd",
            source=source,
            application_fee_amount=round(amount * 0.05),
            on_behalf_of=stripe_account,
        )
    except stripe.error.StripeError:
        raise HTTPException(
            status_code=500, detail="Failed to create charge with Stripe"
        )
