from app.models import User, Route, Airport, Flight, SeatClass, Aircraft, Seat, AirSeatClass, Company, Ticket
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
            'price': int(flight.AirSeatClass.price),
            'seat_class_id': flight.SeatClass.id,
            'seat_class_name': flight.SeatClass.name,
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


def get_air_seat_class(flight_id, aircraft_id, sc_id):
    asc = db.session.query(Flight, AirSeatClass, Aircraft) \
        .join(Flight, Flight.aircraft_id.__eq__(Aircraft.id)) \
        .join(AirSeatClass, AirSeatClass.aircraft_id.__eq__(aircraft_id)) \
        .filter(Flight.id.__eq__(flight_id)) \
        .filter(AirSeatClass.aircraft_id.__eq__(aircraft_id)) \
        .filter(AirSeatClass.seat_class_id.__eq__(sc_id)) \
        .first()

    return asc.AirSeatClass.id


def get_seat(asc_id):
    seats = db.session.query(Seat) \
        .filter(Seat.air_seat_class_id.__eq__(asc_id)) \
        .filter(Seat.active.__eq__(1)).first()

    return seats


def get_ticket_by_user(user_id):
    ticket_of_user = Ticket.query.filter(Ticket.customer_id.__eq__(user_id)).all()

    list_ticket = []
    for ticket in ticket_of_user:
        list_ticket.append({
            'customer_id': ticket.customer_id,
            'flight_id': ticket.flight_id,
            'seat_id': ticket.seat_id,
            'total_price': ticket.total_price,
            'created_date': ticket.created_date
        })

    return list_ticket


def get_info_ticket_user(user_id):
    info_tickets = db.session.query(Ticket, User, Seat, AirSeatClass, Flight, Aircraft, Company, Route, SeatClass) \
        .join(User, User.id.__eq__(Ticket.customer_id)) \
        .join(Seat, Seat.id.__eq__(Ticket.seat_id)) \
        .join(Flight, Flight.id.__eq__(Ticket.flight_id)) \
        .join(AirSeatClass, AirSeatClass.id.__eq__(Seat.air_seat_class_id)) \
        .join(SeatClass, SeatClass.id.__eq__(AirSeatClass.seat_class_id)) \
        .join(Aircraft, Aircraft.id.__eq__(Flight.aircraft_id)) \
        .join(Company, Company.id.__eq__(Aircraft.company_id)) \
        .join(Route, Route.id.__eq__(Flight.route_id)) \
        .filter(User.id.__eq__(user_id)).all()

    list_ticket = []

    for info in info_tickets:
        list_ticket.append({
            'ticket_id': info.Ticket.id,
            'customer_id': info.Ticket.customer_id,
            'flight_id': info.Ticket.flight_id,
            'seat_id': info.Ticket.seat_id,
            'seat_class_name': info.SeatClass.name,
            'aircraft_name': info.Aircraft.name,
            'company_name': info.Company.name,
            'route_name': info.Route.name,
            'ticket_date': info.Ticket.created_date,
            'departure_time': info.Flight.departure_time
        })

    return list_ticket


def get_all_flight():
    return Flight.query.all()


def get_all_route():
    return Route.query.all()


def get_all_aircraft():
    return Aircraft.query.all()


def create_flight(emp_id, route_id, aircraft_id, name, departure_time, arrival_time):
    f = Flight(emp_id=emp_id, route_id=route_id, aircraft_id=aircraft_id, name=name, departure_time=departure_time,
               arrival_time=arrival_time)
    db.session.add(f)
    db.session.commit()


# def revenue_stats(year):
#     query = db.session.query(Route.id, Route.name, func.extract('month', Flight.created_date).label('flight_month'),
#                              func.sum(Ticket.total_price).label('total_price')) \
#         .join(Route, Route.id.__eq__(Flight.route_id)) \
#         .join(Ticket, Ticket.flight_id.__eq__(Flight.id)) \
#         .filter(func.extract('year', Flight.created_date).__eq__(year)) \
#         .group_by(Route.id, func.extract('month', Flight.created_date))
#
#     return query.all()


def revenue_month_stats(year, month=1):
    query = db.session.query(Route.id, Route.name, func.extract('month', Flight.created_date).label('flight_month'),
                             func.sum(Ticket.total_price).label('total_price')) \
        .join(Route, Route.id.__eq__(Flight.route_id)) \
        .join(Ticket, Ticket.flight_id.__eq__(Flight.id)) \
        .filter(func.extract('year', Flight.created_date).__eq__(year)) \
        .filter(func.extract('month', Flight.created_date).__eq__(month))\
        .group_by(Route.id, func.extract('month', Flight.created_date))

    return query.all()
