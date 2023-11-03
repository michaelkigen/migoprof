from django.urls import path
from .views import AggregatedDailyRecordView,Dailyrecordviews

urlpatterns = [
    path("w_m_record/",AggregatedDailyRecordView.as_view(), name="weeklymonthly"),
    path("dailyrecord/",Dailyrecordviews.as_view(), name="daily")
]
