# cal/views.py

from datetime import datetime
from django.shortcuts import get_object_or_404

from .serializers import EventSerializer
from rest_framework.response import Response
from .utils import convert_datetime_to_str
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .permissions import IsEventOwner
from rest_framework.decorators import action
from .models import Event
from rest_framework import status

CURRENT_DATETIME_STR = convert_datetime_to_str(datetime.now())

class EventAPIView(ModelViewSet):

    serializer_class = EventSerializer
    queryset = Event.objects.all()
    permission_classes = (IsAuthenticated, IsEventOwner)
    filterset_fields = ["title"]
    ordering_fields = ["start_time"]

    def list(self, request):
        serializer = self.serializer_class(Event.objects.get_all_events(user=request.user), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, *args, **kwargs):
        data = request.data
        event = self.get_object()
        start_time = convert_datetime_to_str(event.start_time)
        end_time = convert_datetime_to_str(event.end_time)
        
        if (CURRENT_DATETIME_STR >= end_time):

            return Response(
                {"error": "Event has already ended cannot edit now"},
                status=status.HTTP_400_BAD_REQUEST
            )
                
        serializer = self.get_serializer(instance=event, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destory(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except :
            return Response({"Error: Object not Found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"Deleted event"}, status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=["GET"], name="running_events")
    def running_events(self, request, *args, **kwargs):
        serializer_data = self.serializer_class(Event.objects.get_running_events(user=request.user), many=True)
        return Response(serializer_data.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=["GET"], name="upcoming_events")
    def upcoming_events(self, request, *args, **kwargs):
        serializer_data = self.serializer_class(Event.objects.get_upcoming_events(user=request.user), many=True)
        return Response(serializer_data.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=["GET"], name="completed_events")
    def completed_events(self, request, *args, **kwargs):
        serializer_data = self.serializer_class(Event.objects.get_completed_events(user=request.user), many=True)
        return Response(serializer_data.data, status=status.HTTP_200_OK)
    

    # @action(detail=True, methods=["POST"], name="next_week")
    # def next_week(self, request, pk=None):
    #     event = self.get_object()
    #     next = event
    #     next.start_time += timedelta(days=7)
    #     next.end_time += timedelta(days=7)
    #     serializer = self.serializer_class(next)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
        
    #     return Response({"event_url": f"http://127.0.0.1:8000/calendar/event/{serializer.data["id"]}/"})
    

    # @action(detail=True, methods=["POST"], name="next_day")
    # def next_day(request, event_id):

    #     event = get_object_or_404(Event, id=event_id)
    #     if request.method == 'POST':
    #         next = event
    #         next.id = None
    #         next.start_time += timedelta(days=1)
    #         next.end_time += timedelta(days=1)
    #         next.save()
    #         return JsonResponse({'message': 'Sucess!'})
    #     else:
    #         return JsonResponse({'message': 'Error!'}, status=400)

        


