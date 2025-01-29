from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
DATABASE_URL = f"postgresql://{os.getenv('DBUSER')}:{os.getenv('DBPW')}@postgresql.cart-service.svc.cluster.local/{os.getenv('DBNAME')}"


# Database Connection
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Cart Item Model
class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)  # Associate cart items with a user
    product_id = Column(Integer, nullable=False)  # Associate with a product
    quantity = Column(Integer, default=1) # Quantity of the product in the cart, duh

# Create Tables if they don’t exist
Base.metadata.create_all(bind=engine)
