from __future__ import print_function
import json
import urllib2
from collections import defaultdict, OrderedDict
from datetime import datetime
from pytz import timezone
import pytz
from time import gmtime, strftime
import csv
import time
from gtfs_realtime_pb2 import FeedMessage


# Lists of red, orange, and blue line stations
# each station is followed by a list of destinations/directions
# this is followed by a list of arrival times to the station in
# the provided direction


lines = {
    'red': defaultdict(lambda: defaultdict(list)),
    'blue': defaultdict(lambda: defaultdict(list)),
    'orange': defaultdict(lambda: defaultdict(list)),
}

# dictionary to store delay information
delays = defaultdict(lambda: defaultdict(list))

# schedule delay thresholds
schedule_thresholds = {
    # early am: 2:30 - 6:59
    'early_am': 10,
    # am peak: 7:00 - 8:59
    'am_peak': 10,
    # midday: 9:00 - 15:59
    'midday': 10,
    # pm peak: 16:00 - 18:29
    'pm_peak': 10,
    # evening: 18:30 - 2:29
    'evening': 10,
    # weekend friday 2:30 - monday 2:30
    'weekend': 10
}

# branch stations
branches = ['JFK/UMass', 'Savin Hill', 'Fields Corner', 'Shawmut', 'Ashmont',
            'North Quincy', 'Wollaston', 'Quincy Center',
            'Quincy Adams', 'Braintree']

branch_addition = 5


def set_minutes(time_in, station):
    # time of day adjustment
    # convert epoch time_in to readable time
    d = datetime.fromtimestamp(time_in)
    eastern = timezone('US/Eastern')
    d_east = eastern.localize(d)
    hour_in = d_east.hour + (d_east.minute/60)
    # get the day from the time, monday - sunday : 0 - 6
    day_in = d_east.weekday()

    if day_in > 4:
        service = 'weekend'
    elif hour_in >= 2.5 and hour_in < 7:
        service = 'early_am'
    elif hour_in >= 7 and hour_in < 9:
        service = 'am_peak'
    elif hour_in >= 9 and hour_in < 16:
        service = 'midday'
    elif hour_in >= 16 and hour_in < 18.5:
        service = 'pm_peak'
    else:
        service = 'evening'

    minutes_out = schedule_thresholds[service]

    # branch adjustment
    if station in branches:
        minutes_out += branch_addition

    return minutes_out



def print_stations(stations):
    for station in stations:
        print(' ')
        print(station, "Predictions:")

        for dest in stations[station]:
            # if there are predictions for the direction at the station...
            if stations[station][dest]:
                print("Trains to", dest, "approaching in ")

                for time in stations[station][dest]:
                    print(time[0], "minutes")




# check to see if consecutive arrival times at stations differ by more than
# a specified threshold

# find a way to save only if delay > 15 min?
def check_delays(stations, time_in):
    for station in stations:
        for dest in stations[station]:
            # if there are predictions for the direction at the station...
            if stations[station][dest]:
                train1_time = stations[station][dest][0][0]

                # add function here to alter delay time threshold depending on
                #  1. station (e.g. trains less frequent on subway branches)
                #  2. time of the day (e.g. trains more frequent at rush hour)
                minutes = set_minutes(time_in, station)

                if train1_time > minutes:
                    delays[station][dest].append(train1_time)
                for i in stations[station][dest][1:]:
                    delay =  i[0] - train1_time
                    train1_time = i[0]
                    if delay > minutes:
                        # save info to delays dictionary
                        delays[station][dest].append(delay)



def build_stations(stations, data):
    # for each train on the red line, store the predicted arrival time with the
    # station the train is predicted to arrive in. Passengers can check upcoming
    # train arrival times for each station
    for x in data['TripList']['Trips']:
        train_id = x['TripID']
        for y in x['Predictions']:
            # append mintues(convert seconds) to the list of wait times of the stop
            stations[ y['Stop'] ][ x['Destination'] ].append((y['Seconds']/60,
                                                                train_id))
            stations[ y['Stop'] ][ x['Destination'] ].sort()
            # seconds sometimes are less than 0 in json data...


def save_alerts(file_name):
    data = urllib2.urlopen('http://developer.mbta.com/lib/GTRTFS/Alerts/Alerts.pb').read()

    alerts = FeedMessage.FromString(data)

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


def main():
    # get file name from user
    name = raw_input('Please name your CSV alerts file: ')
    csv_file = '/Users/ashleycuster/Desktop/csv/{}.csv'.format(name)
    with open(csv_file, 'wb') as foo:
        dw = csv.writer(foo)
        dw.writerow(['Date', 'Time', 'Line', 'Station', 'Destination', 'Delay_Time'])


    # # get train line from user
    # line = raw_input('Check predictions for red, orange, or blue line? ')
    # # convert user input to all lowercase
    # line = line.strip().lower()
    # # error check
    # if line not in lines:
    #     print("Error. Please enter 'red', 'orange', or 'blue'")
    # else:
    #     # we just use the lines dictionary here
    #     line_color = lines[line]
        # and put the color name into the string

    count = 0
    # runs for 2 hours
    while (count < 120):

        for key in lines.keys():
            line_color = lines[key]
            link_to_data = "http://developer.mbta.com/lib/rthr/{}.json".format(key)

            # open data
            data1 = urllib2.urlopen(link_to_data).read()
            data2 = json.loads(data1)

            # get time (in epoch)
            time1 = data2['TripList']['CurrentTime']

            # build station prediction data structure
            build_stations(line_color, data2)

            # print information about arrival predictions
            print_stations(line_color)

            # get delay information
            check_delays(line_color, time1)

            d = datetime.fromtimestamp(time1)
            eastern = timezone('US/Eastern')
            d_east = eastern.localize(d)
            date_display = d_east.strftime('%Y%m%d')
            time_display = d_east.strftime('%H%M%S')

            # # write csv file
            with open(csv_file, 'ab+') as working_file:
                dw = csv.writer(working_file)
                for station in delays:
                    for destination in delays[station]:
                        for delay_time in delays[station][destination]:
                            dw.writerow([date_display, time_display,
                                        key, station, destination, delay_time])
        # clear delays dictionary
        for station in delays:
            for destination in delays[station]:
                del delays[station][destination][0:]

        # clear lines dictionary
        for color in lines:
            for station in lines[color]:
                for destination in lines[color][station]:
                    del lines[color][station][destination][0:]

        save_alerts('/Users/ashleycuster/Desktop/csv/{}_alerts.csv'.format(name))

        count += 1
        # every one minute
        time.sleep(60)



if __name__ == '__main__':
    # run main
    main()
