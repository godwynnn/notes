from django.urls import path,include
from .views import *

urlpatterns=[
    path('facilities',FacilityView.as_view(), name='facilities'),
    path('facility/staff/',StaffsFacilityView.as_view(), name='facility_users'),

    path('facility/create',CreateFacilityView.as_view(), name='create_facility'),
    path('facility/staff/remove',RemoveStaffFacilityView.as_view(), name='facility_users_remove'),


    path('notes/',NotesView.as_view(), name='notes'),
    path('notes/<str:pk>/',NotesDetailView.as_view(), name='note_detail'),

    path('staff/notes',StaffNotesView.as_view(), name='user_notes'),
    path('facilites/notes',FacilityNotesView.as_view(), name='facility_notes'),
    path('staffs',StaffProfileView.as_view(), name='facility_notes'),
    path('staff/profile/<str:pk>',StaffProfileDetailView.as_view(), name='facility_notes'),
    path('user/note/comments',CommentsView.as_view(), name='comments'),
    


]