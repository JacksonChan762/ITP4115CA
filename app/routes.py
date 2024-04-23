from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g ,flash ,session
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from flask_babel import _, get_locale
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm, \
    ResetPasswordRequestForm, ResetPasswordForm, OrderForm
from app.models import User, Post, Product , Cart 
from werkzeug.utils import secure_filename
from PIL import Image
import jinja2
import os


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    g.locale = str(get_locale())


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required

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
    
@app.route('/update_quantity/<int:id>/<int:quantity>', methods=['POST'])
def update_quantity(id, quantity):
    # 更新數量的代碼在這裡
    ...


@app.route('/products')
def products():
    products = Product.query.all()
    return render_template('products.html.j2', products=products)  # 確保模板名稱正確


# 當您需要顯示產品詳情時，可以添加一個路由
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    # 根據產品ID從資料庫獲取產品
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html.j2', product=product)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

@app.route('/add-product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
       
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        image_file = request.files['image']
        
        if image_file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(image_path)

           
            img = Image.open(image_path)
            img.thumbnail((128, 128))  # Resize the image
            thumbnail_path = os.path.join(app.config['THUMBNAIL_FOLDER'], filename)
            img.save(thumbnail_path)

           
            new_product = Product(name=name, price=float(price), image_filename=filename)
            db.session.add(new_product)
            db.session.commit()

            flash('Product added successfully!')
            return redirect(url_for('index'))
        
    return render_template('add_product.html.j2')
        



# 添加购物车
@app.route("/cart_add/")
@login_required
def cart_add():
    cart = Cart(
        product_id=request.args.get('product_id'),
        number=request.args.get('number'),
        user_id=session.get('user_id', 0)  # 获取用户ID,判断用户是否登录
    )
    db.session.add(cart)  # 添加数据
    db.session.commit()  # 提交数据
    return redirect(url_for('shopping_cart'))


# 清空购物车
@app.route("/cart_clear/")
@login_required
def cart_clear():
    user_id = session.get('user_id', 0)  # 获取用户ID,判断用户是否登录
    Cart.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    return redirect(url_for('shopping_cart'))


# 查看购物车
@app.route("/shopping_cart/")
@login_required
def shopping_cart():
    user_id = session.get('user_id', 0)
    cart = Cart.query.filter_by(user_id=int(user_id)).order_by(Cart.addtime.desc()).all()
    return render_template('shopping_cart.html.j2', cart=cart)


# 删除购物车
@app.route("/cart_delete/<int:id>/")
@login_required
def cart_delete(id=None):
    user_id = session.get('user_id', 0)  # 获取用户ID,判断用户是否登录
    db.session.delete(Cart.query.filter_by(user_id=user_id, product_id=id).first())
    db.session.commit()
    return redirect(url_for('shopping_cart'))






    