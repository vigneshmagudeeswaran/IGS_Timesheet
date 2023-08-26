from rest_framework import serializers
from .models import Timesheet, WeeklyTimesheet

class TimeSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timesheet
        fields = ['date','hours_worked','description','day_type','timesheet_id']  # Include all fields from the model

    # Mark the 'timesheet_id' field as read-only
    timesheet_id = serializers.ReadOnlyField()
    
# class WeeklyTimesheetSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = WeeklyTimesheet
#         fields = '__all__'
#         read_only_fields = ['employee']  # Make the employee field read-only

#     def create(self, validated_data):
#         # Get the currently logged-in user and set it as the employee
#         employee = self.context['request'].user
#         validated_data['employee'] = employee
#         return super().create(validated_data)

class WeeklyTimesheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklyTimesheet
        exclude = ['employee']
        read_only_fields = [
            'timesheet_id',
            'is_approved',
            'approved_by',
        ]
        
# class WeeklyTimesheetManagerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = WeeklyTimesheet
#         fields = ['timesheet_id', 'date1', 'date2', 'date3', 'date4', 'date5', 'is_approved', 'approved_by']
#         read_only_fields = ['timesheet_id', 'date1', 'date2', 'date3', 'date4', 'date5', 'approved_by']
        
class WeeklyTimesheetManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklyTimesheet
        exclude = ['employee']
        read_only_fields = ['timesheet_id']

    def update(self, instance, validated_data):
        # Only allow the manager to edit 'is_approved' and 'approved_by' fields
        if self.context['request'].user.role == 'Manager':
            instance.is_approved = validated_data.get('is_approved', instance.is_approved)
            instance.approved_by = validated_data.get('approved_by', instance.approved_by)
            instance.save()
            return instance
        else:
            raise serializers.ValidationError("Only managers can approve time sheets.")