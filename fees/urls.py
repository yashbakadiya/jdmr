from django.urls import path
from .views import *
from .api import AddFeesAPI, SubmitFeesAPI

urlpatterns = [
    path('addFees/', addFeesC, name='addFeesC'),
    path('viewFees/', viewFees, name='viewFees'),
    path('submitFee/', submitFee, name='submitFee'),
    path('deleteFee/<int:id>', deleteFee, name='deleteFee'),
    path('editFee/<int:id>', editFee, name='editFee'),
    path('archiveFeeList/', archiveFeeList, name='archiveFeeList'),
    path('fees-api', AddFeesAPI, name='fees-api'),
    path('submitFee-api', SubmitFeesAPI, name='submitFee-api'),
]
