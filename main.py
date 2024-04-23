import sqlite3

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from flask_wtf import FlaskForm
from flask import Flask, render_template, redirect, url_for
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import LargeBinary

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cars2.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///registrations.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return self.username


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Boolean, default=True)
    description = db.Column(db.String(100), nullable=False)
    image = db.Column(db.LargeBinary)

    def __repr__(self):
        return self.title


@app.route('/')
def index():
    items = Item.query.order_by(Item.price).all()
    return render_template('index.html', data=items)


@app.route('/registration', methods=["POST", "GET"])
def registration():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        user = User(username=username, password=password, email=email)
        print(user)

        try:
            db.session.add(user)
            db.session.commit()

            return redirect('/')
        except:
            return "Ошибка 0-0"

    else:
        return render_template('registr.html')


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == "POST":
        title = request.form['title']
        price = request.form['price']
        description = request.form['description']
        file = request.files['image']

        item = Item(title=title, price=price, description=description, name= file.filename, image = file.read)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')

        except:
            return "Ошибка 0-0"

    else:
        return render_template('create.html')



@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/upload_image', methods=['POST'])
def upload_image():
    file = request.files['image']
    new_image = Item(name=file.filename, image=file.read())
    db.session.add(new_image)
    db.session.commit()
    return render_template('upload_image.html')


@app.route('/buy/<int:id>')
def item_buy(id):
    item = Item.query.get(id)
    from cloudipsp import Api, Checkout
    api = Api(merchant_id=1396424,
              secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "USD",
        "amount": str(item.price) + "00"
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
