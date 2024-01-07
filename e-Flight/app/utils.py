from datetime import datetime


def format_date(date):
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    day_of_week = date_obj.strftime('%A')
    date_format = str(date).split('-')
    return day_of_week + "," + date_format[2] + " Tháng " + date_format[1] + " " + date_format[0]


def total_cost(tickets):
    total_price, total_amount = 0, 0

    for ticket in tickets.values():
        seat_classes = ticket['seat_class']
        for sc in seat_classes.values():
            total_amount += sc['quantity']
            total_price += sc['quantity'] * sc['price']

    return {
        'total_amount': total_amount,
        'total_price': total_price
    }
