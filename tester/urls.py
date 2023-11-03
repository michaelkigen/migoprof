from django.urls import path
from .views import Testview

urlpatterns = [
    path("test/",Testview.as_view())
]
