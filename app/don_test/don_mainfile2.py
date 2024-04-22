#Import db from main app file
from flask import request
from don_app import app, db
from don_mainfile import Cart 

@app.route('/add-to-cart/<int:product-id>', methods = ['POST'])
def add_to_cart(product_id):
    return 'Product added to cart'
    #Logic to add a product to the cart

@app.route('/add-to-cart/<int:product-id>', methods = ['POST'])
def renove_from_cart(product_id):
    return 'Product removed from cart'
    #Logic to remove a product from the cart

@app.route('/add-to-cart/<int:product-id>', methods = ['POST'])
def update_cart(product_id):
    new_quantity = request.form.get('quantity')
    return 'Cart updated'
    #Logic to update the quantity of a product in the cart 

@app.route('/view-cart', methods = ['GET'])
def view_cart():
    return 'Displaying cart items'
    #Logic to retrieve and display cart items

