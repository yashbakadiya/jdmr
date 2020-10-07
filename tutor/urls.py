from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('test1/', views.test1, name='test1'),
    path('test2/', views.test2, name='test2'),
    path('submitFee/', views.submitFee, name='submitFee'),
    path('testing/', views.testing, name='testing'),
    path('', views.landing, name='landing'),
    path('searchUserStudent/', views.searchUserStudent, name='searchUserStudent'),
    path('addStudentDetail/<int:sno>', views.addStudentDetail, name='addStudentDetail'),
    path('addStudentInst/<int:snum>', views.addStudentInst, name='addStudentInst'),
    path('addTutors/', views.addTutors, name='addTutors'),
    path('addCourses/', views.addCourses, name='addCourses'),
    path('addFees/', views.addFeesC, name='addFeesC'),
    path('addStudents/', views.addStudents, name='addStudents'),
    path('addTutorWork/', views.addTutorWork, name='addTutorWork'),
    path('addTutorInst/<int:sno>', views.addTutorInst, name='addTutorInst'),
    path('archiveCourse/', views.archiveCourse, name='archiveCourse'),
    path('archiveCourseList/', views.archiveCourseList, name='archiveCourseList'),
    path('archiveTutor/', views.archiveTutor, name='archiveTutor'),
    path('archiveStudent/', views.archiveStudent, name='archiveStudent'),
    path('archiveTutorList/', views.archiveTutorList, name='archiveTutorList'),
    path('archiveFees/', views.archiveFees, name='archiveFees'),
    path('batchTiming/', views.batchTiming, name='batchTiming'),
    path('batchTimingEdit/<int:sno>', views.batchTimingEdit, name='batchTimingEdit'),
    path('archiveFeeList/', views.archiveFeeList, name='archiveFeeList'),
    path('deleteArchiveFees/<int:sno>',views.deleteArchiveFee,name='deleteArchiveFee'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboardStudent/', views.dashboardStudent, name='dashboardStudent'),
    path('dashboardTutor/', views.dashboardTutor, name='dashboardTutor'),
    path('deleteCourse/<int:s_num>', views.deleteCourse, name='deleteCourse'),
    path('deleteArchiveCourse/<int:s_num>', views.deleteArchiveCourse, name='deleteArchiveCourse'),
    path('deleteStudent/<int:sno>', views.deleteStudent, name='deleteStudent'),
    path('deleteTutor/<int:sno>', views.deleteTutor, name='deleteTutor'),
    path('deleteFee/<int:sno>', views.deleteFee, name='deleteFee'),
    path('editCourse/<int:s_num>', views.editCourse, name='editCourse'),
    path('editTutor/<int:sno>', views.editTutor, name='editTutor'),
    path('editTutorMini/<int:sno>', views.editTutorMini, name='editTutorMini'),
    path('editStudent/<int:sno>', views.editStudent, name='editStudent'),
    path('editFee/<int:sno>', views.editFee, name='editFee'),
    path('enrollTutor/', views.enrollTutor, name='enrollTutor'),
    path('enrolledTutors/', views.enrolledTutors, name='enrolledTutors'),
    path('enrolledStudents/', views.enrolledStudents, name='enrolledStudents'),
    path('loginTutor/', views.loginTutor, name='loginTutor'),
    path('logoutTutor/', views.logoutTutor, name='logoutTutor'),
    path('loginCoachingCentre/', views.loginCoachingCentre, name='loginCoachingCentre'),
    path('logoutCoachingCentre/', views.logoutCoachingCentre, name='logoutCoachingCentre'),
    path('loginStudent/', views.loginStudent, name='loginStudent'),
    path('logoutStudent/', views.logoutStudent, name='logoutStudent'),
    path('mainPage/', views.mainPage, name='mainPage'),
    path('postTution/', views.postTution, name='postTution'),
    path('postAssignment/', views.postAssignment, name='postAssignment'),
    path("profileCoachingCentre/", views.profileCoachingCentre),
    path("profileStudent/", views.profileStudent),
    path("profileTutor/", views.profileTutor),
    path('search/', views.search, name='search'),
    path('searchStudent/', views.searchStudent, name='searchStudent'),
    path('searchteachType/', views.searchteachType, name='searchteachType'),
    path('signupTutor/', views.signupTutor, name='signupTutor'),
    path('signupCoachingCentre/', views.signupCoachingCentre, name='signupCoachingCentre'),
    path('signupTutorContinued/<int:sno>', views.signupTutorContinued, name='signupTutorContinued'),
    path('signupStudent/', views.signupStudent, name='signupStudent'),
    path('searchTutor/', views.searchTutor, name='searchTutor'),
    path('searchUserTutor/', views.searchUserTutor, name='searchUserTutor'),
    path('searchFee/', views.searchFee, name='searchFee'),
    path('teachingType/', views.teachingType, name='teachingType'),
    path('viewCourses/', views.viewCourses, name='viewCourses'),
    path('viewteachingType/', views.viewteachingType, name='viewteachingType'),
    path('viewteachType/', views.viewteachType, name='viewteachType'),
    path('viewTutors/', views.viewTutors, name='viewTutors'),
    path('viewTutorInst/', views.viewTutorInst, name='viewTutorInst'),
    path('viewStudents/', views.viewStudents, name='viewStudents'),
    path('viewFees/', views.viewFees, name='viewFees'),
    path('viewTution/', views.viewTution, name='viewTution'),
    path('viewAssignment/', views.viewAssignment, name='viewAssignment'),
    path('editTution/<int:sno>', views.editTution, name='editTution'),
    path('editAssignment/<int:sno>', views.editAssignment, name='editAssignment'),
    path('enrolledInstututesTutor/', views.enrolledInstututesTutor, name='enrolledInstututesTutor'),
    path('enrolledInstututesStudent/', views.enrolledInstututesStudent, name='enrolledInstututesStudent'),
    path("tutorCalendar/", views.tutorCalendar),
    path('viewAssignmentTutor/', views.viewAssignmentTutor, name='viewAssignmentTutor'),
    path('ajaxLocation/', views.ajaxLocation, name='ajaxLocation'),
    path('makeAppointment/', views.makeAppointment, name='makeAppointment'),
    path('loginAll/', views.loginAll, name='loginAll'),
    path('archiveStudentList/', views.archiveStudentList, name='archiveStudentList'),
    path('editTeachingType/<int:sno>', views.editTeachingType, name='editTeachingType'),
    path('deleteArchiveTutorList/<int:sno>', views.deleteArchiveTutorList, name='deleteArchiveTutorList'),
    path('deleteArchiveStudent/<int:sno>', views.deleteArchiveStudent, name='deleteArchiveStudent'),
    path('removeFromArchiveStudent/',views.removeFromArchiveStudent,name='removeFromArchiveStudent'),
    path('undoArchiveTutor/',views.undoArchiveTutor,name='undoArchiveTutor'),
    path('undoArchiveFees/',views.undoArchiveFees,name='undoArchiveFees'),
    path('searchCoachingCenter/',views.searchCoachingCenter,name='searchCoachingCenter'),
    path('postNotice/',views.postNotice,name='postNotice'),
    path('getNotices/',views.getNotices,name='getNotices'),
    # Tutorials Institute Urls
    path('tutorials/Add',views.addTutorialsInstitute,name="addtutorials"),
    path('tutorials/Add/Videos/<course_id>',views.addTutorialsInstituteVideos,name="addplaylist"),
    path('tutorials/viewTutorials',views.ViewTutorials,name="viewtutorials"),
    path('tutorials/Edit/<course_id>',views.EditTutorialsInstitute,name="editTutorial"),
    path('tutorials/delete/<course_id>',views.DeleteTutorialsInstitute,name="deletetutorial"),
    path('tutorials/Watch/<course_id>',views.WatchTutorialsInstitute,name="viewtutorial"),
    path('tutorials/Archive',views.ArchiveTutorials,name="archivetutorials"),
    path('tutorials/Watch/Edit/<playlist_id>',views.EditTutorialsInstituteVideos,name="editTutorialvideos"),
    path('tutorials/Watch/Delete/<playlist_id>',views.DeleteTutorialsInstituteVideos,name="deleteplaylistvideo"),
    # Tutorials Tutor Urls
    path('tutorials/Tutor/add',views.addTutorialsTutor,name='tutorialstutor'),
    path('tutorials/Tutor/Add/Videos/<course_id>',views.addTutorialsTutorVideos,name='addvideosTutor'),
    path('tutorials/Tutor/viewTutorials',views.ViewTutorialsTutor,name="viewtutorialstutor"),
    path('tutorials/Tutor/Edit/<course_id>',views.EditTutorialsTutor,name="editTutorialtutor"),
    path('tutorials/Tutor/delete/<course_id>',views.DeleteTutorialsTutor,name="deletetutorialstutor"),
    path('tutorials/Tutor/Watch/<course_id>',views.WatchTutorialsTutor,name="viewtutorialtutor"),
    path('tutorials/Tutor/Archive',views.ArchiveTutorialsTutor,name="archivetutorialstutor"),
    path('tutorials/Tutor/Watch/Edit/<playlist_id>',views.EditTutorialsTutorVideos,name="editTutorialvideostutor"),
    path('tutorials/Tutor/Watch/Delete/<playlist_id>',views.DeleteTutorialsTutorVideos,name="deleteplaylistvideotutor"),
    path('tutorials/search',views.SearchCourses,name="searchcourses"),
    path('tutorials/Student/Watch/<course_id>',views.WatchTutorTutorials,name="watchTutorcourse"),
    path('tutorials/Student/Watch/Institute/<course_id>',views.WatchInstituteTutorials,name="watchInstitutecourse"),
    path('tutorials/Tutor/delete/<course_id>',views.DeleteTutorialsTutor,name="deletetutorialstutor"),
    path('forgotpass',views.forgotpass,name="forgotpass"),
    path('tutorial/search',views.SearchBar,name="searchtutorial"),
    path("getOTP/",views.getOTP,name="getOTP"),
    path("tutorials/Student/Review/Tutor/<Course_id>",views.PostReviewTutor,name="tutorreview"),
    path("tutorials/Student/Review/Instutute/<Course_id>",views.PostReviewInstitute,name="institutereview"),
    path('Review/Institutes/<inst_id>',views.ReviewInstitute,name="reviewinstitute"),
    path('Review/Tutor/<tutor_id>',views.ReviewTutors,name="reviewtutor"),
    path('classes',views.FindClases,name="classes"),
    path('Exams/Add',views.AddExam,name="addexam"),
    path('Exams/view/all',views.ListExams,name='viewexams'),
    path('Exams/toggle/<exam_id>',views.ToggleExam,name='toggle'),
    path('Exams/delete/<exam_id>',views.deleteExam,name='deleteexam'),
    path('Exams/edit/<exam_id>',views.Editexam,name='editexam'),
    path('Questions/all/add',views.QuestionsSection,name="questionsection"),
    path('Questions/add/<exam_id>',views.CreateQuestions,name='questions'),
    path('Exam/Questions/edit/all',views.EditExamQuestions,name="editexamquestions"),
    path('Exam/Questions/edit/<exam_id>',views.EditQuestions,name="editquestions"),
    path('Exam/Questions/shortquestions/edit/<question_id>',views.EditShortQuestions,name='shortansedit'),
    path('Exam/Questions/longquestions/edit/<question_id>',views.EditLongQuestions,name='longansedit'),
    path('Exam/Questions/booleanquestions/edit/<question_id>',views.EditBooleanQuestions,name='booleanansedit'),
    path('Exam/Questions/multiplequestions/edit/<question_id>',views.EditMultipleQuestions,name='multipleansedit'),
    path('Exam/Questions/shortquestions/delete/<question_id>',views.DeleteShortQuestions,name='shortansdelete'),
    path('Exam/Questions/longquestions/delete/<question_id>',views.DeleteLongQuestions,name='longansdelete'),
    path('Exam/Questions/booleanquestions/delete/<question_id>',views.DeleteBooleanQuestions,name='booleanansdelete'),
    path('Exam/Questions/multiplequestions/delete/<question_id>',views.DeleteMultipleQuestions,name='multipleansdelete'),
    path('Student/Exams/All',views.StudentExamsAll,name="studentexams"),
    path('Student/Calculator',views.calculator,name="calc"),
    path('Student/Exam/<pk>',views.instruction,name="instruction"),
    path('Student/Exam/start/<pk>',views.start_exam,name="start_exam"),
    path('Student/all/Questions/<pk>',views.view_questions,name="view_questions"),
    path('student/Exam/Submitted',views.submitted,name="submitted"),
    path('Student/Exam/Store/Data',views.store_data,name="store_data"),
# saving results
    # Saving Answers
    path('multiple_ans/', views.multiple_ans, name='multiple_ans'),
    path('short_ans/', views.short_ans, name='short_ans'),
    path('long_ans/', views.long_ans, name='long_ans'),
    path('tof_ans/', views.tof_ans, name='tof_ans'),
# Student Result Section
    path('Student/Exams/Result/All',views.ViewExamsResult,name="studentexamresults"),
    path('Student/Exam/Result/Detailed/Report/<int:pk>',views.detailed_result,name="detailed_report"),
#Center Result Section
    path('Center/Exams/Result/All',views.CoachingResultStudent,name="centerexamresults"),
    path('Center/Exams/Result/Exam/<exam_id>',views.GetExamResults,name="getexamresults"),
    path('Center/Exam/Result/Student/<student_id>/<exam_id>',views.GetStudentResults,name="studentresult"),
    path('Center/Result/Review/Answer/<question_id>',views.Review_Answer,name="check_answer"),
    path('Center/Result/Anotate/<id>/<pk>',views.webViewerAnnotate,name="anotatePdfViewer"),
    path('Center/Result/Anotate/pdf/<id>/<pk>',views.annotateAnswers,name="anotate"),
# Batch Tutor Timings
    path('Tutor/Batch/add/all',views.BatchTutor,name="addbatchtutor"),
    path('Tutor/Batch/batch/edit/<batch_id>',views.editBatchTutor,name="editbatchtutor"),
    path('Tutor/Batch/batch/delete/<batch_id>',views.deleteBatchTutor,name="deletebatchtutor"),
# Exam Section Tutor
    path('Tutor/Exam/Add/All',views.ExamTutor,name="examtutor"),
    path('Tutor/Exams/View/all',views.ViewExamTutor,name="viewexamstutor"),
    path('Tutor/Exam/Edit/<exam_id>',views.EditExamTutor,name="edittutorexams"),
    path('Tutor/add/Question/Exam/all',views.addQuestionsTutor,name="addquestionstutor"),
    path('Tutor/Question/<exam_id>',views.CreateQuestionsTutor,name="createquestionstutor"),
    path('Tutor/Questions/Edit/all',views.EditExamQuestionsTutor,name="questionalltutor"),
    path('Tutor/Question/edit/<exam_id>',views.EditQuestionsTutor,name="editquestionstutor"),
    path('Tutor/Exam/Questions/shortquestions/edit/<question_id>',views.EditShortQuestionsTutor,name='shortansedittutor'),
    path('Tutor/Exam/Questions/longquestions/edit/<question_id>',views.EditLongQuestionsTutor,name='longansedittutor'),
    path('Tutor/Exam/Questions/booleanquestions/edit/<question_id>',views.EditBooleanQuestionsTutor,name='booleanansedittutor'),
    path('Tutor/Exam/Questions/multiplequestions/edit/<question_id>',views.EditMultipleQuestionsTutor,name='multipleansedittutor'),
# Coaching Center Notes Urls    
    path('Center/Notes/add',views.AddNotesInstitute,name="addnotes"),
    path('Center/Notes/View/All',views.ViewNotesInstitute,name="viewnotes"),
    path('Center/Notes/View/<note_id>',views.PdfViewNoteInstitute,name="pdfviewnoteinstitute"),
    path('Center/Notes/Edit/<note_id>',views.EditNoteInstitute,name="editnoteinstitute"),
    path('Center/Notes/Delete/<note_id>',views.DeleteNoteInstitute,name="deletenoteinstitute"),
# Tutor Notes Urls    
    path('Tutor/Notes/add',views.AddNotesTutor,name="addnotestutor"),
    path('Tutor/Notes/View/All',views.ViewNotesTutor,name="viewnotestutor"),
    path('Tutor/Notes/View/<note_id>',views.PdfViewNoteTutor,name="pdfviewnotetutor"),
    path('Tutor/Notes/Edit/<note_id>',views.EditNoteTutor,name="editnotetutor"),
    path('Tutor/Notes/Delete/<note_id>',views.DeleteNoteTutor,name="deletenotetutor"),
# Student Notes urls
    path('Student/Notes/All',views.AllNotesStudent,name="notesstudents"),
    path('Student/Center/note/<note_id>',views.ViewpdfStudentInstitute,name="viewpdfinstitute"),
    path('Student/Tutor/<note_id>',views.ViewpdfTutor,name="viewpdftutor"),
    ]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
# urlpatterns += [path('<path:dump>/',views.pageNotFound)]
