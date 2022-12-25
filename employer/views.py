from django.shortcuts import render

# Create your views here.
from .decorators import check_admin
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,DestroyAPIView,RetrieveAPIView
from rest_framework import status
from knox.auth import TokenAuthentication
from rest_framework.permissions import AllowAny
from main.models import *
from .serializers import *
from algoauth.serializers import UserSerializer
from rest_framework.response import Response
import datetime
from datetime import date
from django.core.paginator import Paginator,PageNotAnInteger,Page,EmptyPage
from django.core.exceptions import ObjectDoesNotExist

now=datetime.datetime.now()

def get_days_difference(note):
    note_year=int(note.date_time_added.year)
    note_month=int(note.date_time_added.month)
    note_day=int(note.date_time_added.day)

    current_year=now.year
    current_month=now.month
    current_day=now.day

    date1=date(note_year,note_month,note_day)
    date2=date(current_year,current_month,current_day)
    days_differ=date2-date1
    return days_differ.days



class FacilityView(ListAPIView):
    
    serializer_class=FacilitiesSerializer
    # permission_classes=[AllowAny,]
    authentication_classes=[TokenAuthentication,]
    queryset=Facilities.objects.all()
    
    


    

class CreateFacilityView(APIView):
    # permission_classes=[AllowAny,]
    authentication_classes=[TokenAuthentication,]

    @check_admin  
    def post(self,request):
        serializer=FacilitiesSerializer(data=request.data)
        if serializer.is_valid():
            serialized=serializer.save()

            serialized_data=FacilitiesSerializer(serialized).data
            return Response({
                'data': serialized_data,
                'message':'new facility created'
            })

     

     

# class UsersFacilityView(APIView):
#     permission_classes=[AllowAny,]
#     # authentication_classes=[TokenAuthentication,]
#     def get(self,request,*args,**kwargs):
#         facility_id=request.GET.get('facility_id')

#         facility=Facilities.objects.get(id=facility_id)
#         facilities=AssingFacility.objects.filter(facility=facility)

#         user_facility= AssignFacilitiesSerializer(facilities,many=True).data
        
#         for f in user_facility:
#             f['user']=UserSerializer(User.objects.get(id=f['user'])).data
#         return Response({
#             'user_facility':user_facility
#         })


    


class StaffsFacilityView(APIView):
    # permission_classes=[AllowAny,]
    authentication_classes=[TokenAuthentication,]

    
    @check_admin  
    def get(self,request,*args,**kwargs):
        facility_id=request.GET.get('facility_id')
        facility=Facilities.objects.get(id=facility_id)

        all_users=facility.user.all()
        page=request.GET.get('page')
        paginator=Paginator(all_users,4)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        
        
        serialized_users=UserSerializer(users,many=True).data
        for staff in serialized_users:
            staff['profile']=ProfileSerializer(Profile.objects.get(user__id=staff['id']),many=False).data

        return Response({
            'users':serialized_users
        })
            

    @check_admin  
    def post(self,request,*args,**kwargs):
        facility_id=request.GET.get('facility_id')
        user_id=request.GET.get('user_id')

        facility=Facilities.objects.get(id=facility_id)
        
        try:
            user=User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return Response('this user does not exist')

        if user in facility.user.all():
            return Response('this user is already assinged to this facility ')

        else:
            facility.user.add(user)
            # user=FacilitiesSerializer(facility_user,many=False).data
            return Response({
                    'message':f'user assinged to facility {facility.name}',
                    })


        



class RemoveStaffFacilityView(APIView):
    authentication_classes=[TokenAuthentication,]

    @check_admin  
    def post(self,request):
        facility_id=request.GET.get('facility_id')
        user_id=request.GET.get('user_id')

        facility=Facilities.objects.get(id=facility_id)
        try:
            user=User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return Response('this user does not exist')
    
        if user not in facility.user.all():
            return Response('this user is not  assinged to this facility ')

        else:
            facility.user.remove(user)
            return Response({
                    'message':f'user removed from facility {facility.name}',
                    })
        
    
        

        

