from django.shortcuts import render,redirect ,HttpResponse
from django.views.generic import TemplateView , View , DetailView
from django.views.generic.edit import UpdateView
from .models import *
from .forms import *
from django.utils.timezone import timezone
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import  LoginRequiredMixin
from django.contrib.auth.models import User , Group
from datetime import timedelta , datetime
from datedelta import datedelta
from django.db.models import Q


######################## BASIC #############################

class Home(View):
    def get(self,request):
        context = {"course":Course.objects.all()}
        return render(request,'main/home.html',context)


class DetailCourse(DetailView):
    model = Course
    template_name = 'main/detail_course.html'
    context_object_name = 'detailcourse'


class PandingRequest(TemplateView):
    template_name = "main/pandingapply.html"


#////////////////////////////////////// SIGNUP LOGIN LOGOUT \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


class UserSignup(View):
    def get(self,request):
        context = {"form":UserSignupForm}
        return render(request,'main/signup.html',context)

    def post(self, request):
        form = UserSignupForm(request.POST or None)
        if form.is_valid():
            f = form.save()
            group = Group.objects.get(name='student')
            f.groups.add(group)
            return redirect('login')
        else:
            return render(request,'main/signup.html')

#////////////////////////////////////////////////////// LOGIN \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

class Login(View):
    def get(self,request):
        return render(request,'main/login.html')

    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            username = User.objects.get(email=username)
            user = authenticate(username=username.username , password = password)
        except:
            return redirect('login')

        try:
            if user is not None:
                login(request,user)
            else:
                return redirect('login')

            if user.groups.filter(name = "admin").exists():
                return redirect('admindashaboard')

            elif user.groups.filter(name = "student").exists():
                try:
                    Student.objects.get(user=request.user,status=True)
                    return render(request,'student/dashaboard.html')
                except:
                    if Student.objects.filter(user=request.user, status=False).exists():
                        return redirect('pandingrequest')
                    else:
                        return redirect('adduserdetail')
            else:
                return redirect('login')
        except:
            return redirect('login')


#////////////////////////////////////////////////// LOGOUT  \\\\\\\\\\\\\\\\\\\\\\\\\\\

class Logout(View):
    def get(self,request):
        logout(request)
        return redirect('home')
        return render(request,'main/home.html')


#///////////////////////////////////////////////  ADDUSERDETAL \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

class AddUserDetail(LoginRequiredMixin,View):
    def get(self,request):
        context = {"form":UserDetailForm()}
        return render(request,'main/adduserdetail.html',context)

    def post(self,request):
        form = UserDetailForm(request.POST or None , request.FILES or None)
        if form.is_valid():
            a = form.save(commit=False)
            a.user = request.user
            a.save()
            return redirect('login')
        else:
            return redirect('adduserdetail')

#////////////////////////////////// User Add course \\\\\\\\\\\\\\\\\\\\\\\

class UserJoinCourse(LoginRequiredMixin,View):
    def get(self,request,pk):
        # if Student.objects.filter(user = request.user,status=True).exists():
        #     user = Student.objects.get(user=request.user)
        #     course = StudentCourse()
        #     course.student_id = user
        #     course.course_id = Course(pk)
        #     course.save()
        #     return redirect('dashaboard')
        # elif Student.objects.filter(user = request.user,status=False).exists():
        #     return redirect('pandingrequest')
        # else:
        #     return redirect('adduserdetail')
        #

        try:
            Student.objects.filter(user = request.user,status=True)
            user = Student.objects.get(user=request.user)
            course = StudentCourse()
            course.student_id = user
            course.course_id = Course(pk)
            course.save()
            return redirect('dashaboard')
        except:
            if Student.objects.filter(user=request.user,status=False).exists():
                return redirect('pandingrequest')
            else:
                return redirect('adduserdetail')

#/////////////////////////////////////  USER DASHABOARD  \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

class Dashaboard(LoginRequiredMixin,View):
    def get(self,request):
        try:
            Student.objects.get(user = request.user,status=True)
            context = {
                "mycourse":StudentCourse.objects.filter(student_id__user = request.user).count(),

            }
            return render(request,'student/dashaboard.html',context)
        except:
            if Student.objects.filter(user=request.user, status=False).exists():
                return redirect('pandingrequest')
            else:
                return redirect('adduserdetail')


#///////////////////////////////// USER PROFIEL \\\\\\\\\\\\\\\\\\\\\\\\

class Profile(LoginRequiredMixin,View):
    def get(self,request):
        try:
            context = {"profile":Student.objects.get(user = request.user , status=True)}
            return render(request,'student/profile.html',context)
        except:
            if Student.objects.filter(user=request.user , status=False).exists():
                return redirect('pandingrequest')
            else:
                return redirect('adduserdetail')

#////////////////////////////////////////  USER PAYMENT REQUEST \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

class PaymentRequest(LoginRequiredMixin,View):
    def get(self,request,pk):
        try:
            Student.objects.get(user=request.user,status=True)
            data = StudentPayment.objects.get(pay_id = pk)
            data.status = "1"
            data.save()
            return render(request,'student/dashaboard.html')
        except:
            if Student.objects.filter(user=request.user, status=False).exists():
                return redirect('pandingrequest')
            else:
                return redirect('adduserdetail')


#/////////////////////// USER  PAYMENT \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

class StudentPayment(LoginRequiredMixin,View):
    def get(self,request):
        try:
            Student.objects.get(user=request.user,status=True)

        except:
            if Student.objects.filter(user=request.user, status=False).exists():
                return redirect('pandingrequest')
            else:
                return redirect('adduserdetail')
        return render(request,'student/payment.html')



#//////////////////////////////////////////  USER COURSER  /////////////////////////

