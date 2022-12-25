from django.urls import path,include
from .views import *

urlpatterns=[
    path('employee/facility/join',FacilityView.as_view(), name='employee_facilities'),
    path('employee/notes/',EmployeeNotesView.as_view(), name='employee_notes'),
    # path('employee/facility/notes',FacilityNotesView.as_view(), name='facility_notes'),
    path('employee/notes/share',ShareNotesView.as_view(), name='share'),
    path('notes/previous',PreviousNotesView.as_view(),name='previous_note'),
    path('employee/profile',StaffUploadProfileView.as_view(),name='employee_profile'),
    path('notes/shared/remove',RemoveSharedUsersView.as_view(),name='remove_shared')



    
]