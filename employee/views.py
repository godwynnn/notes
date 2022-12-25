from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from algoauth.serializers import *
from knox.auth import TokenAuthentication
from rest_framework.permissions import AllowAny
# Create your views here.
from django.core.mail import send_mail
from django.core.paginator import Paginator,PageNotAnInteger,Page,EmptyPage

from django.utils import timezone

class FacilityView(APIView):
#     def get(self,request):
#         facility_id=request.GET.get('facility_id')
#         facility=Facilities.objects.get(id=facility_id)

#         serializer=FacilitiesSerializer(facility,many=False).data
#         serializer['user']=UserSerializer(facility.user.all(), many=True).data

#         return Response({
#             'facility':serializer,
#             'status':status.HTTP_200_OK
#         })


    def post(self,request):
        facility_id=request.GET.get('facility_id')
        user_facility=Facilities.objects.all().filter(user=request.user)

        try:
            facility=Facilities.objects.get(id=facility_id)
        except ObjectDoesNotExist:
            return  Response('this facility don\'t  exists')
    
        if request.user in facility.user.all():
            return Response('user is already assinged to this facility')
        
        elif user_facility.exists():
            return Response('user cannot be assinged to more than one facility')
       
        else:
            facility.user.add(request.user)
            return Response({
                'status':'success',
                'message':f'user successfully added to {facility.name} Facility'
            })


class EmployeeNotesView(APIView):
    authentication_classes=[TokenAuthentication,]
    def post(self,request):
      
        serializer=NotesSerializer(data=request.data)
        facility=Facilities.objects.get(user=request.user)
        if serializer.is_valid():
            serializer.save()
            serializer_instance=serializer.instance
            serializer_instance.user=request.user
            serializer_instance.facility=facility
            serializer_instance.save()

            serialized_data=NotesSerializer(serializer_instance).data

            return Response({
                'note':serialized_data,
                'status':'success'
            })
        
    def get(self,request):
        
        try:
            note=Notes.objects.filter(user=request.user)
            paginator=Paginator(note,4)
            page=request.GET.get('page')
            paginator=Paginator(note,4)
            try:
                notes = paginator.page(page)
            except PageNotAnInteger:
                notes = paginator.page(1)
            except EmptyPage:
                notes = paginator.page(paginator.num_pages)
            
        # except:
        #     query=request.GET.get('query')
        #     if query == 'shared':
            shared_notes=Notes.objects.filter(shared_with=request.user)
            serialized_note=NotesSerializer(shared_notes,many=True).data
            # count=0
            # for count in range(0,len(serialized_note['shared_with'])+1):
            #     count+=1
            # print(count)
            # serialized_note['count']=len(serialized_note['shared_with'])

            
            shared=False
            if shared_notes.exists():
                shared=True

            return Response({
                'notes':NotesSerializer(notes,many=True).data,
                'shared_notes':serialized_note,
                'status': status.HTTP_200_OK,
                'liked':shared
            })
        except:
            return Response({
                'status':status.HTTP_204_NO_CONTENT
            })


# class FacilityNotesView(APIView):
#     def get(self,request):
#         facility=Facilities.objects.get(user=request.user)
#         note=Notes.objects.filter(facility=facility)

#         page=request.GET.get('page')
#         paginator=Paginator(note,4)
#         try:
#             notes = paginator.page(page)
#         except PageNotAnInteger:
#             notes = paginator.page(1)
#         except EmptyPage:
#             notes = paginator.page(paginator.num_pages)

#         return Response({
#             'notes':NotesSerializer(notes,many=True).data
#         })


class ShareNotesView(APIView):
    # permission_classes=[AllowAny,]
    authentication_classes=[TokenAuthentication,]
    def get(self,request):
        note=Notes.objects.get(id=request.GET.get('note_id'))

        user_id=request.GET.get('user_id')
        user=User.objects.get(id=user_id)

        note.shared_with.add(user)
        return Response('user added')



    def post(self,request):
        
        try:
            note=Notes.objects.get(id=request.GET.get('note_id'))


            # emails=[]

            note.shared=True
            note.save()
            for user in note.shared_with.all():
                send_mail(
                    f'Notes from {request.user.email}',
                    f' {note.note} was shared with you/',
                    request.user.email,
                    [user.email]

                )
                # note.shared_with.remove(user)
                # emails.append(user.email)
            

            return Response('shared succesfully')
        except ObjectDoesNotExist:
            return Response({
                'status':'failed',
                'message':'not sent'
            })



class PreviousNotesView(APIView):
    authentication_classes=[TokenAuthentication,]

    def get(self,request):
        facility=Facilities.objects.get(user=request.user)
        notes=list(Notes.objects.all().order_by('-date_time_added'))

        note=list(filter(lambda x: x.facility == facility and x.date_time_added < timezone.now(), notes))
        serialized_note=NotesSerializer(note[0],many=False).data
        shared_id=[]
        users=User.objects.all()
        for pk in serialized_note['shared_with']:
            # pk['user']=UserSerializer(User.objects.get(id=pk),many=False).data
            print(pk)
            shared_id.append(pk)
        print(shared_id)
        user_obj=[]
        count=0
        for user in users:
            if user.id in shared_id:
                user_obj.append(user)
                count=count+1

        serialized_note['shared_with']=UserSerializer(user_obj,many=True).data
        serialized_note['shared_count']=count
        # notes.sort()

        return Response({
            'note':serialized_note
        })
    
class StaffUploadProfileView(APIView):
    authentication_classes=[TokenAuthentication,]

    def put(self,request):
        try:
            staff=Profile.objects.get(user=request.user)
        except ObjectDoesNotExist:
            return Response('user have no profile status')
        serializer=ProfileSerializer(instance=staff,data=request.data)

        if serializer.is_valid():
            serializer.save()
            # serialized_data=ProfileSerializer(serializer,many=False).data
            return Response({
                'message':'profile updated',
                'profile':serializer.data

            })
        return Response('invalid data')
        
    def get(self,request):
        staff=Profile.objects.get(user=request.user)
        serialized_data=ProfileSerializer(staff,many=False).data
        serialized_data['user']=UserSerializer(User.objects.get(id=serialized_data['user']),many=False).data

        return  Response({
            'profile':serialized_data
        })



class RemoveSharedUsersView(APIView):
    authentication_classes=[TokenAuthentication,]
    def get(self,request):
        user=User.objects.get(id=request.GET.get('user_id'))
        try:
            note=Notes.objects.get(id=request.GET.get('note_id'))
            if request.user == note.user:

                if user in note.shared_with.all():
                    note.shared_with.remove(user)
                    return Response('user removed')
            else:
                return Response('post don\'t  belong to user')
        except:
            return Response({
                'message':'invalid data',
                'status':'failed'
            })
            
