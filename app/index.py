from app import app, login
from flask import redirect, render_template, request, jsonify, session
import dao, utils
from flask_login import login_user, logout_user, current_user
from app.models import User, Role


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
    date_format = utils.format_date(dt)
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
    err_msg = ''
    if request.method.__eq__("POST"):
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        username = request.form.get('username')
        birthday = request.form.get('dateOfBirth')
        gender = request.form.get('gender')
        email = request.form.get('email')
        phone = request.form.get('phone_number')
        pw = request.form.get('password')
        confirm_pw = request.form.get('confirm_password')
        if firstname == '' or lastname == '' or username == '' or birthday is None or email == '' or phone == '' \
                or pw == '' or confirm_pw == '':
            err_msg = 'Vui lòng nhập đầy đủ thông tin!'
        else:
            if pw.__eq__(confirm_pw):
                try:
                    dao.add_user(firstname, lastname, username, pw, gender, birthday, email, phone)
                except Exception as ex:
                    err_msg = 'Hệ thống đang bị lỗi!'
                else:
                    return redirect('/user/login')
            else:
                err_msg = "Mật khẩu không trùng khớp!"
    return render_template('client/user_register.html', err_msg=err_msg)


@app.route("/user/user_profile", methods=['get'])
def user_profile():
    return render_template('client/user_profile.html')


@app.route('/user/login', methods=['get', 'post'])
def user_login():
    err_msg = None
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        user = dao.auth_user(username=username, password=password)

        if user:
            login_user(user=user)
            return redirect('/')
        else:
            err_msg = 'loi'
    return render_template('client/user_login.html', err_msg=err_msg)


@app.route('/user/logout')
def user_logout():
    logout_user()
    return redirect('/')


@app.route('/employee/login', methods=['get', 'post'])
def employee_login():
    err_msg = ''
    if request.method.__eq__("POST"):
        username = request.form.get('username')
        password = request.form.get('password')
        user = dao.auth_user(username, password)
        if user:
            if user.user_role == Role.EMPLOYEE:
                login_user(user=user)
                return redirect('/employee')
            else:
                err_msg = "Chức năng này không dành cho bạn!"
        else:
            err_msg = 'Tài khoản hoặc mật khẩu của bạn không chính xác!'
    return render_template('client/Employeelogin.html', err_msg=err_msg)


@app.route('/employee', methods=['get'])
def employee_index():
    if current_user.is_authenticated:
        return render_template('client/Employeemain.html')
    else:
        return redirect('/employee/login')


@app.route('/employee/search_flights', methods=['get'])
def employee_search():
    locate_from = request.args.get('from')
    locate_to = request.args.get('to')
    sc = request.args.get('sc')
    dt = request.args.get('dt')
    flights = dao.get_flights(locate_from, locate_to, dt, sc)
    route_name = dao.get_route_name(locate_from, locate_to).name
    return render_template('client/Employeemain.html', flights=flights, route_name=route_name)


@app.route('/api/add_cart', methods=['post'])
def add_to_cart():
    data = request.json

    tickets = session.get('tickets')

    if tickets is None:
        tickets = {}

    id = str(data.get('id'))
    sc_id = str(data.get('seat_class_id'))
    if id in tickets:
        if sc_id in tickets[id]['seat_class']:
            tickets[id]['seat_class'][sc_id]['quantity'] += 1
        else:
            tickets[id]['seat_class'][sc_id] = {
                    'seat_class_name': data.get('seat_class_name'),
                    'price': data.get('price'),
                    'quantity': 1
                }
    else:
        tickets[id] = {
            'id': id,
            'aircraft_id': data.get('aircraft_id'),
            'aircraft_name': data.get('aircraft_name'),
            'route_name': data.get('route_name'),
            'company_name': data.get('company_name'),
            'departure_time': data.get('departure_time'),
            'company_logo': data.get('company_logo'),
            'seat_class': {
                sc_id: {
                    'seat_class_name': data.get('seat_class_name'),
                    'price': data.get('price'),
                    'quantity': 1
                }
            }
        }

    session['tickets'] = tickets

    return jsonify({
        'tickets': tickets,
        'total_cost': utils.total_cost(tickets)
    })


@login.user_loader
def get_user(user_id):
    return dao.get_user_by_id(user_id)


@app.context_processor
def common_response():
    return {
        'airports': dao.get_all_airport(),
        'seat_classes': dao.get_seat_class(),
        'current_user': current_user
    }


if __name__ == "__main__":
    from app import admin

    app.run(debug=True)
