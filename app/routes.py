from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g ,flash ,session,jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from flask_babel import _, get_locale
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm, \
    ResetPasswordRequestForm, ResetPasswordForm, OrderForm
from app.models import User, Post, Product , Cart , Collect , Orders , OrdersDetail , SuperCat , SubCat ,Shop , Author , News
from werkzeug.utils import secure_filename
from PIL import Image
import jinja2
import os
import logging
from sqlalchemy import desc


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    g.locale = str(get_locale())


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])

def index():
    product = Product.query.all()
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], '')
    return render_template('index.html.j2' , product=product,image = full_filename)


@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page=page, per_page=app.config["POSTS_PER_PAGE"], error_out=False)
    next_url = url_for(
        'explore', page=posts.next_num) if posts.next_num else None
    prev_url = url_for(
        'explore', page=posts.prev_num) if posts.prev_num else None
    return render_template('index.html.j2', title=_('Explore'),
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(_('Invalid username or password'))
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        # 將 user_id 存入 session
        session['user_id'] = user.id
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html.j2', title=_('Sign In'), form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(_('Congratulations, you are now a registered user!'))
        return redirect(url_for('login'))
    return render_template('register.html.j2', title=_('Register'), form=form)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash(
            _('Check your email for the instructions to reset your password'))
        return redirect(url_for('login'))
    return render_template('reset_password_request.html.j2',
                           title=_('Reset Password'), form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if user is None:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_('Your password has been reset.'))
        return redirect(url_for('login'))
    return render_template('reset_password.html.j2', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.followed_posts().paginate(
        page=page, per_page=app.config["POSTS_PER_PAGE"], error_out=False)
    next_url = url_for(
        'index', page=posts.next_num) if posts.next_num else None
    prev_url = url_for(
        'index', page=posts.prev_num) if posts.prev_num else None
    return render_template('user.html.j2', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html.j2', title=_('Edit Profile'),
                           form=form)


@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username)s not found.', username=username))
        return redirect(url_for('index'))
    if user == current_user:
        flash(_('You cannot follow yourself!'))
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash(_('You are following %(username)s!', username=username))
    return redirect(url_for('user', username=username))

##
@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username)s not found.', username=username))
        return redirect(url_for('index'))
    if user == current_user:
        flash(_('You cannot unfollow yourself!'))
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash(_('You are not following %(username)s.', username=username))
    return redirect(url_for('user', username=username))


@app.template_filter('format_currency')
def format_currency(value):
    if value is None or isinstance(value, jinja2.Undefined):
        return "$0.00"  # 或者可以返回 "N/A"
    try:
        return "${:,.2f}".format(value)
    except (TypeError, ValueError) as e:
        return "Error: Invalid input"
    


@app.route('/products' , methods=['GET', 'POST'])
def products():
    supercat_id = request.args.get('supercat_id', type=int, default=None)
    subcat_id = request.args.get('subcat_id', type=int, default=None)
    supercat_name = None
    subcat_name = None
    
    if supercat_id:
        products = Product.query.filter_by(supercat_id=supercat_id).all()
        supercat = SuperCat.query.filter_by(id=supercat_id).first()
        if supercat:
            supercat_name = supercat.cat_name
    elif subcat_id:
        products = Product.query.filter_by(subcat_id=subcat_id).all()
        subcat = SubCat.query.filter_by(id=subcat_id).first()
        if subcat:
            subcat_name = subcat.cat_name
            supercat_name = subcat.supercat.cat_name  # Assuming SubCat model has a reference to SuperCat
    else:
        products = []

    supercats = SuperCat.query.all()
    return render_template('products.html.j2', supercats=supercats, products=products, supercat_name=supercat_name, subcat_name=subcat_name)


# 當您需要顯示產品詳情時，可以添加一個路由
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    # 根據產品ID從資料庫獲取產品
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html.j2', product=product)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}


@app.route('/get-subcategories/<int:supercat_id>')
def get_subcategories(supercat_id):
    subcats = SubCat.query.filter_by(super_cat_id=supercat_id).all()
    subcat_list = [{'id': subcat.id, 'name': subcat.cat_name} for subcat in subcats]
    return jsonify(subcat_list)


@app.route("/supercat/list/", methods=["GET"])
def supercat_list():
    supercats = SuperCat.query.all()
    
    return render_template('supercat_list.html.j2', supercats=supercats)

