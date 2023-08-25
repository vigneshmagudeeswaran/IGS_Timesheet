from rest_framework import serializers
from .models import Timesheet

class TimeSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timesheet
        fields = ['date','hours_worked','description','day_type','timesheet_id','employee']  # Include all fields from the model

    # Mark the 'timesheet_id' field as read-only
    timesheet_id = serializers.ReadOnlyField()
    