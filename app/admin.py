from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, expose, BaseView
from app import app, db
from app.models import User, Aircraft, Airport, Company, AirSeatClass, \
    Flight, Route, Stopover, Seat, SeatClass, Ticket, Role
from flask_login import login_user, current_user
from flask import request

admin = Admin(app=app, name='ADMIN PAGE', template_mode='bootstrap4')


class AuthenticatedStatsAdmin(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class AuthenticatedSystemAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == Role.ADMIN


class UserView(AuthenticatedSystemAdmin):
    column_list = ['id', 'firstname', 'lastname', 'username', 'gender', 'date_of_birth', 'avatar', 'user_role']
    column_searchable_list = ['firstname']
    column_filters = ['firstname']


class FlightView(AuthenticatedSystemAdmin):
    column_list = ['id', 'name', 'active', 'departure_time', 'arrival_time', 'aircraft_id', 'flight_route', 'emp_id']


class AircraftView(AuthenticatedSystemAdmin):
    column_list = ['id', 'name', 'total_seat', 'created_date', 'company']


class AirportView(AuthenticatedSystemAdmin):
    column_list = ['id', 'name']


class AirlineCompanyView(AuthenticatedSystemAdmin):
    column_list = ['id', 'name', 'active', 'created_date', 'logo']


class FlightRouteView(AuthenticatedSystemAdmin):
    column_list = ['id', 'active', 'created_date', 'locate_from', 'locate_to', 'distance_road', 'airport_from',
                   'airport_to']


class SeatView(AuthenticatedSystemAdmin):
    column_list = ['id', 'active', 'air_seat_class']


class StopoverView(AuthenticatedSystemAdmin):
    column_list = ['id', 'time_break', 'airport_id', 'flight_route_id', 'note']


class SeatClassView(AuthenticatedSystemAdmin):
    column_list = ['id', 'name']


class TicketView(AuthenticatedSystemAdmin):
    column_list = ['id', 'active', 'created_date', 'total_price', 'customer_id', 'seat']


class AirSeatClassView(AuthenticatedSystemAdmin):
    column_list = ['id', 'price', 'aircraft', 'seat_class']


admin.add_view(FlightRouteView(Route, db.session))
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
