import pytest
from fastapi.testclient import TestClient
from app.main import app
import os
from dotenv import load_dotenv

load_dotenv() 

test_client = TestClient(app)

# Parameters for testing to ensure easy changes and so
test_params = {
        "user_id": 5463726,
        "product_id": 3,
        "quantity": 5
    }

# Test root path
def test_root():
    """Tests the root directory, if this fails the api has errors"""
    resp = test_client.get('/')
    assert resp.status_code == 200
    assert resp.json() == {"message": "Cart Service is running with hardcoded beer data!"}

# POST Test, add items to cart
def test_add_item():
    """Test for adding item to cart"""

    resp = test_client.post(
        "/cart/",
        params={
            "user_id": test_params["user_id"],
            "product_id": test_params["product_id"],
            "quantity": test_params["quantity"]
        },
        headers={
            "token": os.getenv('TOKEN')
        },   
    )

    # Check if status code is ok
    print(resp.text)
    assert resp.status_code == 200
    print("here : ", resp.json())
    assert resp.json() == {"message": "Item added to cart", "cart_item":{"user_id":test_params["user_id"],"quantity":test_params["quantity"], "id": resp.json()["cart_item"]["id"], "product_id":test_params["product_id"] }}


# GET Test, get users cart items
def test_get_cart_items():
    """Test for getting users cart items"""
    resp = test_client.get(
        f'/cart/{test_params["user_id"]}',
        headers={
            "token": os.getenv('TOKEN')
        },  
    
    )
    assert resp.status_code == 200

    print(resp.text)

    expected_outcome = {
        "user_id": test_params['user_id'],
        "cart": [
            {
                "product_id": test_params["product_id"],
                "product_name": "Dark Stout",
                "price": 7.29,
                "quantity": test_params["quantity"],
                "total_price": 7.29 * test_params["quantity"]
            }
        ]
    }
    assert resp.json() == expected_outcome

# DELETE Test, individual items
def test_delete_item():
    """Test for deleting individual item"""
    resp = test_client.delete(
        f'/cart/{test_params["user_id"]}/{test_params["product_id"]}',
        headers={
            "token": os.getenv('TOKEN')
        }
    )
    print(resp.text)
    assert resp.status_code == 200
    expected_outcome = {"message": "Item removed from cart"}

    assert resp.json() == expected_outcome


# DELETE Test, empty cart
def test_empty_cart():
    """Test for emptying the entire cart"""
    resp = test_client.delete(
        f'/cart/{test_params['user_id']}',
        headers={
            "token": os.getenv('TOKEN')
        }
    )
    print(resp.text)
    assert resp.status_code == 200
    data = resp.json()
    assert data["message"] == "Cart cleared"
    resp = test_client.get(
        f'/cart/{test_params["user_id"]}',
        headers={
            "token": os.getenv('TOKEN')
        }
    )
    # Check that the cart is truly empty
    assert resp.status_code == 200
    assert resp.json() == {"message": "Cart is empty"}