from django.db import models


# from MBTA_GTFS files

class Agency(models.Model):
    agency_id = models.CharField(max_length=20, primary_key=True)
    agency_name = models.CharField(max_length=50)
    agency_url = models.CharField(max_length=50)
    agency_timezone = models.CharField(max_length=50)
    agency_lang = models.CharField(max_length=50)
    agency_phone = models.CharField(max_length=50)

    def __unicode__(self):
        return self.agency_name

class CalendarDate(models.Model):
    service_id = models.CharField(max_length=200)
    date = models.CharField(max_length=10)
    exception_type = models.CharField(max_length=50)

    def __unicode__(self):
        return self.service_id

class Calendar(models.Model):
    service_id = models.CharField(max_length=200, primary_key=True)
    monday = models.CharField(max_length=50)
    tuesday = models.CharField(max_length=50)
    wednesday = models.CharField(max_length=50)
    thursday = models.CharField(max_length=50)
    friday = models.CharField(max_length=50)
    saturday = models.CharField(max_length=50)
    sunday = models.CharField(max_length=50)
    start_date = models.CharField(max_length=10)
    end_date = models.CharField(max_length=10)

    def __unicode__(self):
        return self.service_id

class FeedInfo(models.Model):
    feed_publisher_name = models.CharField(max_length=20)
    feed_publisher_url = models.CharField(max_length=200)
    feed_lang = models.CharField(max_length=10)
    feed_start_date = models.CharField(max_length=10)
    feed_end_date = models.CharField(max_length=10)
    feed_version = models.CharField(max_length=300)

    def __unicode__(self):
        return self.feed_publisher_name

class Frequency(models.Model):
    trip_id = models.CharField(max_length=200)
    start_time = models.CharField(max_length=20)
    end_time = models.CharField(max_length=20)
    headway_secs = models.CharField(max_length=50)

    def __unicode__(self):
        return self.trip_id

class Route(models.Model):
    route_id = models.CharField(max_length=200, primary_key=True)
    agency_id = models.CharField(max_length=20)
    route_short_name = models.CharField(max_length=20)
    route_long_name = models.CharField(max_length=100)
    route_desc = models.CharField(max_length=200)
    route_type = models.CharField(max_length=50)
    route_url = models.CharField(max_length=200)
    route_color = models.CharField(max_length=10)
    route_text_color = models.CharField(max_length=10)

    def __unicode__(self):
        return self.route_id

class Shape(models.Model):
    shape_id = models.CharField(max_length=10)
    shape_pt_lat = models.CharField(max_length=20)
    shape_pt_lon = models.CharField(max_length=20)
    shape_pt_sequence = models.CharField(max_length=50)
    shape_dist_traveled = models.CharField(max_length=20)

    def __unicode__(self):
        return self.shape_id

class Stop(models.Model):
    stop_id = models.CharField(max_length=100, primary_key=True)
    stop_code = models.CharField(max_length=50)
    stop_name = models.CharField(max_length=200)
    stop_desc = models.CharField(max_length=200)
    stop_lat = models.CharField(max_length=20)
    stop_lon = models.CharField(max_length=20)
    zone_id = models.CharField(max_length=20)
    stop_url = models.URLField()
    location_type =  models.CharField(max_length=50)
    parent_station = models.CharField(max_length=50)

    def __unicode__(self):
        return self.stop_id

class StopTime(models.Model):
    trip_id = models.CharField(max_length=20)
    arrival_time = models.CharField(max_length=10)
    departure_time = models.CharField(max_length=10)
    stop_id = models.CharField(max_length=100)
    stop_sequence = models.CharField(max_length=10)
    stop_headsign =  models.CharField(max_length=50)
    pickup_type =  models.CharField(max_length=50)
    drop_off_type =  models.CharField(max_length=50)

    def __unicode__(self):
        return self.trip_id

class Transfer(models.Model):
    from_stop_id = models.CharField(max_length=100)
    to_stop_id = models.CharField(max_length=100)
    transfer_type = models.CharField(max_length=50)
    min_transfer_time =  models.CharField(max_length=50)

    def __unicode__(self):
        return self.from_stop_id

