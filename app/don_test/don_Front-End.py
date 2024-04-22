from flask import app, render_template
from don_mainfile import Cart, Product

@app.route('/products')
def show_products():
    products = Product.query.all()
    return render_template('products.html.j2',products = products)

@app.route('/cart')
def view_cart():
    cart_time = Cart.query.all()
    return render_template('cart.html.j2',cart_items = cart_items) # type: ignore
