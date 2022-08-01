import doctest
from stat import filemode
from django.contrib.auth import login, authenticate
from .forms import MyUserCreationForm
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import re
import json
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
# Create your views here.


def signup(request):
    student = User.objects.all().order_by('-id')[0]
    code = student.code
    res = re.sub(r'[0-9]+$',
                 lambda x: f"{str(int(x.group())+1).zfill(len(x.group()))}",
                 code)
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=user.username,
                                password=request.POST['password1'])
            login(request, user)
            return redirect('home')
    return render(request, 'registration/signup.html', {'form': form, 'res': res})

@login_required
def editProfile(request):
    if request.method =='POST':
        form = MyUserChangeForm(request.POST,instance= request.user)
        if form.is_valid():
            form.save()
    form = MyUserChangeForm(instance= request.user)
    return render(request, 'user/profile.html',{'form':form})
 
# =============================USER=============================


@login_required
def home(request):
    queryParams = request.GET
    subjects = Subject.objects.all()
    enrolled = Enrollment.objects.filter(
        user_id=request.user.pk).values_list('subject_id', flat=True)
    context = {
        'queryParams': queryParams,
        'subjects': subjects,
        'enrolled': enrolled
    }
    return render(request, 'user/home.html', context)


@login_required
def registerSubject(request, id):
    subject = get_object_or_404(Subject, pk=id)
    student = get_object_or_404(User, pk=request.user.pk)
    form = EnrollmentForm()
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        Enrollment.objects.create(
            subject=get_object_or_404(Subject, pk=request.POST['id']),
            user=request.user,
            note=request.POST['note']
        )
        subject.save()
        return JsonResponse({'success': True})
    return render(request, 'user/register.html', {'form': form, 'subject': subject, 'student': student})


def result(request, id):
    subject = get_object_or_404(Subject, pk=id)
    student = get_object_or_404(User, pk=request.user.pk)
    exams = Exam.objects.filter(subject=subject)
    results = Result.objects.filter(
        student=request.user).values_list('exam_id', 'point')
    data = list()
    for result in results:
        data.insert(result[0], result[1])
    return render(request, 'user/result.html', {'subject': subject, 'student': student, 'exams': exams, 'data': data})
    # return render(request, 'user/result.html')
# =================================== STAFF ==============================


def createSearchUrl(keyword, from_date):
    from_date = from_date or ''
    return f'?keyword={keyword}&from_date={from_date}'


@login_required
def listStudent(request):
    # print(request.method)
    if request.GET.get('keyword') or request.GET.get('from_date'):
        keyword = request.GET.get('keyword')
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')
        students = User.objects.filter(Q(code__contains=keyword)
                                       | Q(name__contains=keyword) | Q(address__contains=keyword) | Q(cmnd__contains=keyword))
        if from_date or to_date:
            students = students.filter(birthday__range=(from_date, to_date))
    else:
        keyword = ''
        from_date = ''
        students = User.objects.all()

    paginator = Paginator(students, 2)  # Show number contacts per page.
    page_number = request.GET.get('page', 1)
    students = paginator.get_page(page_number)
    try:
        students = paginator.page(page_number)
    except EmptyPage:
        students = paginator.page(paginator.num_pages)
    searchUrl = createSearchUrl(keyword, from_date)
    filters = {
        'keyword': request.GET.get('keyword', ''),
        'from_date': request.GET.get('from_date'),
        'to_date': request.GET.get('to_date'),
    }
    return render(request, 'student/list.html', {'students': students, 'searchUrl': searchUrl, 'filters': filters})


@login_required
def createStudent(request):
    student = User.objects.all().order_by('-id')[0]
    # print(student)
    code = student.code
    #  sử dụng fstring tạo chuỗi
    # dùng zfill diền vào các giá trị sau khi tăng
    res = re.sub(r'[0-9]+$',
                 lambda x: f"{str(int(x.group())+1).zfill(len(x.group()))}",
                 code)
    # kết quả
    # print("Chuỗi tăng dần: " + str(res))

    form = MyUserChangeForm()
    form.fields['code'].initial = res
    if request.method == 'POST':
        form = MyUserChangeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student-list')
    return render(request, 'student/form.html', {'form': form, 'res': res})


@login_required
def updateStudent(request, id):
    student = get_object_or_404(User, pk=id)
    form = MyUserChangeForm(instance=student)
    if request.method == 'POST':
        form = MyUserChangeForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student-list')
    return render(request, 'student/form.html', {'form': form})


