from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import requests  # For fetching product data from an external API
from app.database import SessionLocal, CartItem
from app.auth import verify_jwt_token  # Import the verify_jwt_token function

app = FastAPI()

# External API URL 
# PRODUCT_API_URL = Pruttupong's API URL

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Add Item to Cart 
@app.post("/cart/", dependencies=[Depends(verify_jwt_token)])
def add_to_cart(user_id: int, product_id: int, quantity: int = 1, db: Session = Depends(get_db)):

    # Check if the product is already in the cart
    cart_item = db.query(CartItem).filter(CartItem.user_id == user_id, CartItem.product_id == product_id).first()

    if cart_item:
        raise HTTPException(status_code=400, detail="Item already in cart. To update quantity use appropriate endpoint.")
    else:
        cart_item = CartItem(user_id=user_id, product_id=product_id, quantity=quantity)
        db.add(cart_item)

    db.commit()
    db.refresh(cart_item)
    return {"message": "Item added to cart", "cart_item": cart_item}

# Edit the quantity of a specific items
@app.patch("/cart/{user_id}/{product_id}/{quantity}", dependencies=[Depends(verify_jwt_token)])
def edit_item_quantity(user_id: int, product_id: int, quantity_change: int, db: Session = Depends(get_db)):
    """quantity_change, the amount the quantity changes +/-, e.g. if quantity if 10, quantity is change 3, new quantity is 13, if the change is negative (-3), then 7"""
    cart_item = db.query(CartItem).filter(CartItem.user_id == user_id, CartItem.product_id == product_id).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Item not found in cart")

    cart_item.quantity += quantity_change

    if cart_item.quantity <= 0:
        raise HTTPException(status_code=405, detail="Quantity cannot be under 0. If you want to go under zero/removed, use delete method instead.")

    db.commit()
    db.refresh(cart_item)

    return {"message": "Item quantity updated", "cart_item": cart_item}

# Get User's Cart 
@app.get("/cart/{user_id}", dependencies=[Depends(verify_jwt_token)])
def get_cart(user_id: int, db: Session = Depends(get_db)):
    cart_items = db.query(CartItem).filter(CartItem.user_id == user_id).all()
    
    if not cart_items:
        return {"message": "Cart is empty"}

    cart_response = []
    for item in cart_items:
        # Get product details from db data
        
        cart_response.append({
            "product_id": item.product_id,
            "quantity": item.quantity,
        })

    return {"user_id": user_id, "cart": cart_response}

# Remove Item from Cart
@app.delete("/cart/{user_id}/{product_id}", dependencies=[Depends(verify_jwt_token)])
def remove_from_cart(user_id: int, product_id: int, db: Session = Depends(get_db)):
    cart_item = db.query(CartItem).filter(CartItem.user_id == user_id, CartItem.product_id == product_id).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Item not found in cart")

    db.delete(cart_item)
    db.commit()
    return {"message": "Item removed from cart"}

# Clear Cart (On Checkout)
@app.delete("/cart/{user_id}", dependencies=[Depends(verify_jwt_token)])
def clear_cart(user_id: int, db: Session = Depends(get_db)):
    db.query(CartItem).filter(CartItem.user_id == user_id).delete()
    db.commit()
    return {"message": "Cart cleared"}

# Root API check
@app.get("/")
def root():
    return {"message": "Cart Service is running with hardcoded beer data!"}