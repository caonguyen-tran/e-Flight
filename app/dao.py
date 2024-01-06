from app.models import User, Route, Airport, Flight, SeatClass, Aircraft, Seat, AirSeatClass, Company
import hashlib
from app import app, db
from sqlalchemy import func
from datetime import datetime
import locale
from flask import jsonify
import cloudinary.uploader

locale.setlocale(locale.LC_ALL, 'vi_VN')


def get_user_by_id(user_id):
    return User.query.get(user_id)


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    print(password)
    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()


def get_all_route():
    return Route.query.all()


def get_all_airport():
    return Airport.query.all()


def get_flight_by_id(flight_id):
    return Flight.query.filter(flight_id=flight_id)


def get_seat_class():
    return SeatClass.query.all()


def get_route_name(locate_from, locate_to):
    return Route.query.filter(Route.airport_from_id.__eq__(locate_from), Route.airport_to_id.__eq__(locate_to)).first()


def get_flights(locate_from, locate_to, date, seat_class):
    date_obj = datetime.strptime(str(date), '%Y-%m-%d')
    flights = db.session.query(Flight, Route, Aircraft, Company, AirSeatClass, SeatClass) \
        .join(Route, Route.id == Flight.route_id) \
        .join(Aircraft, Flight.aircraft_id == Aircraft.id) \
        .join(Company, Aircraft.company_id == Company.id) \
        .join(AirSeatClass, AirSeatClass.aircraft_id == Aircraft.id) \
        .join(SeatClass, SeatClass.id == AirSeatClass.seat_class_id) \
        .join(Seat, Seat.air_seat_class_id == AirSeatClass.id) \
        .filter(Route.airport_from_id.__eq__(locate_from)) \
        .filter(Route.airport_to_id.__eq__(locate_to)) \
        .filter(AirSeatClass.seat_class_id == seat_class) \
        .filter(Flight.departure_time >= date_obj) \
        .all()

    list_flight = []

    for flight in flights:
        list_flight.append({
            'id': flight.Flight.id,
            'departure_time': flight.Flight.departure_time,
            'aircraft_name': flight.Aircraft.name,
            'price': flight.AirSeatClass.price,
            'seat_class': flight.SeatClass.name,
            'name_route': flight.Route.name,
            'aircraft_id': flight.Aircraft.id,
            'company_name': flight.Company.name,
            'company_logo': flight.Company.logo
        })

    return list_flight


def format_date(date):
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    day_of_week = date_obj.strftime('%A')
    date_format = str(date).split('-')
    return day_of_week + "," + date_format[2] + " Tháng " + date_format[1] + " " + date_format[0]


def add_user(firstname, lastname, username, pw, gender, date_of_birth, email, phone_number):
    u = User(firstname=firstname, lastname=lastname, username=username, password=pw, gender=gender,
             date_of_birth=date_of_birth, email=email, phone_number=phone_number)
    db.session.add(u)
    db.session.commit()