@login_required
def deleteStudent(request, id):
    student = get_object_or_404(User, pk=id)
    student.delete()
    return redirect('student-list')

# ===================================Subject======================

# def listSubject(request):
#     subjects = Subject.objects.get_queryset().order_by('id')
#     keyword = request.GET .get('keyword', '')
#     if keyword:
#         subjects = subjects.filter(Q(code__contains=keyword)
#                                    | Q(name__contains=keyword))
#     return render(request, 'subject/list.html', {'subjects': subjects, 'keyword': keyword})
# def SearchSubject(keyword):
#     return f'?keyword={keyword}'

# ====================GenericView Subject==================================

# class SubjectListView(generic.ListView):
#     model = Subject
#     context_object_name = 'subjects'
#     template_name = 'subject/index.html'
#     paginate_by = 2
#     # def get_queryset(self):
#     #     keyword = self.request.GET.get('keyword')
#     #     if keyword:
#     #         subjects = self.model.objects.filter(name__icontains=keyword)
#     #     else:
#     #         subjects = self.model.objects.none()
#     #     return subjects

#     def get_context_data(self, **kwargs):
#         context = super(SubjectListView, self).get_context_data(**kwargs)
#         keyword = self.request.GET.get('keyword', '')
#         if keyword:
#             subjects = self.model.objects.filter(Q(code__contains=keyword)
#                                                 | Q(name__contains=keyword))
#         else:
#             subjects = self.model.objects.none()
#         subjects = Subject.objects.all()
#         paginator = Paginator(subjects, self.paginate_by)
#         page = self.request.GET.get('page')
#         try:
#             subjects = paginator.page(page)
#         except PageNotAnInteger:
#             subjects = paginator.page(1)
#         except EmptyPage:
#             subjects = paginator.page(paginator.num_pages)
#         context['subjects'] = subjects
#         return context

# class SubjectCreateView(generic.CreateView):
#     template_name = 'subject/form.html'
#     form_class = SubjectForm
#     queryset = Subject.objects.all()
#     success_url = '/app/subject/'

# class SubjectUpdateView(generic.UpdateView):
#     template_name = 'subject/form.html'
#     form_class = SubjectForm
#     queryset = Subject.objects.all()
#     success_url = '/app/subject/'

# class SubjectDeleteView(generic.DeleteView):
#     template_name = 'subject/form.html'
#     form_class = SubjectForm
#     queryset = Subject.objects.all()
#     success_url = '/app/subject/'
# =================================End GenericView===========================

    # def form_valid(self, form):
    #     print(form.cleaned_data)
    #     return super().form_valid(form)
    # def form_valid(self, form):
    #     messages.success(self.request, 'form is valid')
    #     form.instance.user = self.request.user
    #     form.save()

    # def get_success_url(self):
    #     messages.success(self.request, 'Business Added Successfully')
    #     return reverse('business:list')


def SearchSubject(keyword):
    return f'?keyword={keyword}'


@login_required
def listSubject(request):
    if request.GET.get('keyword'):
        keyword = request.GET.get('keyword')
        subjects = Subject.objects.filter(Q(code__contains=keyword)
                                          | Q(name__contains=keyword))
    else:
        keyword = ''
        subjects = Subject.objects.all()
    paginator = Paginator(subjects, 2)  # Show number contacts per page.
    page_number = request.GET.get('page')
    subjects = paginator.get_page(page_number)
    try:
        subjects = paginator.page(page_number)
    except PageNotAnInteger:
        subjects = paginator.page(1)
    except EmptyPage:
        subjects = paginator.page(paginator.num_pages)
    searchsubject = SearchSubject(keyword)
    filters = {
        'keyword': request.GET.get('keyword', ''),
    }
    return render(request, 'subject/list.html', {'subjects': subjects, 'searchsubject': searchsubject, 'filters': filters})


@login_required
def createSubject(request):
    form = SubjectForm()
    if request.method == 'POST':
        form = SubjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('subject-list')
    return render(request, 'subject/form.html', {'form': form})


@login_required
def updateSubject(request, id):
    subject = get_object_or_404(Subject, pk=id)
    form = SubjectForm(instance=subject)
    if request.method == 'POST':
        form = SubjectForm(request.POST, request.FILES, instance=subject)
        if form.is_valid():
            form.save()
            return redirect('subject-list')
    return render(request, 'subject/form.html', {'form': form})


@login_required
def deleteSubject(request, id):
    subject = get_object_or_404(Subject, pk=id)
    subject.delete()
    return redirect('subject-list')

