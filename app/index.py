from app import app, login
from flask import redirect, render_template, request
import dao
from flask_login import login_user, logout_user
from datetime import datetime


@app.route('/', methods=['get'])
def index():
    return render_template('/client/home.html')


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
    err_msg = ""

    return render_template('client/user_register.html')


@app.route("/user/user_profile", methods=['get'])
def user_profile():
    return render_template('client/user_profile.html')


@app.route('/user/login', methods=['get', 'post'])
def user_login():
    return render_template('client/user_login.html')


@app.route('/user/logout', methods=['post'])
def user_logout():
    logout_user()
    return redirect('/')


@app.route('/employee', methods=['get'])
def employee_index():
    return render_template('client/Employeelogin.html')


@app.route('/employee/login', methods=['get', 'post'])
def employee_login():
    return render_template('client/Employeemain.html')


@login.user_loader
def get_user(user_id):
    return dao.get_user_by_id(user_id)


@app.context_processor
def common_response():
    return {
        'airports': dao.get_all_airport(),
        'seat_classes': dao.get_seat_class()
    }


if __name__ == "__main__":
    from app import admin

    app.run(debug=True)
