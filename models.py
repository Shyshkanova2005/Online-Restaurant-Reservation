from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False)  
    email = db.Column(db.String(100), nullable=False)

    bookings = db.relationship('Booking', backref='customer', lazy=True)

class Tables(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    table_number = db.Column(db.String(10), nullable=False, unique=True)
    seats = db.Column(db.Integer, nullable=False)

    bookings = db.relationship('Booking', backref='table_ref', lazy=True)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(10), nullable=False)
    during = db.Column(db.String(10), nullable=False) 
    guests = db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    table_id = db.Column(db.Integer, db.ForeignKey('tables.id'), nullable=False)
    order_items = db.relationship('OrderItem', backref='booking', lazy=True, cascade='all, delete-orphan')

    @property
    def total_sum(self):
        return sum(item.total_price for item in self.order_items)


class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(255))

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_item.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    menu_item = db.relationship('MenuItem')

    @property
    def total_price(self):
        return self.menu_item.price * self.quantity


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(200))
    role = db.Column(db.String(50), nullable=False, default='user')


    