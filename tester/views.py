from rest_framework import views,status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .models import Test
from .serializers import Testserializer

class Testview(ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = Testserializer