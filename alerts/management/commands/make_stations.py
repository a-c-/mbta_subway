from django.core.management.base import BaseCommand, CommandError
# from alerts.models import Station, DelayRuleset, Route
import csv
import os
from alerts.models import Agency, CalendarDate, Calendar, FeedInfo, Frequency, Route, Shape, Stop, StopTime, Transfer, Trip


class Command(BaseCommand):
    help = 'populates MBTA_GTFS tables'

    def handle(self, *args, **options):
        gtfs_types = {
            Agency: 'agency',
            CalendarDate: 'calendar_dates',
            Calendar: 'calendar',
            FeedInfo: 'feed_info',
            Frequency: 'frequencies',
            Route: 'routes',
            Shape: 'shapes',
            Stop: 'stops',
            StopTime: 'stop_times',
            Transfer: 'transfers',
            Trip: 'trips'
        }
        for Model, filename in gtfs_types.items():
            # Model.objects.all().delete()
            for row in csv.DictReader(open('/Users/ashleycuster/Desktop/MBTA_GTFS/{}.txt'.format(filename))):
                # print row
                Model.objects.create(**row)






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
