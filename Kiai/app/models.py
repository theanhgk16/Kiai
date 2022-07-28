from telnetlib import STATUS
from tkinter.messagebox import QUESTION, YES
from xml.dom.minidom import Document
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from django.db import models
from grpc import Status
# Create your models here.


class User(AbstractUser):
    # fullname = models.CharField(max_length=50)
    # phone = models.CharField(max_length=20)
    MALE = 'Nam'
    FEMALE = 'Nữ'
    OTHER = 'Giới tính khác'

    SEX = [
        (MALE, 'Nam'),
        (FEMALE, 'Nữ'),
        (OTHER, 'Giới tính khác'),
    ]

    # id = models.AutoField(primary_key=True)
    code = models.CharField(
        max_length=50, verbose_name='Mã', unique=True)
    name = models.CharField(max_length=100, verbose_name='Tên')
    birthday = models.DateField(
        null=True, verbose_name='Ngày sinh')
    sex = models.CharField(max_length=20, choices=SEX,
                           blank=True, verbose_name='Giới tính')
    phone = models.CharField(max_length=20, verbose_name='Số điện thoại')
    address = models.CharField(max_length=250, verbose_name='Địa chỉ')
    cmnd = models.CharField(max_length=30, verbose_name='CMND')

    def __str__(self):
        return self.code


# class Student(models.Model):
#     MALE = 'Nam'
#     FEMALE = 'Nữ'
#     OTHER = 'Giới tính khác'

#     SEX = [
#         (MALE, 'Nam'),
#         (FEMALE, 'Nữ'),
#         (OTHER, 'Giới tính khác'),
#     ]

#     # id = models.AutoField(primary_key=True)
#     code = models.CharField(max_length=50, verbose_name='Mã', unique=True)
#     name = models.CharField(max_length=100, verbose_name='Tên')
#     birthday = models.DateField(
#         null=True, verbose_name='Ngày sinh')
#     sex = models.CharField(max_length=20, choices=SEX,
#                            blank=True, verbose_name='Giới tính')
#     phone = models.CharField(max_length=20, verbose_name='Số điện thoại')
#     address = models.CharField(max_length=250, verbose_name='Địa chỉ')
#     cmnd = models.CharField(max_length=30, verbose_name='CMND')

#     def __str__(self):
#         return self.code


class Subject(models.Model):
    # id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=50, verbose_name='Mã môn học', unique=True, error_messages={
        "unique": "Môn học có mã đã tồn tại"
    })
    name = models.CharField(max_length=100, verbose_name='Tên môn học')
    description = models.CharField(
        max_length=500, verbose_name='Mô tả', blank=True)
    image = models.ImageField(
        verbose_name='Ảnh môn học', upload_to='static/images')
    
    def __str__(self):
        return self.name


class Classes(models.Model):
    # id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=50, verbose_name='Mã', unique=True, error_messages={
        "unique": "Lớp học có mã đã tồn tại"})
    name = models.CharField(max_length=100, verbose_name='Tên')  # mã lớp
    subject = models.ForeignKey(
        Subject, verbose_name="Môn học",  on_delete=models.PROTECT)

    def __str__(self):
        return self.code


class Exam(models.Model):
    # id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=100, verbose_name='Mã', unique=True, error_messages={
        "unique": "Kì thi có mã đã tồn tại"})
    name = models.CharField(max_length=100, verbose_name='Tên')
    start_date = models.DateField(
        null=True, verbose_name='Ngày bắt đầu')
    subject = models.ForeignKey(
        Subject, verbose_name="Môn học",  on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Result(models.Model):
    # id = models.AutoField(primary_key=True)
    exam = models.ForeignKey(
        Exam, verbose_name="Kì Thi",  on_delete=models.PROTECT)
    student = models.ForeignKey(
        User, verbose_name="Học sinh",  on_delete=models.PROTECT)
    point = models.FloatField(verbose_name='Điểm')

    # def __str__(self):
    #     return self.exam_id


# class Enrollment(models.Model):
#     code = models.CharField(
#         max_length=200, verbose_name="Học sinh", unique=True)

#     note = models.CharField(max_length=200, verbose_name="Ghi chú")
class Enrollment(models.Model):
    user = models.ForeignKey(
        User, verbose_name="Học sinh",  on_delete=models.PROTECT, default='')
    subject = models.ForeignKey(
        Subject, verbose_name="Môn học",  on_delete=models.PROTECT, default='')
    note = models.CharField(
        max_length=200, verbose_name="Ghi chú ", default='')

class ExamManagement(models.Model):
    YES = 'Có'
    NO = 'Không'

    STATUS = [
        (YES, 'Có'),
        (NO, 'Không'),
    ]
    subject = models.ForeignKey(
        Subject, verbose_name="Môn học",  on_delete=models.PROTECT)
    code = models.CharField(max_length=100, verbose_name='Mã đề thi')
    num_question = models.IntegerField(verbose_name='Số lượng câu hỏi')
    status = models.CharField(max_length=20, choices=STATUS,
                           blank=True, verbose_name='Trạng thái xuất bản')
    
    def __str__(self):
        return self.code

class FileModel(models.Model):
    document = models.ForeignKey(
        ExamManagement, verbose_name="Upload",  on_delete=models.PROTECT,default='')
    doc = models.FileField(upload_to='static/', default=None)