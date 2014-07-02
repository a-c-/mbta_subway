from __future__ import print_function
import urllib2
from gtfs_realtime_pb2 import FeedMessage

data = urllib2.urlopen('http://developer.mbta.com/lib/gtrtfs/Vehicles.pb').read()

vehicles = FeedMessage.FromString(data)

print("print(vehicles): ")
print(vehicles)

print("print(len(vehicles.entity)): ")
# entity is the list of entities
print(len(vehicles.entity))

print("print(vehicles.entity[0].vehicle): ")
# each element in the entity list has a .vehicle field (or .trip_update or .alert in other feeds)
print(vehicles.entity[0].vehicle)