@app.route("/subcat/list/", methods=["GET"])
def subcat_list():
    subcats = SubCat.query.all()
    return render_template('subcat_list.html.j2', subcats=subcats)
  

# 添加购物车
@app.route("/cart_add/")
@login_required
def cart_add():
    cart = Cart(
        product_id=request.args.get('product_id'),
        number=request.args.get('number'),
        user_id=session.get('user_id')  # 获取用户ID,判断用户是否登录
    )
    db.session.add(cart)  # 添加数据
    db.session.commit()  # 提交数据
    return redirect(url_for('shopping_cart'))


# 清空购物车
@app.route("/cart_clear/")
@login_required
def cart_clear():
    user_id = session.get('user_id')  # 获取用户ID,判断用户是否登录
    Cart.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    return redirect(url_for('shopping_cart'))


# 查看购物车
@app.route("/shopping_cart/")
@login_required
def shopping_cart():
    user_id = session.get('user_id')
    cart = Cart.query.filter_by(user_id=int(user_id)).order_by(Cart.addtime.desc()).all()
    total = sum([item.product.price * item.number for item in cart])
    return render_template('shopping_cart.html.j2', cart=cart , total=total)


# 删除购物车
@app.route("/cart_delete/<int:id>/")
@login_required
def cart_delete(id=None):
    user_id = session.get('user_id')  # 获取用户ID,判断用户是否登录
    db.session.delete(Cart.query.filter_by(user_id=user_id, product_id=id).first())
    db.session.commit()
    return redirect(url_for('shopping_cart'))



# 购物车添加订单
@app.route("/cart_order/", methods=['GET', 'POST'])
@login_required
def cart_order():
    
    if request.method == 'POST':
        user_id = session.get('user_id')  # 获取用户id
        # 添加订单
        orders = Orders(
            user_id=user_id,
        )
        db.session.add(orders)  # 添加数据
        db.session.commit()  # 提交数据_
        # 添加订单详情
        cart = Cart.query.filter_by(user_id=user_id).all()
        object = []
        for item in cart:
            product = Product.query.get(item.product_id)
            object.append(
                OrdersDetail(
                    order_id=orders.id,
                    product_id=item.product_id,
                    order_name=product.name,  # 從 Product 模型中獲取產品名稱
                    number=item.number,  # 從 Cart 模型中獲取數量
                )
            )
        db.session.add_all(object)
        Cart.query.filter_by(user_id=user_id).update({'user_id':0})
        db.session.commit()
    return redirect(url_for('order_list'))

# 查看我的订单
@app.route("/order_list", methods=['GET', 'POST'])
@login_required
def order_list():
    user_id = session.get('user_id', 0)
    orders = OrdersDetail.query.join(Orders).filter(Orders.user_id == user_id).order_by(Orders.addtime.desc()).all()
    return render_template('order_list.html.j2', orders=orders)

@app.route("/order_detail/<int:id>/")
@login_required
def order_detail(id=None):
    orders = OrdersDetail.query.filter_by(order_id=id).all()
    return render_template('order_detail.html.j2', orders=orders)

# 收藏与取消收藏商品
@app.route("/collect_add/")
@login_required
def collect_add():
    product_id = request.args.get("product_id", "")  # 接收传递的参数
    user_id = session.get('user_id', 0)  # 获取当前用户的ID
    collect = Collect.query.filter_by(  # 根据用户ID和商品ID判断是否该收藏
        user_id=int(user_id),
        product_id=int(product_id)
    ).count()

    # 已收藏,取消收藏
    if collect == 1:
        c = Collect.query.filter_by(product_id=product_id, user_id=user_id).first()  # 查找Collect表，查看记录是否存在
        db.session.delete(c)  # 删除数据
        db.session.commit()  # 提交数据
        return redirect(url_for('product_detail', product_id=product_id))

    # 未收藏进行收藏
    if collect == 0:
        collect = Collect(
            user_id=int(user_id),
            product_id=int(product_id)
        )
        db.session.add(collect)  # 添加数据
        db.session.commit()  # 提交数据
        return redirect(url_for('product_detail', product_id=product_id) )
    


