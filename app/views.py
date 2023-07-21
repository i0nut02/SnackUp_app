from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User

from .utils import check_valid_password
from .models import Classroom, Student, School

# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return render(request, "app/index.html")
    return render(request, "app/student/user_welcome.html", {
        "user_name": Student.objects.filter(email= request.user.email).first()
    })

def login_views(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "app/login.html", {
                "message":"Invalid credentials."
            })
    else:
        return render(request, "app/login.html")


def signup_views(request):
    if request.method == "POST":
        email = request.POST["email"].lower()
        password= request.POST["password"]
        password_reapet = request.POST["password-repeat"]
        phone_number = request.POST["phone-number"]
        classroom_id = request.POST["classroom"]
        username = request.POST["username"]
        # add prefix, phone number and check for phone number
        psw_message = check_valid_password(password)

        if psw_message != None:
            return render(request, "app/signup.html", {
                    "classrooms":Classroom.objects.all(), "message":psw_message
                })
        
        elif password == password_reapet:
            if Student.objects.filter(email= email).exists() or User.objects.filter(username=email).exists() or User.objects.filter(email=email).exists(): # add for companies
                return render(request, "app/signup.html", {
                    "classrooms":Classroom.objects.all(), "message":"Already exist a user with this email"
                })
            if Student.objects.filter(phone_number= phone_number).exists(): # add for companies
                return render(request, "app/signup.html", {
                    "classrooms":Classroom.objects.all(), "message":"Already exists a user with this phone number"
                })
            
            # check for particular edge cases (idk which ones)
            try :
                user = User.objects.create_user(email=email, password=password, username=email)
            except Exception as e:
                return render(request, "app/signup.html", {
                    "classrooms":Classroom.objects.all(), "message":f"An Exception accoured: {str(e)}"
                })
            
            if user is not None:
                # replace with a try and except
                if classroom_id == "None":
                    Student.objects.create(email= email, phone_number= phone_number, username= username)
                else:
                    classroom = Classroom.objects.get(pk=classroom_id)
                    Student.objects.create(email= email, phone_number= phone_number, classroom=classroom, username= username)

                user = authenticate(request, username=email, password=password)
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "app/signup.html", {
                    "classrooms":Classroom.objects.all(), "message":"Please retry, if it happens more time, means there exist a user  with your email so you have to log in"
                })
        else:
            return render(request, "app/signup.html", {
                    "classrooms":Classroom.objects.all(), "message":"The two passwords aren't the same"
                })
    else:
        return render(request, "app/signup.html", {
            "classrooms": Classroom.objects.all()
        })

def logout_views(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def order(request):
    return render(request, "app/student/order.html")

def menu(request):
    student = Student.objects.filter(email= request.user.email).first()
    if student == None:
        return HttpResponseRedirect(reverse("logout"))

    classroom = student.classroom
    if classroom == None:
        return render(request, "app/user_account.html", {
            "message": "Insert the school and class on your account"
        })
    
    # every class must have a school
    company = classroom.school.company
    foods = company.foods.all()

    if request.method == "POST":
        order_student = {}
        for k,v in request.POST.items():
            if isinstance(k, int):
                if foods.filter(pk=k).exists():
                    order_student[k] = v
        return HttpResponseRedirect("order", request)

    if company == None:
        return render(request, "app/student/menu.html", {
            "message": "There isn't any company wich offer this service to your school"
        })

    return render(request, "app/student/menu.html", {
        "foods": foods
    })

