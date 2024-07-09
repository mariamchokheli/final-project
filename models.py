from flask_login import UserMixin
from ext import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
class BaseModel:
    def create (self):
        db.session.add(self)
        db.session.commit()

    def delete (self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def save():
        db.session.commit()

class Product (db.Model, BaseModel):
    __tablename__="products"

    id=db.Column(db.Integer(), primary_key=True)
    name=db.Column(db.String(), nullable=False)
    price=db.Column(db.Integer(),nullable=False)
    img=db.Column(db.Integer(),nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class Comment(db.Model, BaseModel):
    __tablename__ = "comments"

    id = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.String(), nullable=False)
    product_id = db.Column(db.Integer(), db.ForeignKey('products.id'), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)  

    user = db.relationship('User', backref='comments')
    product = db.relationship('Product', backref='comments')


class User (db.Model, BaseModel, UserMixin):

    __tablename__="users"
    
    id=db.Column(db.Integer(), primary_key=True)
    username=db.Column(db.String())
    password=db.Column(db.String())
    phone_number=db.Column(db.Integer())
    role = db.Column(db.String(), nullable=False, default="Guest")

    def __init__(self, username, password, role='Guest'):
        self.username=username
        self.password=generate_password_hash(password)
        self.role=role

    def check_password(self,password):
        return check_password_hash(self.password, password)