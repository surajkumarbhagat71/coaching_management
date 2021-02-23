from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


#///////////////////////////////////////////////////////////////////////////////////////////////////////////////#


class Student(models.Model):
    st_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    father_name = models.CharField(max_length=200)
    contact = models.IntegerField()
    email = models.EmailField()
    dp = models.ImageField(upload_to='media',blank=True)
    city = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    date_time = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)


    def __str__(self):
        return self.name


class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='media/')
    discription = models.TextField()
    fee = models.IntegerField()

    def __str__(self):
        return self.name


class StudentCourse(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course,on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    date_time = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)


    def __str__(self):
        return self.student_id.name


class StudentPayment(models.Model):
    pay_id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student,on_delete=models.CASCADE)
    course_id = models.ForeignKey(StudentCourse,models.CASCADE)
    pay_date = models.DateTimeField()
    pay_amount = models.IntegerField()
    pay_due = models.IntegerField()
    status = models.CharField(choices=(("0","Not paid"),("1","pending"),("2","paid")),max_length=200)

    def __str__(self):
        return self.student_id.name
