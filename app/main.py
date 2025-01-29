from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import requests  # For fetching product data from an external API
from app.database import SessionLocal, CartItem
from app.auth import verify_jwt_token  # Import the verify_jwt_token function

app = FastAPI()

# External API URL 
# PRODUCT_API_URL = Pruttupong's API URL

beers = [
    {"id": 1, "sku": "BEER001", "name": "Golden Ale", "price": 5.99, "description": "A smooth, golden-hued ale with a crisp finish."},
    {"id": 2, "sku": "BEER002", "name": "Hoppy IPA", "price": 6.49, "description": "A bold, hop-forward IPA with citrus and pine notes."},
    {"id": 3, "sku": "BEER003", "name": "Dark Stout", "price": 7.29, "description": "A rich, full-bodied stout with chocolate and coffee flavors."},
    {"id": 4, "sku": "BEER004", "name": "Amber Lager", "price": 5.79, "description": "A smooth amber lager with caramel malt sweetness."},
    {"id": 5, "sku": "BEER005", "name": "Wheat Beer", "price": 6.19, "description": "A refreshing wheat beer with hints of orange and coriander."},
    {"id": 6, "sku": "BEER006", "name": "Pilsner", "price": 5.49, "description": "A light-bodied, crisp pilsner with a clean malt profile."},
    {"id": 7, "sku": "BEER007", "name": "Barrel-Aged Porter", "price": 8.99, "description": "A deep, roasted porter aged in oak barrels for complexity."},
    {"id": 8, "sku": "BEER008", "name": "Sour Ale", "price": 7.99, "description": "A tart, fruity sour ale with raspberry and cherry notes."},
    {"id": 9, "sku": "BEER009", "name": "Double IPA", "price": 8.49, "description": "A high-ABV, intensely hoppy IPA with tropical fruit aroma."},
    {"id": 10, "sku": "BEER010", "name": "Blonde Ale", "price": 5.89, "description": "A crisp and light blonde ale with a smooth finish."}
]

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Get All Beers 
@app.get("/beers/", dependencies=[Depends(verify_jwt_token)])
def get_beers():
    return beers

# Get a Specific Beer by ID
@app.get("/beers/{beer_id}", dependencies=[Depends(verify_jwt_token)])
def get_beer(beer_id: int):
    beer = next((b for b in beers if b["id"] == beer_id), None)
    if beer is None:
        raise HTTPException(status_code=404, detail="Beer not found")
    return beer

# Add Item to Cart 
@app.post("/cart/", dependencies=[Depends(verify_jwt_token)])
def add_to_cart(user_id: int, product_id: int, quantity: int = 1, db: Session = Depends(get_db)):
    # Check if the product exists
    beer = next((b for b in beers if b["id"] == product_id), None)
    if beer is None:
        raise HTTPException(status_code=404, detail="Product not found")

    # Check if the product is already in the cart
    cart_item = db.query(CartItem).filter(CartItem.user_id == user_id, CartItem.product_id == product_id).first()

    if cart_item:
        cart_item.quantity += quantity  # Increase quantity if already in cart
    else:
        cart_item = CartItem(user_id=user_id, product_id=product_id, quantity=quantity)
        db.add(cart_item)

    db.commit()
    db.refresh(cart_item)
    return {"message": "Item added to cart", "cart_item": cart_item}

# Get User's Cart 
@app.get("/cart/{user_id}", dependencies=[Depends(verify_jwt_token)])
def get_cart(user_id: int, db: Session = Depends(get_db)):
    cart_items = db.query(CartItem).filter(CartItem.user_id == user_id).all()
    
    if not cart_items:
        return {"message": "Cart is empty"}

    cart_response = []
    for item in cart_items:
        # Get product details from hardcoded list
        beer = next((b for b in beers if b["id"] == item.product_id), None)
        
        if beer:
            cart_response.append({
                "product_id": item.product_id,
                "product_name": beer["name"],
                "price": beer["price"],
                "quantity": item.quantity,
                "total_price": beer["price"] * item.quantity
            })
        else:
            cart_response.append({
                "product_id": item.product_id,
                "product_name": "Product not found",
                "price": 0.0,
                "quantity": item.quantity,
                "total_price": 0.0
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