    # Interpret GTFS realtime data of Trip Updates
    #     feed includes profress and arrival predictions,
    #     MBTA bus only... ?



from __future__ import print_function
import urllib2
from gtfs_realtime_pb2 import FeedMessage

data = urllib2.urlopen('http://developer.mbta.com/lib/gtrtfs/Passages.pb').read()

trip_updates = FeedMessage.FromString(data)

print("\nTrip updates: ")
print(trip_updates)

print("\nNumber of trip updates: ")
# entity is the list of entities
print(len(trip_updates.entity))

print("\nFirst trip update: ")
# each element in the entity list has a .vehicle field (or .trip_update or .alert in other feeds)
print(trip_updates.entity[0].trip_update)

print("\n66 Bus stop ids: ")



count = 0

for entity in trip_updates.entity:
    if entity.trip_update.trip.route_id == "66":
        print("66 bus number", count)
        count += 1
        print("at stop id", entity.trip_update.stop_time_update[0].stop_id)
        print(entity.trip_update.stop_time_update[0].departure)

# # this (sort of) works for me - you probably need to check the update type or something b/c some stop_ids seem to be blank
# for entity in trip_updates.entity:
#     if entity.trip_update.trip.route_id == "66":
#         print(entity.trip_update.stop_time_update[0].stop_id)
#         print(entity.trip_update.stop_time_update[0].departure)
