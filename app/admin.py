from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, expose, BaseView
from app import app, db
from app.models import User, Aircraft, Airport, Company, AirSeatClass, \
    Flight, Route, Stopover, Seat, SeatClass, Ticket, Role
from flask_login import login_user, current_user, logout_user, login_required
from flask import redirect, render_template
import dao
admin = Admin(app=app, name='ADMIN PAGE', template_mode='bootstrap4')


class AuthenticatedUser(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class AuthenticatedAdmin(BaseView):
    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.user_role == Role.ADMIN or current_user.user_role == Role.EMPLOYEE

        return False


class AuthenticatedSystemAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == Role.ADMIN


class UserView(AuthenticatedSystemAdmin):
    column_list = ['id', 'firstname', 'lastname', 'username', 'gender', 'date_of_birth', 'avatar', 'user_role',
                   'phone_number', 'email']
    column_searchable_list = ['firstname']
    column_filters = ['firstname']


class FlightView(AuthenticatedSystemAdmin):
    column_list = ['id', 'name', 'active', 'departure_time', 'arrival_time', 'aircraft_id', 'route_id', 'emp_id']


class AircraftView(AuthenticatedSystemAdmin):
    column_list = ['id', 'name', 'total_seat', 'created_date', 'company']


class AirportView(AuthenticatedSystemAdmin):
    column_list = ['id', 'name', 'locate']


class AirlineCompanyView(AuthenticatedSystemAdmin):
    column_list = ['id', 'name', 'active', 'created_date', 'logo']


class RouteView(AuthenticatedSystemAdmin):
    column_list = ['id', 'active', 'name', 'created_date', 'distance_road', 'airport_from',
                   'airport_to']
    column_filters = ['name']


class SeatView(AuthenticatedSystemAdmin):
    column_list = ['id', 'active', 'air_seat_class', 'air_seat_class_id']


class StopoverView(AuthenticatedSystemAdmin):
    column_list = ['id', 'time_break', 'airport_id', 'route_id', 'note']


class SeatClassView(AuthenticatedSystemAdmin):
    column_list = ['id', 'name']


class TicketView(AuthenticatedSystemAdmin):
    column_list = ['id', 'active', 'created_date', 'flight_id', 'total_price', 'customer_id', 'seat']


class AirSeatClassView(AuthenticatedSystemAdmin):
    column_list = ['id', 'price', 'aircraft', 'seat_class', 'seat_class_id']
    column_filters = ['seat_class_id']


class LogoutView(AuthenticatedUser):
    @expose('/')
    def index(self):
        logout_user()

        return redirect('/admin')


class StatsView(AuthenticatedAdmin):
    @expose('/')
    def index(self):
        stats = dao.revenue_stats(2024)
        return self.render('/admin/stats.html', stats=stats)


admin.add_view(RouteView(Route, db.session))
admin.add_view(AirlineCompanyView(Company, db.session))
admin.add_view(AirportView(Airport, db.session))
admin.add_view(SeatClassView(SeatClass, db.session))
admin.add_view(UserView(User, db.session))
admin.add_view(FlightView(Flight, db.session))
admin.add_view(AircraftView(Aircraft, db.session))
admin.add_view(SeatView(Seat, db.session))
admin.add_view(AirSeatClassView(AirSeatClass, db.session))
admin.add_view(StopoverView(Stopover, db.session))
admin.add_view(TicketView(Ticket, db.session))
admin.add_view(LogoutView(name="Log Out"))
admin.add_view(StatsView(name="Statistic"))
