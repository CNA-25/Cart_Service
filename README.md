# FastAPI Cart Service

This is a simple FastAPI-based cart service that allows users to manage their shopping cart. The service uses SQLAlchemy for database interactions and includes endpoints for adding, retrieving, and removing items from the cart.

## Features

- Retrieve a list of available beers
- Retrieve details of a specific beer
- Add items to the cart
- Retrieve items in the user's cart
- Remove items from the cart
- Clear the cart

## Requirements

- Python 3.10
- FastAPI
- SQLAlchemy
- Pydantic
- Requests
- PostgreSQL

## Setup

1. Clone the repository:

    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Create and activate a virtual environment:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:

    ```sh
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the root directory with the following content:

    ```env
    MODE=development
    
    DBNAME='db_name'

    DBPW='db_password'

    DBUSER='db_user'
    ```

5. Run the FastAPI application:

    ```sh
    uvicorn app.main:app --reload
    ```

## Running Locally

To run the FastAPI application locally, follow these steps:

1. Ensure that PostgreSQL is installed and running on your local machine.
2. Update the `DATABASE_URL` in the `.env` file with your local PostgreSQL credentials.
3. Start the FastAPI application:

    ```sh
    uvicorn app.main:app --reload
    ```

4. Open your browser and navigate to `http://127.0.0.1:8000` to access the application.
5. You can also access the automatically generated API documentation at `http://127.0.0.1:8000/docs`.

## Endpoints

The API endpoints can also be viewed and tested using the automatically generated API documentation at `http://127.0.0.1:8000/docs`. or if you want to veiw live you can ask us for the link.

### Get All Beers

- **URL:** `/beers/`
- **Method:** `GET`
- **Description:** Retrieve a list of all available beers.

### Get a Specific Beer by ID

- **URL:** `/beers/{beer_id}`
- **Method:** `GET`
- **Description:** Retrieve details of a specific beer by its ID.

### Add Item to Cart

- **URL:** `/cart/`
- **Method:** `POST`
- **Description:** Add an item to the user's cart.
- **Parameters:**
  - __user_id__(int): The ID of the user.
  - __product_id__ (int): The ID of the product to add.
  - __quantity__ (int, optional): The quantity of the product to add (default is 1).

### Get User's Cart

- **URL:** `/cart/{user_id}`
- **Method:** `GET`
- **Description:** Retrieve the items in the user's cart.

### Remove Item from Cart

- **URL:** `/cart/{user_id}/{product_id}`
- **Method:** `DELETE`
- **Description:** Remove an item from the user's cart.

### Clear Cart (On Checkout)

- **URL:** `/cart/{user_id}`
- **Method:** `DELETE`
- **Description:** Clear all items from the user's cart.

## Database

The database schema includes a single table [cart_items](./app/database.py) with the following columns:

- __id__ (Integer, Primary Key): The unique identifier for the cart item.
- __user_id__ (Integer): The ID of the user associated with the cart item.
- __product_id__ (Integer): The ID of the product associated with the cart item.
- __quantity__ (Integer): The quantity of the product in the cart.

