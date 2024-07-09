from flask import render_template, redirect, flash,request,url_for
from os import path
from flask_login import login_user, logout_user, login_required, current_user
from models import Product, Comment, User
from forms import LoginForm, ProductForm, RegisterForm
from ext import app, db
profiles = [
]

@app.route("/")
def index():
    products=Product.query.all()
    return render_template("index.html", products=products, role="Admin")

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        Registered_user = User.query.filter_by(username=form.username.data).first()
        if Registered_user:
            flash('Username is already taken. Please choose a different one.')
            return redirect("/register")
        new_user = User(username=form.username.data, password=form.password.data)
        new_user.create()
        flash('Registration successful! You can now log in.')
        return redirect("/login")
    return render_template("register.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")

@app.route("/create_product", methods=["GET", "POST"])
@login_required
def create_product():
    if not current_user.is_authenticated or current_user.role != 'Admin':
        flash("Access to this page is restricted.")
        return redirect("/")
    form = ProductForm()
    if form.validate_on_submit():
        new_product = Product(name=form.name.data, price=form.price.data)
        image = form.img.data
        directory = path.join(app.root_path, "static", "images", image.filename)
        image.save(directory)
        new_product.img =image.filename
        new_product.create()
        return redirect("/")

    return render_template("create_product.html",form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in.")
        return redirect('/')
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Login successful!")
            return redirect('/')
        flash('Invalid username or password.')
    return render_template('login.html', form=form)


@app.route("/second")
def second():
    return render_template("second.html")

@app.route("/product/<int:product_id>", methods=['GET', 'POST'])
def product(product_id):
    product = Product.query.get_or_404(product_id)
    comments = Comment.query.filter_by(product_id=product_id).all()

    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect("/login")  
        text = request.form.get('comment_text')
        if text:
            comment = Comment(text=text, product_id=product_id, user_id=current_user.id)
            comment.create()
            return redirect(url_for('product', product_id=product_id))
    return render_template ("product_details.html",product=product, comments=comments)

@app.route("/delete_product/<int:product_id>")
def delete_product(product_id):
    product=Product.query.get(product_id)
    product.delete()

    return redirect("/")
@app.route("/edit_product/<int:product_id>", methods=["GET", "POST"])
def edit_product(product_id):
    if not current_user.is_authenticated or current_user.role != 'Admin':
        flash("Access to this page is restricted.")
        return redirect("/")
    product = Product.query.get(product_id)
    form = ProductForm(name=product.name, price=product.price)
    
    if form.validate_on_submit():
        product.name = form.name.data
        product.price = form.price.data
        if form.img.data:
            image = form.img.data
            image_path = path.join(app.root_path, "static", "images", image.filename)
            image.save(image_path)
            product.img = image.filename 
        product.save()
        flash("Product updated successfully!")
        return redirect("/")
    
    return render_template("create_product.html", form=form, product=product)
@app.route("/delete_comment/<int:comment_id>", methods=["POST"])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    
    if comment.user_id != current_user.id and current_user.role != 'Admin':
        flash("You do not have permission to delete this comment.")
        return redirect(url_for('product', product_id=comment.product_id))
    
    comment.delete()
    flash("Comment deleted successfully!")
    return redirect(url_for('product', product_id=comment.product_id))
