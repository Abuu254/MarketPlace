import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import random
from datetime import datetime
from app import db
from app.models import User, Product, Category, Image, Address
from config import Config
from flask import Flask

# Create an instance of the Flask application
app = Flask(__name__)
app.config.from_object(Config)

# Bind the app with the SQLAlchemy service
db.init_app(app)

# Create tables within an application context
with app.app_context():
    db.create_all()

# Replace 'your_database_uri' with your actual database URI
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

# Function to generate a random date in October and November 2023
def random_date():
    month = random.choice([10, 11])  # October or November
    day = random.randint(1, 30 if month == 11 else 31)  # Day of the month
    return datetime(2023, month, day)

def add_or_get_address(street):
    full_address = {'Street': street, 'City': 'New Haven', 'State': 'CT', 'ZipCode': '06511', 'Country': 'USA'}
    address = session.query(Address).filter_by(Street=full_address['Street']).first()
    if not address:
        address = Address(UserID=admin_user.UserID, **full_address)
        session.add(address)
        session.commit()
    return address


# Read CSV file
df = pd.read_csv('cleaned_data.csv')

# Ensure 'Yale Marketplace Admin' exists
admin_user = session.query(User).filter_by(FirstName='Yale', LastName='Marketplace Admin').first()
if not admin_user:
    admin_user = User(FirstName='Yale', LastName='Marketplace Admin', Email='admin@example.com', ProfileImage='path_to_image')
    session.add(admin_user)
    session.commit()

# Define addresses
street_numbers = ['90 Prospect Street', '205 Elm Street', '74 High Street', '248 York St', '302 York St', '89 Elm St', '68 High St', '304 York St', '130 Prospect St', '261 Park St', '242 Elm St', '505 College St', '345 Temple St', '241 Elm St']


print("Starting....")
# Insert data from CSV
for index, row in df.iterrows():
    # Category
    category = session.query(Category).filter_by(CategoryName=row['Category']).first()
    if not category:
        category = Category(CategoryName=row['Category'])
        session.add(category)
        session.commit()

    # Random Address
    selected_street = np.random.choice(street_numbers)
    address = add_or_get_address(selected_street)
    if not address:
        address = Address(UserID=admin_user.UserID, **selected_address)
        session.add(address)
        session.commit()

    # Product
    product = Product(
        ProductID=row['ProductID'],
        SellerID=admin_user.UserID,
        CategoryID=category.CategoryID,
        ProductName=row['ProductTitle'],
        ProductColor=row['Colour'],
        # Description='Some description',  # Add as required
        Price=row['Price'],
        Condition=row['Condition'],
        DatePosted=random_date(),
        IsSold=False
    )
    session.add(product)
    session.commit()

    # Image
    image = Image(ProductID=product.ProductID, ImageURL=row['ImageURL'])
    session.add(image)
    session.commit()

# Close the session
session.close()
print("Done!!!")
