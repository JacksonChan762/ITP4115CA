
from datetime import datetime, timedelta, timezone
from hashlib import md5
from app import app, db, login 
from .config import Config
from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash


followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    orders = db.relationship('Orders', backref='user') 
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def __repr__(self) -> str:
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode("utf-8")).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Post.query.join(
            followers, followers.c.followed_id == Post.user_id
        ).filter(followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({"reset_password": self.id,
                           "exp": datetime.now(tz=timezone.utc) + timedelta(seconds=expires_in)},
                          app.config["SECRET_KEY"], algorithm="HS256")

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config["SECRET_KEY"], algorithms="HS256")[
                "reset_password"]
        except:           
            return None
        return User.query.get(id)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self) -> str:
        return f'<Post {self.body}>'

# 建立一個新的關聯表

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)  
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    image_filename = db.Column(db.String(120), nullable=True) 
    ##
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  
    cart = db.relationship("Cart", backref='product')   
    collect = db.relationship("Collect", backref='poods') # 订单外键关系关联
    orders_detail = db.relationship("OrdersDetail", backref='product')  # 订单外键关系关联
    supercat_id = db.Column(db.Integer, db.ForeignKey('supercat.id'), nullable=False)
    subcat_id = db.Column(db.Integer, db.ForeignKey('subcat.id'), nullable=False)
    inventory = db.relationship("Inventory", backref='product')
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'))


   # 店铺外键关系关联
    
    def __repr__(self):
        return f'<Product {self.name}>'




class SuperCat(db.Model):
    __tablename__ = 'supercat'
    id = db.Column(db.Integer, primary_key=True)
    cat_name = db.Column(db.String(100), nullable=False)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    subcats = db.relationship("SubCat", backref='supercat', lazy='dynamic')
    products = db.relationship("Product", backref='supercat', lazy='dynamic')

    def __repr__(self):
        return f"<SuperCat {self.cat_name}>"

# Sub Category Model
class SubCat(db.Model):
    __tablename__ = 'subcat'
    id = db.Column(db.Integer, primary_key=True)
    cat_name = db.Column(db.String(100), nullable=False)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    super_cat_id = db.Column(db.Integer, db.ForeignKey('supercat.id'), nullable=False)
    products = db.relationship("Product", backref='subcat', lazy='dynamic')

    def __repr__(self):
        return f"<SubCat {self.cat_name}>"
    



class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    number = db.Column(db.Integer, default=0)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    addtime = db.Column(db.DateTime, default=datetime.utcnow)
    quantity = db.Column(db.Integer)

    def __repr__(self):
        return "<Cart %r>" % self.id
    

class Collect(db.Model):
    __tablename__ = 'collect'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product = db.relationship('Product', back_populates='collect', overlaps="collect,poods")
    user_id = db.Column(db.Integer)  # 所属用户
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<Collect %r>" % self.id


class Orders(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    user_id = db.Column((db.Integer), db.ForeignKey('user.id')) # 所属用户
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    orders_detail = db.relationship("OrdersDetail", backref='orders')  # 外键关系关联

    def __repr__(self):
        return "<Orders %r>" % self.id


class OrdersDetail(db.Model):
    __tablename__ = 'orders_detail'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))  # 所属商品
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))  # 所属订单
    number = db.Column(db.Integer, default=0)  # 购买数量
    price = db.Column(db.Float, default=0)  # 价格
    order_name = db.Column(db.String(100), nullable=True)  




class Shop(db.Model):
    __tablename__ = 'shop'
    id = db.Column(db.Integer, primary_key=True)  
    name = db.Column(db.String(100), nullable=False) 
    desc = db.Column(db.String(255), nullable=True)  
    tel = db.Column(db.String(11), nullable=True)  
    email = db.Column(db.String(100), nullable=True)  
    address = db.Column(db.String(255), nullable=True)  
    inventory = db.relationship("Inventory", backref='shop')  
    products_id = db.relationship("Product", backref='shop')  
    

    def __repr__(self):
        return f"<Shop {self.id}>"


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    desc = db.Column(db.String(200))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    news = db.relationship('News')
    


class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    addtime = db.Column(db.DateTime, default=datetime.now)
    image_filename = db.Column(db.String(120))
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    author = db.relationship('Author', backref='news_items')

class Inventory(db.Model):
    __tablename__ = 'inventory'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'), nullable=False)  # 新增的字段
    quantity = db.Column(db.Integer, nullable=False)
