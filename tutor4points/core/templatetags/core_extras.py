from django import template
from datetime import date, datetime

register = template.Library()

@register.simple_tag
def requeststatus (request_date, end_time, status):
    if status is True:
        return "Request Accepted"
    elif status is None: 
        if request_date == date.today() and end_time < datetime.now().time():
            return "Request Expired"
        else: 
            return "Awaiting Response"
    else:
        return "Request Declined"