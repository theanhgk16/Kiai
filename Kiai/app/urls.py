from django.urls import path, include
from . import views

urlpatterns = [
    # =====================User==========================
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup', views.signup),
    path('accounts/edit-profile', views.editProfile, name='edit-profile'),

    path('', views.home, name='home'),
    path('register/<int:id>', views.registerSubject, name='register-subject'),
    path('result/<int:id>', views.result, name='result'),
    path('exam-document', views.exam_document, name='exam-document'),
    
    
    
    
    
    
    # =====================Student=========================
    path('staff', views.listStudent, name='student-list'),
    path('staff/student-create/', views.createStudent, name='student-create'),
    path('staff/student-update/<int:id>',
         views.updateStudent, name='student-update'),
    path('staff/student-delete/<int:id>',
         views.deleteStudent, name='student-delete'),

    # =====================GenericView Subject==============
    #     path('subject/', views.SubjectListView.as_view(), name='subject-list'),
    #     path('subject/create/', views.SubjectCreateView.as_view(), name='subject-create'),
    #     path('subject/update/<int:pk>',
    #          views.SubjectUpdateView.as_view(), name='subject-update'),
    #     path('subject/update/<int:pk>',
    #          views.SubjectDeleteView.as_view(), name='subject-delete'),

    # ======================Subject========================
    path('staff/subject-list', views.listSubject, name='subject-list'),
    path('staff/subject-create', views.createSubject, name='subject-create'),
    path('staff/subject-update/<int:id>',
         views.updateSubject, name='subject-update'),
    path('staff/subject-delete/<int:id>',
         views.deleteSubject, name='subject-delete'),

    # =====================Classes========================
    path('staff/class-list', views.listClass, name='class-list'),
    path('staff/class-create', views.createClass, name='class-create'),
    path('staff/class-update/<int:id>',
         views.updateClass, name='class-update'),
    path('staff/class-delete/<int:id>',
         views.deleteClass, name='class-delete'),

    # =====================Exam===========================
    path('staff/exam-list', views.listExam, name='exam-list'),
    path('staff/exam-create', views.createExam, name='exam-create'),
    path('staff/exam-update/<int:id>',
         views.updateExam, name='exam-update'),
    path('staff/exam-delete/<int:id>',
         views.deleteExam, name='exam-delete'),

    # ====================Result==========================
    path('staff/result-list', views.listResult, name='result-list'),
    path('staff/result-create', views.createResult, name='result-create'),
    path('staff/result-update/<int:id>',
         views.updateResult, name='result-update'),
    path('staff/result-delete/<int:id>',
         views.deleteResult, name='result-delete'),
    
    # ====================Document==========================
    path('staff/document-list', views.listDocument, name='document-list'),
    path('staff/document-create', views.createDocument, name='document-create'),
    path('staff/upload-file/<int:id>', views.uploadFile, name='upload-file'),
     #=======================File Model=====================
    path('staff/set-document-status/<pk>', views.set_document_status),

]
    