# ==============================Classes=========================

# def searchClass(keyword):
#     return f'?keyword={keyword}'


def searchClass(keyword, subject_id):
    subject_id = subject_id or ''
    return f'?keyword={keyword}&subject_id={subject_id}'


@login_required
def listClass(request):
    keyword = request.GET.get('keyword', '')
    subject_id = request.GET.get('subject_id', '')
    if keyword or subject_id:
        classes = Classes.objects.filter(Q(code__contains=keyword) | Q(
            name__contains=keyword))
        if subject_id:
            classes = classes.filter(
                subject=Subject.objects.get(id=subject_id))
    else:
        classes = Classes.objects.all()
    # Show number contacts per page.
    paginator = Paginator(classes, 2)
    page_number = request.GET.get('page')
    classes = paginator.get_page(page_number)
    try:
        classes = paginator.page(page_number)
    except PageNotAnInteger:
        classes = paginator.page(1)
    except EmptyPage:

        classes = paginator.page(paginator.num_pages)
    searchclass = searchClass(keyword, subject_id)
    filters = {
        'keyword': keyword,
        'classes': classes,
        'subject_id': subject_id,
    }
    #
    return render(request, 'classes/list.html', {'classes': classes, 'subjects': Subject.objects.all(), 'searchclass': searchclass, 'filters': filters})


@login_required
def createClass(request):
    form = ClassesForm()
    if request.method == 'POST':
        form = ClassesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('class-list')
    return render(request, 'classes/form.html', {'form': form})


@login_required
def updateClass(request, id):
    classes = get_object_or_404(Classes, pk=id)
    form = ClassesForm(instance=classes)
    if request.method == 'POST':
        form = ClassesForm(request.POST, instance=classes)
        if form.is_valid():
            form.save()
            return redirect('class-list')

    return render(request, 'classes/form.html', {'form': form})


@login_required
def deleteClass(request, id):
    classses = get_object_or_404(Classes, pk=id)
    classses.delete()
    return redirect('class-list')
# # =============================Exam=========================


def searchExam(keyword):
    return f'?keyword={keyword}'


@login_required
def listExam(request):
    if request.GET.get('keyword') or request.GET.get('from_date'):
        keyword = request.GET.get('keyword')
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')
        exams = Exam.objects.filter(Q(code__contains=keyword)
                                    | Q(name__contains=keyword) | Q(subject__name__contains=keyword))
        if from_date or to_date:
            exams = exams.filter(start_date__range=(from_date, to_date))
    else:
        keyword = ''
        from_date = ''
        exams = Exam.objects.all()
    paginator = Paginator(exams, 2)  # Show number contacts per page.

    page_number = request.GET.get('page')
    exams = paginator.get_page(page_number)
    try:
        exams = paginator.page(page_number)
    except PageNotAnInteger:
        # Nếu page_number không thuộc kiểu integer, trả về page đầu tiên
        exams = paginator.page(1)
    except EmptyPage:
        # Nếu page không có item nào, trả về page cuối cùng
        exams = paginator.page(paginator.num_pages)

    searchexam = searchExam(keyword)

    filters = {
        'keyword': request.GET.get('keyword', ''),
        'date': request.GET.get('date'),
    }
    return render(request, 'exam/list.html', {'exams': exams, 'searchexam': searchexam,  'filters': filters})


@login_required
def createExam(request):
    form = ExamForm()
    if request.method == 'POST':
        form = ExamForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('exam-list')
    return render(request, 'exam/form.html', {'form': form})


@login_required
def updateExam(request, id):
    exams = get_object_or_404(Exam, pk=id)
    form = ExamForm(instance=exams)
    if request.method == 'POST':
        form = ExamForm(request.POST, instance=exams)
        if form.is_valid():
            form.save()
            return redirect('exam-list')
    return render(request, 'exam/form.html', {'form': form})

@login_required
def deleteExam(request, id):
    exams = get_object_or_404(Exam, pk=id)
    exams.delete()
    return redirect('exam-list')
# ==============================Result=====================

# def listResult(request):
#     results = Result.objects.all()
#     return render(request, 'result/list.html', {'results': results})