class Trip(models.Model):
    route_id = models.CharField(max_length=100)
    service_id = models.CharField(max_length=200)
    trip_id = models.CharField(max_length=30, primary_key=True)
    trip_headsign = models.CharField(max_length=100)
    trip_short_name = models.CharField(max_length=50)
    direction_id = models.CharField(max_length=50)
    block_id = models.CharField(max_length=50)
    shape_id = models.CharField(max_length=10)

    def __unicode__(self):
        return self.route_id



# from JSON subway information


class Position(models.Model):
    timestamp = models.PositiveIntegerField()
    train = models.CharField(max_length=20)
    latitude = models.DecimalField(max_digits=8, decimal_places=5)
    longitude = models.DecimalField(max_digits=8, decimal_places=5)
    heading = models.PositiveIntegerField()

class Prediction(models.Model):
    stop_id = models.CharField(max_length=20)
    stop = models.CharField(max_length=20)
    seconds = models.PositiveIntegerField()

class TripItem(models.Model):
    trip_id = models.CharField(max_length=50)
    destination = models.CharField(max_length=50)
    position = models.ForeignKey(Position)
    predictions = models.ManyToManyField(Prediction)

class TripList(models.Model):
    current_time = models.PositiveIntegerField()
    line = models.CharField(max_length=20)
    trips = models.ManyToManyField(TripItem)


# from GTFS-realtime alerts data

class ActivePeriod(models.Model):
    start = models.PositiveIntegerField()
    end = models.PositiveIntegerField()

class InformedEntity(models.Model):
    agency_id = models.ForeignKey(Agency)
    route_id = models.CharField(max_length=20)
    route_type = models.PositiveIntegerField()

class Alert(models.Model):
    active_period = models.ManyToManyField(ActivePeriod)
    informed_entity = models.ForeignKey(InformedEntity)
    cause = models.CharField(max_length=20)
    effect = models.CharField(max_length=20)
    header_text = models.CharField(max_length=256)
    description_text = models.TextField()

class Entity(models.Model):
    entity_id = models.CharField(max_length=20)
    alert = models.ForeignKey(Alert)


# additonal classes

class Distance(models.Model):
    train_first = models.ForeignKey(TripItem, related_name='train1')
    train_last = models.ForeignKey(TripItem, related_name='train2')
    distance = models.DecimalField(max_digits=12,decimal_places=2)
    velocity = models.DecimalField(max_digits=12,decimal_places=5)



# LINES = (
#     ('red', 'Red (main)'),
#     ('red-ashmont', 'Red (Ashmont)'),
#     ('red-braintree', 'Red (Braintree)'),
#     ('orange', 'Orange'),
#     ('blue', 'Blue'),
# )
#
# class DelayRuleset(models.Model):
#     line = models.CharField(max_length=20, choices=LINES)
#     early_am_delay_mins = models.PositiveIntegerField()
#     peak_am_delay_mins = models.PositiveIntegerField()
#     midday_delay_mins = models.PositiveIntegerField()
#     peak_pm_delay_mins = models.PositiveIntegerField()
#     evening_delay_mins = models.PositiveIntegerField()
#
#     def __unicode__(self):
#         return self.get_line_display()
#
# class Line(models.Model):
#     line = models.CharField(max_length=20, choices=LINES)
#     early_am_delay_mins = models.PositiveIntegerField()
#     peak_am_delay_mins = models.PositiveIntegerField()
#     midday_delay_mins = models.PositiveIntegerField()
#     peak_pm_delay_mins = models.PositiveIntegerField()
#     evening_delay_mins = models.PositiveIntegerField()
#
#     def __unicode__(self):
#         return self.get_line_display()
#
#
# class Station(models.Model):
#     name = models.CharField(max_length=50)
#     line = models.CharField(max_length=20, choices=LINES)
#     order = models.PositiveIntegerField()
#
#     def delay_ruleset(self):
#         return DelayRuleset.objects.get(line=self.line)
#
#     def __unicode__(self):
#         return '{} - {}'.format(self.name, self.get_line_display())
