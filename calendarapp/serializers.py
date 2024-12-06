from rest_framework import serializers
from calendarapp.models import Event
from datetime import datetime
from .utils import convert_datetime_to_str

class EventSerializer(serializers.ModelSerializer):

    start_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", input_formats=["%Y-%m-%d %H:%M:%S"])
    end_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", input_formats=["%Y-%m-%d %H:%M:%S"])

    class Meta:
        model = Event
        fields = "__all__"
        extra_kwargs = {
            "user": {"read_only": True}
        }

    def validate(self, attrs):

        title = attrs.get('title', None)
        start_time = attrs.get('start_time', None)
        end_time = attrs.get('end_time', None)
        
        if start_time and end_time and start_time > end_time:
            raise serializers.ValidationError(
                "Invalid start_datetime and end_datetime. It should follow (end_datetime > start_datetime).")
        
        if end_time and convert_datetime_to_str(end_time) < convert_datetime_to_str(datetime.now()):
            raise serializers.ValidationError(
                "Invalid end_time, end_time cannot be before current time. It should follow (end_time > current_time)"
            )
        
        if start_time and convert_datetime_to_str(start_time) < convert_datetime_to_str(datetime.now()):
            raise serializers.ValidationError(
                "Invalid start_datetime, start_datetime cannot be before event creation datetime.")
        

        return attrs