class UserCourse(LoginRequiredMixin,View):
    def get(self,request):
        try:
            Student.objects.get(user = request.user,status=True)
            context = {"course": StudentCourse.objects.filter(student_id__user = request.user)}
            return render(request,'student/join_course.html',context)
        except:
            if Student.objects.filter(user=request.user, status=False).exists():
                return redirect('pandingrequest')
            else:
                return redirect('adduserdetail')


class StudentProfileUpdate(LoginRequiredMixin,UpdateView):
    model = Student
    form_class = UserDetailForm
    template_name = 'student/student_update_profile.html'

    def form_valid(self, form):
        form.save()
        return redirect('profiel')


#/////////////////////////////////////////////// ADMIN WORK \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\/\\\\\\\\\\\\//////\\\\\\\\\\\\\\\



#/////////////////////////////  ADD COURSE \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

class AddCourse(LoginRequiredMixin,View):
    def get(self,request):
        user = User.objects.get(username=request.user)
        if user.groups.filter(name='admin'):
            form = CourseForm()
            return render(request, 'director/addcourse.html', {"form": form})

        else:
            return render(request, 'main/home.html')


    def post(self,request):
        user = User.objects.get(username=request.user)
        if user.groups.filter(name='admin'):
            form = CourseForm(request.POST or None, request.FILES or None)
            if form.is_valid():
                form.save()
                return redirect('admindashaboard')

        else:
            return render(request, 'main/home.html')


#////////////////////////////////////  ADMIN DASHABOARD \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

class AdminDashaboard(LoginRequiredMixin,View):
    def get(self,request):
        user = User.objects.get(username = request.user)
        if user.groups.filter(name = 'admin'):
            return render(request,'director/dashaboard.html')
        else:
            return render(request,'main/home.html')


#////////////////////////////////// REQUEST FOR ADMISSION BY STUDENT \\\\\\\\\\\\\\\\\\\\\\\\\

class RequestforAddmision(LoginRequiredMixin,View):
    def get(self,request):
        user = User.objects.get(username=request.user)
        if user.groups.filter(name='admin'):
            context = {"requestforaddmision":Student.objects.filter(status=False)}
            return render(request, 'director/requestforaddmision.html',context)
        else:
            return render(request, 'main/home.html')


#////////////////////////////////// REQUEST FOR COURSE BY STUDENT \\\\\\\\\\\\\\\\\\\\\\\\\

class Requestforcourse(LoginRequiredMixin, View):
    def get(self, request):
        user = User.objects.get(username=request.user)
        if user.groups.filter(name='admin'):
            context = {"requestforcourse": StudentCourse.objects.filter(status=False)}
            return render(request,'director/requestforcourse.html',context)
        else:
            return render(request, 'main/home.html')


#////////////////////////////////// ALL STUDENT \\\\\\\\\\\\\\\\\\\\\\\\\

class AllStudent(LoginRequiredMixin,View):
    def get(self,request):
        user = User.objects.get(username=request.user)
        if user.groups.filter(name='admin'):
            context = {"allstudent":Student.objects.filter(status=True)}
            return render(request,'director/allstudent.html',context)
        else:
            return render(request,'main/home.html')


#/////////////////////////////////////// Apsept Payment \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

class ApseptPayment(LoginRequiredMixin,View):
    def get(self,request,pk):
        user = User.objects.get(username=request.user)
        if user.groups.filter(name='admin'):
            data = StudentPayment.objects.get(pay_id=pk)
            data.status = "2"
            data.save()
            return redirect('admindashaboard')
            return render(request, 'director/payment_due.html')
        else:
            return render(request,'main/home.html')


#///////////////////////////////// Apsept Admission \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

class ApseptAdminssion(LoginRequiredMixin, View):
    def get(self,request,pk):
        user = User.objects.get(username=request.user)
        if user.groups.filter(name='admin'):
            data = Student.objects.get(st_id=pk)
            data.status = True
            data.save()
            return redirect('requestforaddmision')
        else:
            return render(request,'main/home.html')


#///////////////////////////////// Apsept Course \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

class ApseptCourse(LoginRequiredMixin, View):
    def get(self,request,pk):
        user = User.objects.get(username=request.user)
        if user.groups.filter(name='admin'):
            data = StudentCourse.objects.get(id =pk)
            data.status = True
            data.save()
            return redirect('requestforcourse')
        else:
            return render(request, 'main/home.html')



#///////////////////////////////////////////////// I am working on \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

# def diff_month(d1,d2):
#     return (d1.year - d2.year) * 12 + d1.month - d2.month
#
# class PaymentGenarate(LoginRequiredMixin,View):
#     def get(self,request):
#       std_course = StudentCourse.objects.filter(student_id__user = request.user , status=True)
        # user_id = Student.objects.get(user=request.user)
        #
        # for x in range(std_course.count()):
        #     doj = std_course[x].date_time
        #     pay = std_course[x].course_id.fee
        #
        #     while diff_month(datetime.now().date(),doj) != 0:
        #
        #         cond = Q(p_month = doj) & Q( course_id = std_course[x].id) & Q(student_id__user = request.user)
        #
        #         if StudentPayment.objects.filter(cond).exists() == False:
        #             p = StudentPayment()
        #             p.course_id = Course(std_course[x].course_id)
        #             p.student_id = Student(user_id.st_id)
        #             p.pay_amount = pay
        #             p.pay_due = pay
        #             p.pay_date = doj
        #             p.status = "0"
        #             p.save()
        #         doj  = doj + datedelta(months = 1)
        #
        # try:
        #     data = {"payment":StudentPayment.objects.filter(student_id__user = request.user)}
        #     return render(request,'student/payment.html',data)
        # except:
        #     return HttpResponse("not avalable your paymet")













