from app import app, login
from flask import redirect, render_template, request
import dao
from flask_login import login_user
from datetime import datetime


@app.route('/', methods=['get'])
def index():
    airports = dao.get_all_airport()
    seat_classes = dao.get_seat_class()
    return render_template('/client/home.html', airports=airports, seat_classes=seat_classes)


@app.route('/flights', methods=['get'])
def flight_search():
    locate_from = request.args.get('from')
    locate_to = request.args.get('to')
    sc = request.args.get('sc')
    dt = request.args.get('dt')
    flights = dao.get_flights(locate_from, locate_to, dt, sc)
    route_name = dao.get_route_name(locate_from, locate_to).name
    date_format = dao.format_date(dt)
    return render_template('client/flight.html', flights=flights, route_name=route_name, date_format=date_format)


@app.route('/admin/login', methods=['post'])
def admin_login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = dao.auth_user(username=username, password=password)

    if user:
        login_user(user=user)

    return redirect('/admin')


@app.route('/user/register', methods=['get', 'post'])
def user_register():
    return render_template('client/user_register.html')


@app.route('/user/login', methods=['get', 'post'])
def user_login():
    return render_template('client/user_login.html')


@login.user_loader
def get_user(user_id):
    return dao.get_user_by_id(user_id)


if __name__ == "__main__":
    from app import admin

    app.run(debug=True)
