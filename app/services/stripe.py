import stripe
import os
from dotenv import load_dotenv

load_dotenv()

stripe.api_key = os.getenv("STRIPE_API_KEY") 

def crear_sesion_pago(cantidad: int, descripcion: str, email_cliente: str):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "clp",
                    "product_data": {
                        "name": descripcion
                    },
                    "unit_amount": cantidad * 100  
                },
                "quantity": 1
            }],
            mode="payment",
            customer_email=email_cliente,
            success_url="https://example.com/success",  
            cancel_url="https://example.com/cancel"
        )
        return session.url
    except Exception as e:
        raise Exception(f"Error al crear sesión de Stripe: {str(e)}")