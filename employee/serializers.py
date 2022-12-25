from rest_framework import serializers
from main.models import *
from knox.models import AuthToken
from django.core.exceptions import ObjectDoesNotExist


class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Notes
        fields='__all__'

    
        

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields='__all__'

        

        
class FacilitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Facilities
        fields='__all__'



        
class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comments
        fields='__all__'


class SecuritySerializer(serializers.ModelSerializer):
    class Meta:
        model=Security
        fields='__all__'


        