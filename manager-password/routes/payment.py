from fastapi import FastAPI, HTTPException
import stripe
from fastapi import APIRouter, Depends, HTTPException
from dotenv import load_dotenv
import os
import stripe
import database
load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

router = APIRouter()

@router.post("/process-payment")
async def process_payment(amount: int, currency:str):
    try:
        charge = stripe.Charge.create(
            amount = amount,
            currency = currency,
            description = "Payment for service",
            source = "tok_visa",
           
        )


   
        # Return a success response
        return {"status": "success", "charge_id": charge.id}
    except stripe.error.CardError as e:
        return{"status": "error", "message": "Something went wrong. Please try again later."}
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=500, detail=f"Stripe error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Network error: {str(e)}")
if __name__ == "__main__":
    app = FastAPI()
    app.include_router(router, prefix="/payment", tags=["payment"])
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)