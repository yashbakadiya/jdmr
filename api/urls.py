from django.urls import path, include
from .views import *

urlpatterns = [
    # AUTH Coaching Center
 	path('login/<str:username>/<str:password>',logincoachingentre,name="logincoaching"),
 	path('signup',signupCoachingCentre,name="signupcoaching"),
 	# AUTH Tutor
 	# AUTH Student
 	# Models
	path('courses/center',CoursesCentre,name="addlistcourse"),
	path('courses/center/<pk>',CoursesCentreEdit,name="editcourses"),
	path('courses/Archived/center',ArchivedCoursesCentre,name="archivecoursescenter"),
	path('center/Archived/remove',RemoveArchivedCoursesCentre,name="removearchivecoursescenter"),
	path('center/Teaching/all',TeachingTypeCenter,name="teachingtypecenter"),
	path('center/Teaching/edit/<pk>',TeachingTypeEdit,name="editteachingtypecenter"),
	path('center/Batch/all',BatchTimingCenter,name="batchcenter"),
	path('center/Batch/edit/<pk>',BatchTimingEdit,name="editbatchcenter"),
	path('center/Fees/all',AddFeesCenter,name="feescenter"),
	path('center/Fees/edit/<pk>',AddFeesEdit,name="editfeescenter"),
	path('center/Fees/Archived',ArchiveFeesCentre,name="archivefeescenter"),
	path('center/Fees/Archived/remove',RemoveArchiveFeesCentre,name="removearchivefeescenter"),
	path('SearchFees',SearchFeesCenter,name="searchfeescenter"),
	path('SubmitFees',SubmitFeesCenter,name="submitfeescenter"),
	path('SearchuserTutor',SearchTutorCenter,name="searchusertutor"),
	path('Center/add/Tutor',addTutors,name="addtutor"),
	path('center/Tutor/delete/<pk>',DeleteTutorInstitute,name="deletetutorinstitute"),
	path('center/Tutor/Edit/<pk>',EditTutorInstitute,name="edittutorinstitute"),
	path('center/Tutor/Archive/<pk>',ArchiveTutors,name="archivetutorinstitute"),
	path('center/Tutor/Archive/all',archiveTutorList,name="archivetutorlistinstitute"),
	path('center/Tutor/Archive/Delete/<pk>',deleteArchiveTutor,name="deletearchivetutorinstitute"),
	path('Center/add/Student',addStudents,name="addstudent"),
	path('Center/Student/All',viewStudents,name="studentlistcenter"),
	path('Center/Student/Archive/All',archiveStudentList,name="archivestudentlistcenter"),
	path('center/Student/Archive/All',archiveStudent,name="archivestudentlistinstitute"),
	path('center/Student/Archive/Remove',removeFromArchiveStudent,name="removearchivestudentlistinstitute"),
	path('center/Student/delete/<pk>',deleteStudent,name="deletestudentinstitute"),
	path('center/Student/Archive/delete/<pk>',deleteArchiveStudent,name="deletearchivestudentinstitute"),
	path('center/Student/Edit/<pk>',editStudent,name="editstudentinstitute"),
	#Tutorials Institute
	path('center/Tutorials',AddTutorialCenter,name="addtutorialsinstitute"),
	path('center/Tutorials/Add/Video/<pk>',AddTutorialCenterVideo,name="addtutorialsvideoinstitute"),
	path('center/Tutorials/Archive/All',ArchiveTutorialslist,name="archivetutorialinstitute"),
	path('center/Tutorials/Remove/Archive',UnArchiveTutorials,name="removearchivetutorialinstitute"),
	path('center/Tutorials/Video/Edit/<pk>',EditDeleteTutorials,name="edittutorialinstitute"),
	path('center/Tutorials/Watch/<course_id>',WatchTutorialsInstitute,name="watchtutorialinstitute"),
	path('center/Tutorials/Video/Edit/<playlist_id>',EditTutorialsInstituteVideos,name="edittutorialvideoinstitute"),
	path('center/Tutorials/Video/Delete/<playlist_id>',DeleteTutorialsInstituteVideos,name="deletetutorialvideoinstitute"),

	path('center/Notes/Add',AddNotesInstitute,name="addnotesinstitute"),
	path('center/Notes/View/All',ViewNotesInstitute,name="viewnotesinstitute"),
	path('center/Notes/View/Note/<note_id>',PdfViewNoteInstitute,name="viewnotepdfinstitute"),
	path('center/Notes/Edit/<note_id>',EditNoteInstitute,name="editnoteinstitute"),
	path('center/Notes/Delete/<note_id>',DeleteNoteInstitute,name="deletenoteinstitute"),
	path('center/Notes/Search/<search>',SearchNotes,name="searchnotesinstitute"),

# Result Coaching Center
	path('center/Result/View/All',CoachingResult,name="viewresultallinstitute"),
	path('center/Result/View/Exam/<exam_id>',GetExamResults,name="viewresultinstitute"),
	path('center/Result/View/Exam/Student/<student_id>/<exam_id>',GetStudentResults,name="viewstudentresultinstitute"),


######################################## Tutor Apis ##########################################################
	path('Tutor/Profile',profileTutor,name="profiletutorapi"),
	path('Tutor/Login',loginTutor,name="logintutorapi"),
	path('Tutor/Signup',signupTutor,name="signuptutorapi"),
	path('Tutor/Signup/Continued',signupTutorContinued,name="signuptutorcontinuedapi"),
	path('center/Exam/Search/enrolledstudent',enrolledStudents,name="searchenrolledstudent"),
	path('center/Exam/Search/searchassignmentstudent',viewAssignmentTutor,name="searchassignmentstudent"),
	path('Tutor/Tutorials/Add',AddTutorialTutor,name="addtutorialstutor"),
	path('Tutor/Tutorials/Video/Add/<pk>',AddTutorialTutorVideo,name="addtutorialsvideotutor"),
	path('Tutor/Tutorials/Archive/All',ArchiveTutorialstutorlist,name="archivetutorialstutorall"),
	path('Tutor/Tutorials/Archive',ArchiveTutorialstutor,name="archivetutorialstutor"),
	path('Tutor/Tutorials/Edit/Delete/<pk>',EditDeleteTutorialstutor,name="edittutorialstutor"),
	path('Tutor/Tutorials/Watch/<course_id>',WatchTutorialsTutor,name="watchtutorialstutor"),
	path('Tutor/Tutorials/Edit/Video/<playlist_id>',EditTutorialsTutorVideos,name="edittutorialsvideotutor"),
	path('Tutor/Tutorials/Delete/Video/<playlist_id>',DeleteTutorialsTutorVideos,name="deletetutorialsvideotutor"),
	path('Tutor/Batch/Add',AddBatchTutor,name="addbatchtutorapi"),
	path('Tutor/Search/Tutorial',SearchTutorialsTutor,name="searchtutorialtutor"),
	path('Tutor/Note/All/Add',AddNotesTutor,name="notestutor"),
	path('Tutor/Note/add/<note_id>',EditNoteTutor,name="editdeletenotestutor"),
	path('Tutor/Note/pdf/View/<note_id>',PdfViewNoteTutor,name="pdfviewnotestutor"),
	path('Tutor/Note/Search',SearchNotesTutor,name="searchnotestutor"),
	
	# Exam APIs
	path('Tutor/Exam/All/Add',ExamTutor,name="addlistexamtutor"),
	path('center/Exam/Add',AddExamInstitute,name="addexaminstitute"),
	path('center/Exam/All',ListExams,name="examlistinstitute"),
	path('center/Exam/Toggle/<exam_id>',ToggleExam,name="toggleexam"),
	path('center/Exam/Edit/<exam_id>',Editexam,name="editexam"),
	path('center/Exam/Delete/<exam_id>',deleteExam,name="deleteexam"),
	path('center/Exam/Search/<search>',SearchExam,name="searchexam"),
	path('center/Exam/Questions/Add/<exam_id>',CreateQuestionsCenter,name="addhexamquestions"),
	path('center/Exam/Questions/All/get/<exam_id>',QuestionsCenter,name="showexamquestions"),
	path('Exam/Questions/Short/Edit/<question_id>',EditShortQuestionsTutor,name="editshortquestions"),
	path('Exam/Questions/Boolean/Edit/<question_id>',EditBooleanQuestionsTutor,name="editbooleanquestions"),
	path('Exam/Questions/Multiple/Edit/<question_id>',EditMultipleQuestionsTutor,name="editmultiplequestions"),
	path('Exam/Questions/Long/Edit/<question_id>',EditLongQuestionsTutor,name="editlongquestions"),
	path('Exam/Answers/Multiple/Ans/Save',multiple_ans,name="savemultipleansapi"),
	path('Exam/Answers/Short/Ans/Save',short_ans,name="saveshortansapi"),
	path('Exam/Answers/Long/Ans/Save',long_ans,name="savelongansapi"),
	path('Exam/Answers/Boolean/Ans/Save',tof_ans,name="savebooleanansapi"),
	path('Student/Answers/All/<exam_id>',StudentAnswersAll,name="studentanswersall"),

######################################## Student Apis ##########################################################
	path('Student/Login/All',loginStudent,name="loginstudentapi"),
	path('Student/Signup',signupStudent,name="signupstudentapi"),
	path('Student/profile',profileStudent,name="profilestudentapi"),
	path('Student/profile/search/coaching/center',searchCoachingCenter,name="searchcoachingcenterapi"),
	path('Student/profile/search/tutor',enrolledTutors,name="searchtutorsapi"),
	path('Student/Post/Assignment/Add',postAssignment,name="addassignmentsapi"),
	path('Student/Post/Tutor/Requirement/Add',postTution,name="posttutorrequirementapi"),
	path('Student/Search/Tutorials',SearchCourses,name="searchtutorialsapi"),
	path('Student/Search/notes/All',StudentNotesAll,name="studentnotesallapi"),
	path('Student/Search/notes/<srch>',SearchNotes,name="searchnotesapi"),
	path('Student/Exam/Result/All',StudentExamsResultAll,name="studentresultsapi"),
	path('Student/Exam/All',StudentExamsAll,name="studentexamsallsapi"),
	path('Student/Post/Tutorial/Tutor/Review/<Course_id>',PostReviewTutorTutorials,name="tutortutorialreviewsapi"),
	path('Student/Post/Tutorial/Institute/Review/<Course_id>',PostReviewInstituteTutorials,name="centertutorialreviewsapi"),
	path('Institute/Detail/<pk>',InstitutesDetails,name="centerdetailapi"),
	path('Tutor/Detail/<pk>',TutorsDetail,name="tutordetailapi"),
## Review Tutor and Institute
	path('Institute/Review/Add/All/<inst_id>',ReviewInstitute,name="centerreviewapi"),
	path('Tutor/Review/Add/All/<tutor_id>',ReviewTutors,name="tutorreviewapi"),

]
