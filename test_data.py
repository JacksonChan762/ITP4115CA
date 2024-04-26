from app import app, db
from app.models import User, Post, Product, SuperCat, SubCat, Cart, Collect, Orders, OrdersDetail, Author, News, Shop
from datetime import datetime

app_context = app.app_context()
app_context.push()

def add_test_data():
    # Clear existing data and create new tables
    db.drop_all()
    db.create_all()

    # Create users
    user1 = User(username='user1', email='user1@example.com')
    user1.set_password('password1')
    user2 = User(username='user2', email='user2@example.com')
    user2.set_password('password2')

    # Create posts
    post1 = Post(body='Hello from user1!', user_id=1)
    post2 = Post(body='Hello from user2!', user_id=2)

    # Create product categories
    supercat1 = SuperCat(cat_name='Electronics')
    subcat1 = SubCat(cat_name='Smartphones', super_cat_id=1)

    # Create products
    product1 = Product(name='iPhone 12', price=999.99, description='Latest Apple iPhone', supercat_id=1, subcat_id=1 , image_filename='iphone12.jpg')
    product2 = Product(name='Samsung Galaxy S20', price=899.99, description='Latest Samsung Phone', supercat_id=1, subcat_id=1, image_filename='s20.jpg')

    # Create a cart
    cart1 = Cart(user_id=1, product_id=1, quantity=2)

    # Create orders
    order1 = Orders(user_id=1)
    order_detail1 = OrdersDetail(product_id=1, order_id=1, number=1, price=999.99)

    # Create shop
    shop1 = Shop(desc='Local Computer Store', tel='1234567890', email='info@localstore.com', address='123 Tech Ave')

    # 創建兩個作者
    author1 = Author(name='Author One', desc='Description of Author One', addtime=datetime.now())
    author2 = Author(name='Author Two', desc='Description of Author Two', addtime=datetime.now())

    # 創建兩個新聞
    news1 = News(title='News One', content='Content of News One', author_id=author1.id , image_filename='news1.jpg' , addtime=datetime.now() , author=author1)
    news2 = News(title='News Two', content='Content of News Two', author_id=author2.id, image_filename='news2.jpg', addtime=datetime.now() , author=author2)

    # Add to session and commit
    db.session.add_all([user1, user2, post1, post2, author1, author2, news1, news2, supercat1, subcat1, product1, product2, cart1, order1, order_detail1, shop1 , author1, author2, news1, news2])
    db.session.commit()

    print('Test data added.')

if __name__ == '__main__':
    add_test_data()