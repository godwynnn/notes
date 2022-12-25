from rest_framework import serializers
from main.models import *
from knox.models import AuthToken
from django.core.exceptions import ObjectDoesNotExist


class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Notes
        fields=['note','facility','user','date_time_added','is_deleted','shared_with','shared','comments']

    
        

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields='__all__'

        

        
class FacilitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Facilities
        fields='__all__'


# class AssignFacilitiesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=AssingFacility
#         fields='__all__'
        
class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comments
        fields='__all__'


class SecuritySerializer(serializers.ModelSerializer):
    class Meta:
        model=Security
        fields='__all__'


        