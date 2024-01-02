from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, expose, BaseView
from app import app, db
from app.models import User, Aircraft, Airport, AirlineCompany, AirSeatClass, \
    Customer, Employee, _Admin, Flight, FlightRoute, Stopover, Seat, SeatClass, Ticket, Role, AdminType
from flask_login import login_user, current_user
from flask import request

admin = Admin(app=app, name='ADMIN PAGE')


class AuthenticatedSystemAdmin(ModelView, BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class AuthenticatedStatsAdmin(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.type_admin == AdminType.STATISTIC


class UserView(ModelView):
    column_list = ['id', 'firstname', 'lastname', 'username', 'gender', 'date_of_birth', 'avatar', 'user_role',
                   'point_accumulator', 'type_admin', 'type_emp']
    column_searchable_list = ['name']
    column_filters = ['name']


class FlightView(ModelView):
    column_list = ['__all__']


class AircraftView(ModelView):
    column_list = ['__all__']


class AirportView(ModelView):
    column_list = ['__all__']


# class AirlineCompanyView(AuthenticatedSystemAdmin):
#     column_list = ['__all__']
#
#
# class FlightRouteView(AuthenticatedSystemAdmin):
#     column_list = ['__all__']
#
#
# class SeatView(AuthenticatedSystemAdmin):
#     column_list = ['__all__']
#
#
# class StopoverView(AuthenticatedSystemAdmin):
#     column_list = ['__all__']
#
#
# class SeatClassView(AuthenticatedSystemAdmin):
#     column_list = ['__all__']
#

# admin.add_view(UserView(User, db.session))
admin.add_view(FlightView(Flight, db.session))
admin.add_view(AircraftView(Aircraft, db.session))
admin.add_view(AirportView(Airport, db.session))
