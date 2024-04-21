#Import db from main app file
from don_app import db

#Define the Product model
class Product(db.model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    price = db.Column(db.Float, nullable = False)
    #Add other relevant fields as needed

#Create the databae tables
db.create_all()

#Define the Cart model
class Cart(db.model):
    id = db.Column(db.Integer, primary_key = True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable = False)
quantity = db.Column(db.Integer, default = 1)
#ADDitional fields like user_id can be added for user-specific carts

#Create the database tables
db.create_all()

#Add a relationship in the Product model
class Product(db.Model):
    #Existing fields...
    cart_items = db.relationship('Cart', backref = 'product', lazy = True)

#Modify the Cart model
class Cart(db.model):
    #Existing fields...
    product = db.relationship('Product')

class Cart(db.Model):
    #Existing fields and relationships...
    def add_to_cart(self, product_id):
        return
        #Logic to add a product to the cart

    def renove_from_cart(self, product_id):
        return
        #Logic to remove a product from the cart
    
    def update_quantity(self,new_quantity):
        return
        #Logic to update the quantity of a product in the cart 