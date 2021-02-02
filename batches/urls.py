from django.urls import path
from .views import *
from .api import BatchTimingAPI, NoticeAPI

urlpatterns = [
    path('batchTiming/', batchTiming, name='batchTiming'),
    path('batchTiming2/', batchTiming2, name='batchTiming2'),
    path('batchTiming-api/', BatchTimingAPI, name='batchTimingAPI'),
    path('postNotice/', postNotice, name='postNotice'),
    path('postNotice-api/', NoticeAPI, name='NoticeAPI'),
    path('batchTimingEdit/<int:id>', batchTimingEdit, name='batchTimingEdit'),
    path('Tutor/Batch/add/all', BatchTutor, name="addbatchtutor"),
    path('Tutor/Batch/batch/edit/<batch_id>',
         editBatchTutor, name="editbatchtutor"),
    path('Tutor/Batch/batch/delete/<batch_id>',
         deleteBatchTutor, name="deletebatchtutor"),
]
