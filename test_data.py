from app import app, db
from app.models import User, Post, Product, SuperCat, SubCat, Cart, Collect, Orders, OrdersDetail, Author, News, Shop
from datetime import datetime
from datetime import date

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
    supercat1 = SuperCat(cat_name='手機產品')
    supercat2 = SuperCat(cat_name='電腦產品')
    supercat3 = SuperCat(cat_name='家電產品')
    supercat4 = SuperCat(cat_name='其他產品')

    subcat1 = SubCat(cat_name='智能手機', super_cat_id=1)
    subcat2 = SubCat(cat_name='手機週邊', super_cat_id=1)

    subcat3 = SubCat(cat_name='平板電腦', super_cat_id=2)
    subcat4 = SubCat(cat_name='筆記型電腦', super_cat_id=2)
    subcat5 = SubCat(cat_name='桌上型電腦', super_cat_id=2)

    subcat6 = SubCat(cat_name='電視', super_cat_id=3)
    subcat7 = SubCat(cat_name='冰箱', super_cat_id=3)
    subcat8 = SubCat(cat_name='洗衣機', super_cat_id=3)

    subcat9 = SubCat(cat_name='其他', super_cat_id=4)
    
    # Create products
    

    from datetime import date

    product1 = Product(name='iPhone 12', price=999.99, description='Apple iPhone 12', image_filename='iphone12.jpg', supercat_id=1, subcat_id=1 , addtime='2022-10-31')
    product2 = Product(name='Samsung Galaxy S21', price=899.99, description='Samsung Galaxy S21', image_filename='s21.jpg', supercat_id=1, subcat_id=1 , addtime='2022-10-31')
    product3 = Product(name='Apple Watch Series 6', price=399.99, description='Apple Watch Series 6', image_filename='watch6.jpg', supercat_id=1, subcat_id=2 , addtime='2022-10-31')
    product4 = Product(name='Samsung Galaxy Buds Pro', price=199.99, description='Samsung Galaxy Buds Pro', image_filename='budspro.jpg', supercat_id=1, subcat_id=2 , addtime='2022-10-31')
    product5 = Product(name='iPad Pro', price=799.99, description='Apple iPad Pro', image_filename='ipadpro.jpg', supercat_id=2, subcat_id=3 , addtime='2022-10-31')
    product6 = Product(name='MacBook Pro', price=1299.99, description='Apple MacBook Pro', image_filename='macbookpro.jpg', supercat_id=2, subcat_id=4 , addtime='2022-10-31')
    product7 = Product(name='iMac', price=1799.99, description='Apple iMac', image_filename='imac.jpg', supercat_id=2, subcat_id=5 , addtime='2022-10-31')
    product8 = Product(name='Samsung 65" QLED TV', price=1499.99, description='Samsung 65" QLED TV', image_filename='qledtv.jpg', supercat_id=3, subcat_id=6 , addtime='2022-10-31')
    product9 = Product(name='LG 55" OLED TV', price=1299.99, description='LG 55" OLED TV', image_filename='oledtv.jpg', supercat_id=3, subcat_id=6 , addtime='2022-10-31')
    product10 = Product(name='冰箱', price=1999.99, description='冰箱', image_filename='fridge.jpg', supercat_id=3, subcat_id=7 , addtime='2022-10-31')
    product11 = Product(name='洗衣機', price=999.99, description='洗衣機', image_filename='washer.jpg', supercat_id=3, subcat_id=8 , addtime='2022-10-31')
    product12 = Product(name='其他產品', price=99.99, description='其他產品', image_filename='other.jpg', supercat_id=4, subcat_id=9 , addtime='2022-10-31')

            
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
    news1 = News(title='News One', content='Content of News One', author_id=author1.id , image_filename='news1.jpg' , addtime=datetime.now() , author=author1 ,product_id=1)
    news2 = News(title='News Two', content='Content of News Two', author_id=author2.id, image_filename='news2.jpg', addtime=datetime.now() , author=author2 )

    # Add to session and commit
    db.session.add_all([user1, user2, post1, post2, supercat1, supercat2, supercat3, supercat4, subcat1, subcat2, subcat3, subcat4, subcat5, subcat6, subcat7, subcat8, subcat9, product1, product2, product3, product4, product5, product6, product7, product8, product9, product10, product11, product12, cart1, order1, order_detail1, shop1, author1, author2, news1, news2])
    db.session.commit()

    print('Test data added.')

if __name__ == '__main__':
    add_test_data()