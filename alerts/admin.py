from django.contrib import admin
# from .models import Agency, CalendarDate, Calendar, FeedInfo, Frequency, Route, Shape, Stop, StopTime, Transfer, Trip
from alerts.models import Info, Trip, Position, Prediction 

admin.site.register(Info)
admin.site.register(Trip)
admin.site.register(Position)
admin.site.register(Prediction)

# admin.site.register(Agency)
# admin.site.register(CalendarDate)
# admin.site.register(Calendar)
# admin.site.register(FeedInfo)
# admin.site.register(Frequency)
# admin.site.register(Route)
# admin.site.register(Shape)
# admin.site.register(Stop)
# admin.site.register(StopTime)
# admin.site.register(Transfer)
# admin.site.register(Trip)

# admin.site.register(DelayRuleset)
