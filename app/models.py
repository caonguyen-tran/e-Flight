from sqlalchemy import Integer, String, Float, DateTime, Column, Boolean, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
import enum
from app import db
from datetime import datetime
from flask_login import UserMixin


class Role(enum.Enum):
    USER = 1
    ADMIN = 2
    EMPLOYEE = 3


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    gender = Column(String(20), nullable=False)
    date_of_birth = Column(DateTime, default=datetime.now())
    avatar = Column(String(100),
                    default='https://res.cloudinary.com/dndakokcz/image/upload/v1704201170/default-user-avatar_fegu5k.webp')
    user_role = Column(Enum(Role), default=Role.USER)

    def __str__(self):
        return self.username


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.now())


class Company(BaseModel):
    name = Column(String(50), nullable=False, unique=True)
    logo = Column(String(150),
                  default='https://res.cloudinary.com/dndakokcz/image/upload/v1704202637/airplane-logo-template-icon-design-vector-35304303_ljbocz.jpg')

    def __str__(self):
        return self.name


class Aircraft(BaseModel):
    name = Column(String(50), nullable=False, unique=True)
    total_seat = Column(Integer, nullable=False, default=250)
    airline_company_id = Column(Integer, ForeignKey(Company.id), nullable=False)
    company = relationship('Company', backref='aircraft', lazy=True)

    def __str__(self):
        return self.name


class Airport(BaseModel):
    name = Column(String(50), nullable=False, unique=True)

    def __str__(self):
        return self.name


class Route(BaseModel):
    locate_from = Column(String(50), nullable=False)
    locate_to = Column(String(50), nullable=False)
    airport_from_id = Column(Integer, ForeignKey(Airport.id), nullable=False)
    airport_to_id = Column(Integer, ForeignKey(Airport.id), nullable=False)
    UniqueConstraint('airport_from', 'airport_to')
    distance_road = Column(Float, nullable=False)
    airport_from = relationship('Airport', foreign_keys=[airport_from_id], lazy=True)
    airport_to = relationship('Airport', foreign_keys=[airport_to_id], lazy=True)

    def __str__(self):
        return str('Từ ' + self.locate_from + ' đi ' + self.locate_to)


class Flight(BaseModel):
    name = Column(String(50), nullable=False, unique=False)
    arrival_time = Column(Integer, default=30)
    departure_time = Column(DateTime, nullable=False)
    aircraft_id = Column(Integer, ForeignKey(Aircraft.id), nullable=False)
    flight_route = Column(Integer, ForeignKey(Route.id), nullable=False)
    emp_id = Column(Integer, ForeignKey(User.id), nullable=False)
    aircraft = relationship('Aircraft', backref='flight', lazy=True)
    routes = relationship('Route', backref='flight', lazy=True)
    emp = relationship('User', backref='flight', lazy=True)

    def __str__(self):
        return self.name


class Stopover(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    time_break = Column(Integer, nullable=False, default=20)
    note = Column(String(100), nullable=True)
    airport_id = Column(Integer, ForeignKey(Airport.id), nullable=False)
    flight_route_id = Column(Integer, ForeignKey(Route.id), nullable=False)
    airport = relationship('Airport', backref='stopovers', lazy=True)
    route = relationship('Route', backref='stopovers', lazy=True)


class SeatClass(BaseModel):
    name = Column(String(50), nullable=False, unique=True)

    def __str__(self):
        return self.name


class AirSeatClass(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    seat_class_id = Column(Integer, ForeignKey(SeatClass.id), nullable=False)
    aircraft_id = Column(Integer, ForeignKey(Aircraft.id), nullable=False)
    price = Column(Float, nullable=False)
    seat_class = relationship('SeatClass', backref='air_seat_classes', lazy=True)
    aircraft = relationship('Aircraft', backref='air_seat_classes', lazy=True)


class Seat(BaseModel):
    air_seat_class_id = Column(Integer, ForeignKey(AirSeatClass.id), nullable=False)
    air_seat_class = relationship('AirSeatClass', backref='seat', lazy=True)

    def __str__(self):
        return self.id


class Ticket(BaseModel):
    total_price = Column(Float, nullable=False)
    customer_id = Column(Integer, ForeignKey(User.id), nullable=False)
    flight_id = Column(Integer, ForeignKey(Flight.id), nullable=False)
    seat_id = Column(Integer, ForeignKey(Seat.id), nullable=False)
    customer = relationship('User', backref='tickets', lazy=True)
    seat = relationship('Seat', backref='tickets', lazy=True)


if __name__ == "__main__":
    from app import app
    import hashlib

    with app.app_context():
        db.create_all()

        # u = User(firstname='nguyen', lastname='tran', username='admin',
        #          password=str(hashlib.md5('Admin@123'.encode('utf-8')).hexdigest()), gender='Male',
        #          date_of_birth='2003-11-10 15:02:25', user_role=Role.ADMIN)
        # db.session.add(u)
        # db.session.commit()
