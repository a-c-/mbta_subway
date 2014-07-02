from __future__ import print_function
import json
import urllib2
from collections import defaultdict, OrderedDict
from datetime import datetime
from pytz import timezone
import pytz
from time import gmtime, strftime
import csv


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



def print_stations(stations, f_name):
    for station in stations:
        print(' ', file = f_name)
        print(station, "Predictions:", file = f_name)

        for dest in stations[station]:
            # if there are predictions for the direction at the station...
            if stations[station][dest]:
                print("Trains to", dest, "approaching in ", file = f_name)

                for time in stations[station][dest]:
                    print(time[0], "minutes", file = f_name)




# check to see if consecutive arrival times at stations differ by more than
# a specified threshold
# default delay check is 10 minutes... may change that later

# find a way to save only if delay > 15 min?
def check_delays(stations, time_in, minutes = 10):
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



def main():
    # get train line from user
    line = raw_input('Check predictions for red, orange, or blue line? ')
    # convert user input to all lowercase
    line = line.strip().lower()
    # error check
    if line not in lines:
        print("Error. Please enter 'red', 'orange', or 'blue'")
    else:
        # we just use the lines dictionary here
        line_color = lines[line]
        # and put the color name into the string
        link_to_data = "http://developer.mbta.com/lib/rthr/{}.json".format(line)

        # open data
        data1 = urllib2.urlopen(link_to_data).read()
        data2 = json.loads(data1)

        # get time (in epoch)
        time1 = data2['TripList']['CurrentTime']

        # build station prediction data structure
        build_stations(line_color, data2)

        # # print information about arrival predictions
        # print_stations(line_color, f)

        # get delay information
        check_delays(line_color, time1)

        # write csv file
        csv_file = '/Users/ashleycuster/Desktop/csv/{0}_{1}.txt'.format(
                        line,
                        datetime.fromtimestamp(time1).strftime('%Y%m%d_%H%M%S')
                        )
        with open(csv_file, 'wb') as foo:
            dw = csv.writer(foo)
            dw.writerow(['Station', 'Destination', 'Delay_Time'])
            for station in delays:
                for destination in delays[station]:
                    for delay_time in delays[station][destination]:
                        dw.writerow([station, destination, delay_time])





if __name__ == '__main__':
    # run main
    main()