# 查看收藏列表
@app.route("/collect_list")
@login_required
def collect_list():
    user_id = session.get('user_id', 0)
    collects = Collect.query.filter_by(user_id=int(user_id)).order_by(Collect.addtime.desc()).all()
    return render_template('collect_list.html.j2', collects=collects)



# 删除收藏
@app.route("/collect_delete/<int:id>/")
@login_required
def collect_delete(id=None):
    user_id = session.get('user_id', 0)  # 获取用户ID,判断用户是否登录
    db.session.delete(Collect.query.filter_by(user_id=user_id, product_id=id).first())
    db.session.commit()
    return redirect(url_for('collect_list'))

@app.route("/product_delete/<int:id>/")
@login_required
def product_delete(id=None):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('products'))


@app.route("/product_edit/<int:id>/", methods=['GET', 'POST'])
@login_required
def product_edit(id=None):
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.price = request.form.get('price')
        product.description = request.form.get('description')
        product.supercat_id = request.form.get('supercat_id')
        product.subcat_id = request.form.get('subcat_id')
        db.session.commit()
        return redirect(url_for('products'))
    return render_template('product_edit.html.j2', product=product, categories=SubCat.query.distinct(SubCat.super_cat_id).all())





@app.route('/shop')
def shops():
    # 從數據庫中查詢所有的 Shop 紀錄
    shops = Shop.query.all()
    # 將查詢結果傳遞給模板
    return render_template('shop.html.j2', shop=shops)


@app.route('/shop/detail/<int:id>/')
def shop_detail(id):
    shop = Shop.query.get_or_404(id)
    return render_template('shop_detail.html.j2', shop=shop)


@app.route('/author')
def author():
    authors = Author.query.all()
    return render_template('author.html.j2', authors=authors)


@app.route('/author/<int:id>')
def author_detail(id):
    author = Author.query.get_or_404(id)
    return render_template('author_detail.html.j2', author=author)

@app.route('/news_list')
def news_list():
    news = News.query.all()
    return render_template('news_list.html.j2', news=news)




@app.route('/news_list/<int:news_id>')
def news_detail(news_id):
    news_item = News.query.get(news_id)
    return render_template('news_detail.html.j2', news_item=news_item)

@app.route('/search')
def search():
    page = request.args.get('page', 1, type=int)
    keywords = request.args.get('keywords', '', type=str)
    if keywords:
        page_data = Product.query.filter(Product.name.like("%" + keywords + "%")).order_by(
            Product.addtime.desc()
        ).paginate(page=page, per_page=12)
    else:
        page_data = Product.query.order_by(
            Product.addtime.desc()
        ).paginate(page=page, per_page=12)
    return render_template("search.html.j2", page_data=page_data, keywords=keywords)


@app.route('/newproduct')
def newproduct():
    products = Product.query.order_by(desc(Product.addtime)).all()
    return render_template('newproduct.html.j2', products=products)



@app.route('/add_comment/<int:news_id>', methods=['POST'])
def add_comment(news_id):
    content = request.form.get('content')
    comment = Comment(content=content, news_id=news_id)
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('news_detail', news_id=news_id))

@app.route('/information')
def information():
    return render_template('information.html.j2')

@app.route('/washing_machine')
def washing_machine():
    return render_template('washing_machine.html.j2')

@app.route('/Air_conditioner')
def Air_conditioner():
    return render_template('Air_conditioner.html.j2')

@app.route('/Dehumidifier')
def Dehumidifier():
    return render_template('Dehumidifier.html.j2')

@app.route('/oral_care')
def oral_care():
    return render_template('oral_care.html.j2')

@app.route('/Refrigerator')
def Refrigerator():
    return render_template('Refrigerator.html.j2')

@app.route('/post')
def all_posts():
    post = Post.query.all()
    return render_template('post.html.j2', post=post)

@app.route('/post/<int:post_id>')
def single_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html.j2', post=post)



@app.route('/new_post', methods=['GET', 'POST'])
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data)  # Remove the 'author' argument
        db.session.add(post)
        db.session.commit()
        flash(_('Your post is now live!'))
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.paginate(
        page=page, per_page=app.config["POSTS_PER_PAGE"], error_out=False)
    next_url = url_for(
        'new_post', page=posts.next_num) if posts.next_num else None
    prev_url = url_for(
        'new_post', page=posts.prev_num) if posts.prev_num else None
    return render_template('index.html.j2', title=_('Home'), form=form,
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)