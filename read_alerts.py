# reads information from Alerts.pb

import gtfs_realtime_pb2
import sys
import urllib2

# iterate through all updates in Alerts and print information about them

def ListAlerts(input_alerts):
  # print active_period information
  # for

  # print informed entity information

  # print cause information
  for cause in input_alerts.cause:
      print cause

  # print effect information
  for effect in input_alerts.effect:
      print effect

  # print url

  # print header text

  # print description text


# create alerts object
alerts = gtfs_realtime_pb2.Alert()


# get updated Alerts.pb from url
data = urllib2.urlopen("http://developer.mbta.com/lib/GTRTFS/Alerts/Alerts.pb")
# convert into string, parse string, then save into alerts object
alerts.ParseFromString(data.read())
# print alerts object
print alerts
