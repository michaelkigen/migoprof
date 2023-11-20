from django.shortcuts import render
from rest_framework import views,status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .models import DailyRecord
from .serializers import DailyRecordSerializer
from Profile.models import Profile
from users.models import User
from datetime import datetime, timedelta
from menu.models import Menu_Object
from django.utils import timezone
# ...
# Create your views here.

def convert_to_points(unavilable_food,user):
    phone_number = user["phone_number"]
    print("User ",phone_number)
    try:
        user = User.objects.get(phone_number=phone_number)
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        return Response({'error': 'profile not found.'}, status=status.HTTP_404_NOT_FOUND)
    pnts = int(unavilable_food) * 5
    print("Pointd ",pnts)
    profile.points +=pnts
    profile.save()




def recorder(food, user):
    current_time = timezone.now()  # Get the current date and time
    for item in food:
        if item['food']['is_avilable'] == True:
            food_name = item['food']['food_name']
            quantity = item['quantity']
            sub_total = item['sub_total']

            # Calculate the time difference between the current time and the record's date
            try:
                record = DailyRecord.objects.filter(food=food_name).first()
                time_difference = current_time - record.date
            except DailyRecord.DoesNotExist:
                time_difference = timedelta(hours=24)  # Set a default time difference

            # If the time difference exceeds 23 hours, create a new DailyRecord entry
            if time_difference.total_seconds() >= 23 * 3600:
                record = DailyRecord(food=food_name, quantity=quantity, amount=sub_total, date=current_time)
            else:
                # If it exists, increment the quantity and update the amount
                record.quantity += quantity
                record.amount += sub_total

            record.save()

        if item['food']['is_avilable'] == False:
            unavilable_food = item['sub_total']
            convert_to_points(unavilable_food, user)

         
class Dailyrecordviews(views.APIView):
    def get(self,request):
        try:
            dr = DailyRecord.objects.all()
        except DailyRecord.DoesNotExist:
            return Response({'error':'query dies not exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = DailyRecordSerializer(dr,many =True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        data = request.data
        # Ensure that 'food' and 'measuredFood' are present in the request data
        if 'food' not in data or 'measuredFood' not in data:
            return Response({'error': 'Both "food" and "measuredFood" fields are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new DailyRecord instance with the provided data
        serializer = DailyRecordSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class Dailydeatiled(views.APIView):
    def get(self,request,dailyrecord_id):
        try:
            dr = DailyRecord.objects.filter(dailyrecord_id = dailyrecord_id).first()
        except DailyRecord.DoesNotExist:
            return Response({'error':'query dies not exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = DailyRecordSerializer(dr,many =True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self,request,dailyrecord_id):
        try:
            dr = DailyRecord.objects.filter(dailyrecord_id = dailyrecord_id).first()
        except DailyRecord.DoesNotExist:
            return Response({'error':'query dies not exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = DailyRecordSerializer(dr,data=request.data , partial= True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    

class AggregatedDailyRecordView(views.APIView):
    def get(self, request):
        # Calculate the date range for the past week and month
        today = datetime.now().date()
        one_week_ago = today - timedelta(days=7)
        one_month_ago = today - timedelta(days=30)

        # Filter daily records for the past week and month
        weekly_records = DailyRecord.objects.filter(date__gte=one_week_ago, date__lte=today)
        monthly_records = DailyRecord.objects.filter(date__gte=one_month_ago, date__lte=today)

        # Serialize the data
        weekly_serializer = DailyRecordSerializer(weekly_records, many=True)
        monthly_serializer = DailyRecordSerializer(monthly_records, many=True)

        # Calculate weekly and monthly totals
        weekly_total_quantity = sum(record.quantity for record in weekly_records)
        weekly_total_amount = sum(record.amount for record in weekly_records)
        monthly_total_quantity = sum(record.quantity for record in monthly_records)
        monthly_total_amount = sum(record.amount for record in monthly_records)

        response_data = {
            'weekly_records': weekly_serializer.data,
            'monthly_records': monthly_serializer.data,
            'weekly_total_quantity': weekly_total_quantity,
            'weekly_total_amount': weekly_total_amount,
            'monthly_total_quantity': monthly_total_quantity,
            'monthly_total_amount': monthly_total_amount,
        }

        return Response(response_data, status=status.HTTP_200_OK)