@login_required
def listResult(request):
    if request.GET.get('keyword', ''):
        keyword = request.GET.get('keyword')
        results = Result.objects.filter(Q(code__contains=keyword)
                                        | Q(name__contains=keyword))
    else:
        results = Result.objects.all()
    paginator = Paginator(results, 2)
    page_number = request.GET.get('page')
    results = paginator.get_page(page_number)
    try:
        results = paginator.page(page_number)
    except PageNotAnInteger:

        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)
    filters = {
        'keyword': request.GET.get('keyword', ''),
    }
    return render(request, 'result/list.html', {'results': results, 'filters': filters})

@login_required
def createResult(request):
    form = ResultForm()
    if request.method == 'POST':
        form = ResultForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('result-list')
    return render(request, 'result/form.html', {'form': form})

@login_required
def updateResult(request, id):
    results = get_object_or_404(Result, pk=id)
    form = ResultForm(instance=results)
    if request.method == 'POST':
        form = ResultForm(request.POST, instance=results)
        if form.is_valid():
            form.save()
            return redirect('result-list')
    return render(request, 'result/form.html', {'form': form})

@login_required
def deleteResult(request, id):
    results = get_object_or_404(Result, pk=id)
    results.delete()
    return redirect('result-list')

# ===============================ExamManagement=======================

def searchDocument(keyword, subject_id):
    subject_id = subject_id or ''
    return f'?keyword={keyword}&subject_id={subject_id}'


# @login_required
# def listDocument(request):

#     if request.GET.get('keyword', ''):
#         keyword = request.GET.get('keyword')
#         documents = ExamManagement.objects.filter(Q(code__contains=keyword)
#                                         | Q(subject__name__contains=keyword))
#     else:
#         documents = ExamManagement.objects.all()
#     filters = {
#         'keyword': request.GET.get('keyword', ''),
#     }
    
#     return render(request, 'document/list.html', {'documents':  documents, 'filters': filters})


@login_required
def listDocument(request):
    keyword = request.GET.get('keyword', '')
    subject_id = request.GET.get('subject_id', '')
    document = ExamManagement.objects.all()
    if keyword or subject_id:
        documents = ExamManagement.objects.filter(Q(code__contains=keyword))
        if subject_id:
            documents = documents.filter(
                subject=Subject.objects.get(id=subject_id))
    else:
        documents = ExamManagement.objects.all()
    # Show number contacts per page.
    paginator = Paginator(documents, 5)
    page_number = request.GET.get('page')
    documents = paginator.get_page(page_number)
    try:
        documents = paginator.page(page_number)
    except PageNotAnInteger:

        documents = paginator.page(1)
    except EmptyPage:
        documents = paginator.page(paginator.num_pages)

    searchdocument = searchDocument(keyword, subject_id)
    filters = {
        'keyword': keyword,
        'documents': documents,
        'subject_id': subject_id,
    }
    #
    return render(request, 'document/list.html', {'documents': documents, 'subjects': Subject.objects.all(), 'searchdocument': searchdocument, 'filters': filters })

@login_required
def createDocument(request):
    form = ExamManagementForm()
    if request.method == 'POST':
        form = ExamManagementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('document-list')
    return render(request, 'document/form.html', {'form': form})

@csrf_exempt
@require_http_methods(["POST"])
def set_document_status(request, pk):
    document = ExamManagement.objects.get(pk=pk)
    document.status = request.GET.get('status')
    document.save()

    return HttpResponse(
        json.dumps({'success': True}), 
        content_type='application/json'
    )
  
# @login_required
# def uploadFile(request,id):
#     document = get_object_or_404(ExamManagement, pk=id)
#     form = DocumentForm()
#     if request.method == 'POST':
#         form = DocumentForm(request.POST,request.FILES)
#         FileModel.objects.create(
#             document=get_object_or_404(ExamManagement, pk=id),
#             doc = request.FILES['doc']
#         )
#         document.save()
#         return redirect('document-list', id)
#     return render(request, 'document/uploadFile.html', {'form': form, 'document': document})

@login_required
def uploadFile(request,id):
    document = get_object_or_404(ExamManagement, pk=id)
    form = DocumentForm()
    if request.method == 'POST'and 'doc' in request.FILES:
        form = DocumentForm(request.POST,request.FILES)
        if form.is_valid():
            FileModel.objects.create(
                document=document,
                doc = request.FILES['doc']
            )
            document.save()
        return redirect('result-document', id)
    return render(request, 'document/uploadFile.html', {'form': form, 'document': document,})  


@login_required
def resultDocument(request, id):
    document = get_object_or_404(ExamManagement, pk=id)
    return render(request, 'document/resultDocument.html', {'document': document})

@login_required
def viewDocument(request):
    return render(request, 'document/viewDocument.html')