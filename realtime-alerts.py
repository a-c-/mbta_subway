"""    Interpret GTFS realtime data of Alerts
        feed includes all service alerts
"""


from __future__ import print_function
import urllib2
from gtfs_realtime_pb2 import FeedMessage
from datetime import datetime
from pytz import timezone
import pytz
from time import gmtime, strftime
import csv
import time

data = urllib2.urlopen('http://developer.mbta.com/lib/GTRTFS/Alerts/Alerts.pb').read()

alerts = FeedMessage.FromString(data)

# temp_file = '/Users/ashleycuster/Desktop/csv/temp.csv'
# f = open(temp_file, 'w+')
# print("\nAlerts: ", file = f)
# print(alerts, file = f)
# f.close()
#
# print("\nNumber of Alerts: ")
# # entity is the list of entities
# print(len(alerts.entity))
#
# print("\nFirst Alert: ")
# # each element in the entity list has a .vehicle field (or .trip_update or .alert in other feeds)
# print(alerts.entity[0].alert)

# create file
file_name = '/Users/ashleycuster/Desktop/csv/alert_test3.csv'

# time output
alert_time = alerts.header.timestamp
d = datetime.fromtimestamp(alert_time)
eastern = timezone('US/Eastern')
d_east = eastern.localize(d)
date_display = d_east.strftime('%Y%m%d')
time_display = d_east.strftime('%H%M%S')

for entity in alerts.entity:

    route = entity.alert.informed_entity[0].route_id
    color = ""
    # orange line
    if route == "903_" or route == "913_":
        color = "Orange"
    # red line
    elif route == "931_" or route == "933_":
        color = "Red"
    # blue line
    elif route == "946_" or route == "948_":
        color = "Blue"

    detour = 4

    if color and (entity.alert.effect != detour):
        text = entity.alert.header_text.translation[0].text
        with open(file_name, 'ab+') as foo:
            dw = csv.writer(foo)
            dw.writerow([date_display, time_display, color, text])
