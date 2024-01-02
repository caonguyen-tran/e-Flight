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


class AdminType(enum.Enum):
    SYSTEM = 1
    STATISTIC = 2


class EmployeeType(enum.Enum):
    SYSTEM = 1
    SELLER = 2


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
        return self.name


class Customer(User):
    point_accumulator = Column(Integer, default=0, nullable=False)


class _Admin(User):
    type_admin = Column(Enum(AdminType), default=AdminType.SYSTEM)


class Employee(User):
    type_emp = Column(Enum(EmployeeType), default=EmployeeType.SELLER)


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.now())


class AirlineCompany(BaseModel):
    name = Column(String(50), nullable=False, unique=True)
    logo = Column(String(150),
                  default='https://res.cloudinary.com/dndakokcz/image/upload/v1704202637/airplane-logo-template-icon-design-vector-35304303_ljbocz.jpg')
    aircraft = relationship('Aircraft', backref='airlinecompany', lazy=True)


class Aircraft(BaseModel):
    name = Column(String(50), nullable=False, unique=True)
    total_seat = Column(Integer, nullable=False, default=250)
    airline_company = Column(Integer, ForeignKey(AirlineCompany.id), nullable=False)

    def __str__(self):
        return self.name


class Airport(BaseModel):
    name = Column(String(50), nullable=False, unique=True)

    def __str__(self):
        return self.name


class FlightRoute(BaseModel):
    locate_from = Column(String(50), nullable=False)
    locate_to = Column(String(50), nullable=False)
    airport_from = Column(Integer, ForeignKey(Airport.id), nullable=False)
    airport_to = Column(Integer, ForeignKey(Airport.id), nullable=False)
    UniqueConstraint('airport_from', 'airport_to')
    distance_road = Column(Float, nullable=False)
    # flight = relationship('Flight', backref='flight_route', lazy=True)


class Flight(BaseModel):
    name = Column(String(50), nullable=False, unique=True)
    arrival_time = Column(Integer, default=30)
    departure_time = Column(DateTime, nullable=False)
    tickets = relationship('Ticket', backref='flight', lazy=True)
    flight_route = Column(Integer, ForeignKey(FlightRoute.id), nullable=False)

    def __str__(self):
        return self.name


class Stopover(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    time_break = Column(Integer, nullable=False, default=20)
    note = Column(String(100), nullable=True)
    airport = Column(Integer, ForeignKey(Airport.id), nullable=False)
    flight_route = Column(Integer, ForeignKey(FlightRoute.id), nullable=False)


class SeatClass(BaseModel):
    name = Column(String(50), nullable=False, unique=True)

    def __str__(self):
        return self.name


class AirSeatClass(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    seat_class = Column(Integer, ForeignKey(SeatClass.id), nullable=False)
    aircraft = Column(Integer, ForeignKey(Aircraft.id), nullable=False)
    price = Column(Float, nullable=False)


class Seat(BaseModel):
    air_seat_class = Column(Integer, ForeignKey(AirSeatClass.id), nullable=False)


class Ticket(BaseModel):
    total_price = Column(Float, nullable=False)
    customer_id = Column(Integer, ForeignKey(Customer.id), nullable=False)
    flight_id = Column(Integer, ForeignKey(Flight.id), nullable=False)
    seat_id = Column(Integer, ForeignKey(Seat.id), nullable=False)


if __name__ == "__main__":
    from app import app

    with app.app_context():
        db.create_all()
