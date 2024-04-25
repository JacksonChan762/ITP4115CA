from app import db, app
from app.models import User, Post, Product , Cart , Collect , Orders , OrdersDetail , SuperCat , SubCat ,Shop , StoreInventory


app_context = app.app_context()
app_context.push()

# Create some users
user1 = User(username='john', email='john@example.com')
user1.set_password('password')
user2 = User(username='jane', email='jane@example.com')
user2.set_password('password')
db.session.add(user1)
db.session.add(user2)
db.session.commit()

# Create some posts
post1 = Post(body='This is a test post.', user_id=user1.id)
post2 = Post(body='Another test post.', user_id=user2.id)
db.session.add(post1)
db.session.add(post2)
db.session.commit()

# Create some categories
supercat1 = SuperCat(cat_name='Electronics')
supercat2 = SuperCat(cat_name='Clothing')
db.session.add(supercat1)
db.session.add(supercat2)

subcat1 = SubCat(cat_name='Laptops', super_cat_id=supercat1.id)
db.session.add(subcat1)
subcat2 = SubCat(cat_name='Smartphones', super_cat_id=supercat1.id)
subcat3 = SubCat(cat_name='Shirts', super_cat_id=supercat2.id)
subcat4 = SubCat(cat_name='Pants', super_cat_id=supercat2.id)
db.session.add(subcat1)
db.session.add(subcat2)
db.session.add(subcat3)
db.session.add(subcat4)
db.session.commit()

# Create some products
product1 = Product(name='MacBook Pro', price=1999.99, description='A powerful laptop for professionals.', supercat_id=supercat1.id, subcat_id=subcat1.id)
product2 = Product(name='iPhone 12', price=799.99, description='The latest iPhone from Apple.', supercat_id=supercat1.id, subcat_id=subcat2.id)
product3 = Product(name='Polo Shirt', price=29.99, description='A classic polo shirt.', supercat_id=supercat2.id, subcat_id=subcat3.id)
product4 = Product(name='Jeans', price=49.99, description='A pair of stylish jeans.', supercat_id=supercat2.id, subcat_id=subcat4.id)
db.session.add(product1)
db.session.add(product2)
db.session.add(product3)
db.session.add(product4)
db.session.commit()

# Create some carts
cart1 = Cart(user_id=user1.id, product_id=product1.id, quantity=1)
cart2 = Cart(user_id=user2.id, product_id=product3.id, quantity=2)
db.session.add(cart1)
db.session.add(cart2)
db.session.commit()

# Create some collections
collect1 = Collect(product_id=product2.id, user_id=user1.id)
collect2 = Collect(product_id=product4.id, user_id=user2.id)
db.session.add(collect1)
db.session.add(collect2)
db.session.commit()

# Create some orders
order1 = Orders(user_id=user1.id)
order2 = Orders(user_id=user2.id)
db.session.add(order1)
db.session.add(order2)
db.session.commit()

# Create some order details
order_detail1 = OrdersDetail(product_id=product1.id, order_id=order1.id, number=1, price=product1.price, order_name=product1.name)
order_detail2 = OrdersDetail(product_id=product3.id, order_id=order2.id, number=2, price=product3.price, order_name=product3.name)
db.session.add(order_detail1)
db.session.add(order_detail2)
db.session.commit()

# Create some shops
shop1 = Shop(desc='A tech store', tel='1234567890', email='shop1@example.com', address='123 Main St')
shop2 = Shop(desc='A clothing store', tel='0987654321', email='shop2@example.com', address='456 Oak Ave')
db.session.add(shop1)
db.session.add(shop2)
db.session.commit()

# Create some store inventories
store_inventory1 = StoreInventory(product_id=product1.id, number=10, shop_id=shop1.id)
store_inventory2 = StoreInventory(product_id=product2.id, number=20, shop_id=shop1.id)
store_inventory3 = StoreInventory(product_id=product3.id, number=15, shop_id=shop2.id)
store_inventory4 = StoreInventory(product_id=product4.id, number=25, shop_id=shop2.id)
db.session.add(store_inventory1)
db.session.add(store_inventory2)
db.session.add(store_inventory3)
db.session.add(store_inventory4)
db.session.commit()