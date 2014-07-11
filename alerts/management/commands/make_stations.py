from django.core.management.base import BaseCommand, CommandError
# from alerts.models import Station, DelayRuleset, Route
import csv
import os
# from alerts.models import Agency, CalendarDate, Calendar, FeedInfo, Frequency, Route, Shape, Stop, StopTime, Transfer, Trip
from alerts.models import Info, Trip, Position, Prediction
import json
import urllib2

# class Command(BaseCommand):
#     help = 'populates MBTA_GTFS tables'
#
#     def handle(self, *args, **options):
#         gtfs_types = {
#             Agency: 'agency',
#             CalendarDate: 'calendar_dates',
#             Calendar: 'calendar',
#             FeedInfo: 'feed_info',
#             Frequency: 'frequencies',
#             Route: 'routes',
#             Shape: 'shapes',
#             Stop: 'stops',
#             StopTime: 'stop_times',
#             Transfer: 'transfers',
#             Trip: 'trips'
#         }
#         for Model, filename in gtfs_types.items():
#             # Model.objects.all().delete()
#             for row in csv.DictReader(open('/Users/ashleycuster/Desktop/MBTA_GTFS/{}.txt'.format(filename))):
#                 # print row
#                 Model.objects.create(**row)

def log_subway(data):

    # add data to Info table
    current_time_in = data['TripList']['CurrentTime']
    line_in = data['TripList']['Line']
    info_in = Info.objects.create(
        current_time = current_time_in,
        line = line_in
    )

    for trip in data['TripList']['Trips']:
        trip_id_in = trip['TripID']
        destination_in = trip['Destination']
        note_in = trip.get('Note')
        #relate to Info object here
        trip_in = Trip.objects.create(
            trip_id = trip_id_in,
            destination = destination_in,
            note = note_in,
            info = info_in
        )

        position = trip.get('Position')
        if position is not None:
            timestamp_in = position['Timestamp']
            train_in = position['Train']
            lat_in = position['Lat']
            lon_in = position['Long']
            heading_in = position['Heading']
            # relate to Trip object
            Position.objects.create(
                timestamp = timestamp_in,
                train = train_in,
                latitude = lat_in,
                longitude = lon_in,
                heading = heading_in,
                trip = trip_in
            )

        for prediction in trip['Predictions']:
            stop_id_in = prediction['StopID']
            stop_in = prediction['Stop']
            seconds_in = prediction['Seconds']
            # relate to Trip object
            Prediction.objects.create(
                stop_id = stop_id_in,
                stop = stop_in,
                seconds = seconds_in,
                trip = trip_in
            )



class Command(BaseCommand):
    help = 'populates subway realtime data tables'

    def handle(self, *args, **options):
        key = 'red'
        link_to_data = "http://developer.mbta.com/lib/rthr/{}.json".format(key)

        # open data
        data1 = urllib2.urlopen(link_to_data).read()
        data2 = json.loads(data1)

        log_subway(data2)






# class Command(BaseCommand):
#     help = 'Makes all of the MBTA station objects and their delay rules'
#
#     def handle(self, *args, **options):
#         DelayRuleset.objects.create(
#             line='red',
#             early_am_delay_mins = 5,
#             peak_am_delay_mins = 5,
#             midday_delay_mins = 5,
#             peak_pm_delay_mins = 5,
#             evening_delay_mins = 5
#         )
#
#         red_main_stations = ['Alewife', 'Davis', 'Porter Square', 'Harvard Square',
#                                 'Central Square', 'Kendall/MIT', 'Charles/MGH',
#                                 'Park Street', 'Downtown Crossing', 'South Station',
#                                 'Broadway', 'Andrew', 'JFK/UMass']
#         for order, station in enumerate(red_main_stations):
#             Station.objects.create(name=station, line='red', order=order)
#
#         red_ashmont_stations = ['Savin Hill', 'Fields Corner', 'Shawmut', 'Ashmont']
#         jfk = len(red_main_stations)
#         for order, station in enumerate(red_ashmont_stations):
#             Station.objects.create(name=station, line='red-ashmont', order=order+jfk)
#
#         red_braintree_stations = ['North Quincy', 'Wollaston', 'Quincy Center',
#                                   'Quincy Adams', 'Braintree']
#
#         blue_stations = ['Wonderland', 'Revere', 'Beachmont', 'Suffolk', 'Orient Heights',
#                             'Wood Island', 'Airport', 'Maverick', 'Aquarium', 'State',
#                             'Government Center', 'Bowdoin']
#
#         orange_stations = ['Oak Grove', 'Malden', 'Wellington', 'Sullivan Square',
#                             'Community College', 'North Station', 'Haymarket', 'State',
#                             'Downtown Crossing', 'Chinatown', 'Tufts', 'Back Bay',
#                             'Mass Ave', 'Ruggles', 'Roxbury Crossing', 'Jackson Square',
#                             'Stony Brook', 'Green Street', 'Forest Hills']