class NotesView(APIView):
    serializer_class=NotesSerializer
    permission_classes=[]
    authentication_classes=[TokenAuthentication,]

    @check_admin 
    def get(self,request):
        note=Notes.objects.all()
        page=request.GET.get('page')
        paginator=Paginator(note,4)
        try:
            notes = paginator.page(page)
        except PageNotAnInteger:
            notes = paginator.page(1)
        except EmptyPage:
            notes = paginator.page(paginator.num_pages)

        return Response({
            'notes':NotesSerializer(notes,many=True).data
        })
    
    
       


class NotesDetailView(APIView):
    # authentication_classes=[TokenAuthentication,]
    permission_classes=[AllowAny,]

    def get(self,request,pk):
        note=Notes.objects.get(id=pk)
        return Response({
            'note':NotesSerializer(note,many=False).data
        })

    
    @check_admin 
    def delete(self,request,pk):
        note=Notes.objects.get(pk=pk)
        # date_differ=datetime.datetime.now().strftime(('%Y-%m-%d')) - note.date_time_added.strftime('%Y-%m-%d')
        # date_differ=datetime.datetime.strptime(str(datetime.datetime.now()).strip(),'%Y-%m-%d') -datetime.datetime.strptime( str(note.date_time_added).strip(),'%Y-%m-%d')
        
        
        days=get_days_difference(note)
        print(days)
        
        if days >= 60:
            note.delete()
            return Response('note deleted')
        else:
            return Response({
                'message':'can\'t delete a note less that 60days of upload',
                'status': 'failed'
            })

    


    

class StaffNotesView(APIView):
    authentication_classes=[TokenAuthentication,]

    @check_admin  
    def get(self,request):
        user_id=request.GET.get('user_id')
        try:
            user=User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return Response('this user does not exist')
    
        notes=Notes.objects.filter(user=user)
        serialized_notes=NotesSerializer(notes,many=True).data
        # comment_id=[]
        # for note in serialized_notes:
        #     note['comments']=CommentsSerializer(note.comments.all(), many=True).data

        return Response({
            'notes':serialized_notes
        })
    


class FacilityNotesView(APIView):
    @check_admin  
    def get(self,request):
        facility=Facilities.objects.get(id=request.GET.get('facility_id'))
        note=Notes.objects.filter(facility=facility)
        paginator=Paginator(note,4)
        page=request.GET.get('page')
        paginator=Paginator(note,4)
        try:
            notes = paginator.page(page)
        except PageNotAnInteger:
            notes = paginator.page(1)
        except EmptyPage:
            notes = paginator.page(paginator.num_pages)

        return Response({
            'notes':NotesSerializer(notes,many=True).data
        })
    

class StaffProfileView(APIView):
    @check_admin  
    def get(self,request):

        try:
        
            all_staffs=Profile.objects.filter(user__is_staff=True,user__email__icontains=request.GET.get('email'))
        except:
            all_staffs=Profile.objects.filter(user__is_staff=True)
        
        
        paginator=Paginator(all_staffs,4)
        page=request.GET.get('page')
        paginator=Paginator(all_staffs,4)
        try:
            staffs = paginator.page(page)
        except PageNotAnInteger:
            staffs = paginator.page(1)
        except EmptyPage:
            staffs = paginator.page(paginator.num_pages)

        serialized_staff=ProfileSerializer(staffs,many=True).data
        for staff in serialized_staff:
            staff['user']=UserSerializer(User.objects.get(id=staff['user']),many=False).data

        return Response({
            'staff':serialized_staff
        })

class StaffProfileDetailView(APIView):

    @check_admin  
    def get(self,request,pk):
        staff=Profile.objects.get(id=pk)
        serialized_staff=ProfileSerializer(staff,many=False).data
        serialized_staff['user']=UserSerializer(User.objects.get(id=serialized_staff['user']),many=False).data

        return Response({
            'staff':serialized_staff
        })
        

class CommentsView(APIView):
    def get(self,request,pk):
        comments=Comments.objects.filter(note__id=pk)
        serialized_comments=CommentsSerializer(comments,many=True).data
        for comment in serialized_comments:
            comment['user']=UserSerializer(User.objects.get(id=comment['user'],many=False)).data

        
        return Response({
            'comments':serialized_comments
        })


