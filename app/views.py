from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.db import transaction

from .utils import check_valid_password
from .models import Classroom, Student, Order, Food_Order, Cart

import datetime

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

def cart(request):
    student = Student.objects.filter(email= request.user.email).first()
    if student == None:
        return HttpResponseRedirect(reverse("logout"))

    classroom = student.classroom
    if classroom == None:
        return render(request, "app/user_account.html", {
            "message": "Insert the school and class on your account"
        })
    
    company = classroom.school.company
    
    if request.method == "POST":
        # every class must have a school

        foods = company.foods.all()
        payment_methods = company.payment_methods.all()

        payment_type = None
        food_ordered = {}
        total_price = 0

        for k,v in request.POST.items():
            if k.isnumeric():
                if foods.filter(pk=int(k)).exists() and v.isnumeric() and int(v) > 0:
                    food = foods.get(pk=int(k))
                    food_ordered[food] = int(v)
                    total_price += int(v) * food.price

            elif payment_methods.filter(pk=v).exists():
                payment_type = v

        if len(food_ordered) == 0:
            return HttpResponseRedirect(reverse("menu"))
        
        if payment_type == None:
            return render(request, "app/student/cart.html", {
            "order" : food_ordered.items(), "methods" : company.payment_methods.all(),
            "message" : "An error accour with the payment method"
        })

        order_s = Order.objects.create(student=student, company=company, total_price=total_price, instant_purchase=datetime.datetime.now())

        for food, quantity in food_ordered.items():
            Food_Order.objects.create(food=food, order=order_s, quantity=quantity)
        
        item_to_delete = Cart.objects.filter(student= student)
        item_to_delete.delete()
        
        return render(request, "app/student/successful_order.html")

    else:
        food_ordered = {}
        for cart_obj in Cart.objects.filter(student= student):
            food_ordered[cart_obj.food] = cart_obj.quantity
        
        if len(food_ordered) == 0:
            return redirect('menu')
        else:
            return render(request, "app/student/cart.html", {
                "order" : food_ordered.items(), "methods" : company.payment_methods.all()
            })



def orders(request):
    student = Student.objects.filter(email= request.user.email).first()
    if student == None:
        return HttpResponseRedirect(reverse("logout"))
    orders_s = Order.objects.filter(student=student).order_by('-instant_purchase')
    food_order = {}
    for order_m in orders_s:
        food_order[order_m] = []
        for food_ord in Food_Order.objects.filter(order=order_m):
            food_order[order_m].append(food_ord)

    return render(request, "app/student/orders.html", {
        "orders" : food_order.items()
    })


def account(request, message=None):
    student = Student.objects.filter(email= request.user.email).first()
    if student == None:
        return HttpResponseRedirect(reverse("logout"))

    classroom = student.classroom

    html_dict = { "data": {
                    "User Name": student.username, "Email": student.email, 
                    "Phone Number":student.phone_number, "Classroom": classroom
                    }
                }
    if message != None:
        html_dict["message"] = message
    # the keys of the dictionary will appear in the html page
    return render(request, "app/student/account.html", html_dict)


def change_information(request, change_info):
    # change_info if not typed directly it's in lower case but if typed by the user we don't know
    change_info = change_info.lower()

    student = Student.objects.filter(email= request.user.email).first()
    if student == None:
        return HttpResponseRedirect(reverse("logout"))
    
    dict_info = {"information" : change_info.capitalize()}

    if change_info == "classroom":
        dict_info["list"] = Classroom.objects.all()
        if len(dict_info["list"]) == 0:
            return HttpResponseRedirect(reverse("account"))
        
    elif change_info in {"user name", "email", "phone number"}:
        if change_info == "user name":
            dict_info["last_information"] = student.username
        elif change_info == "email":
            dict_info["last_information"] = student.email
        elif change_info == "phone number":
            dict_info["last_information"] = student.phone_number
    elif change_info == "password":
        pass
    else:
        # no one operation identified
        return HttpResponseRedirect(reverse("account"))
    
    if request.method == "POST":
        if change_info == "classroom":
            if request.POST["classroom"] == None:
                student.classroom = None
            else:
                student.classroom = Classroom.objects.get(pk=int(request.POST["classroom"]))
            student.save()

        elif change_info == "user name":
            student.username = request.POST["user name"]
            student.save()

        elif change_info == "email":
            try :
                with transaction.atomic():
                    email = request.POST["email"]
                    if Student.objects.filter(email= email).exists() or User.objects.filter(username=email).exists() or User.objects.filter(email=email).exists(): # add for companies
                        dict_info["message"] = "Already exist a user with this email"
                    else:
                        user = User.objects.get(username = student.email)
                        user.email = email
                        user.username = email
                        user.save()
                        
                        old_email = student.email
                        old_phone_number = student.phone_number

                        student.email = email
                        student.phone_number = None
                        student.save()

                        Student.objects.get(pk=old_email).delete()
                        student.phone_number = old_phone_number
                        student.save()
            except Exception as e:
                dict_info["message"] = str(e)
                

        elif change_info == "phone number":
            try :
                with transaction.atomic():
                    phone_number = request.POST["phone number"]
                    if Student.objects.filter(phone_number= phone_number).exists(): # add for companies
                        dict_info["message"] = "Already exist a user with this phone number"
                    else:
                        student.phone_number = phone_number
                        student.save()
            except Exception as e:
                dict_info["message"] = str(e)

        elif change_info == "password":
            password1 = request.POST["password1"]
            password2 = request.POST["password2"]
            if password1 == password2:
                message = check_valid_password(password1)
                if message == None:
                    user = User.objects.get(username = student.email)
                    user.password = password1
                else:
                    dict_info["message"] = message
            else:
                dict_info["message"] = "The two password are different"
        else:
            # no one operation identified
            return HttpResponseRedirect(reverse("account"))

    if (not ("message" in dict_info)) and (request.method == "POST"):
        return HttpResponseRedirect(reverse("index"))
    return render(request,  "app/student/change_information.html", 
            dict_info)
    

def menu(request):
    student = Student.objects.filter(email= request.user.email).first()
    if student == None:
        return HttpResponseRedirect(reverse("logout"))

    classroom = student.classroom
    if classroom == None:
        return account(request, "Insert your classroom if it exist, otherwise you can't order")
    
    # every class must have a school
    company = classroom.school.company
    foods = company.foods.all()

    if request.method == "POST":
        order_student = {}
        for k,v in request.POST.items():
            if k.isnumeric():
                if foods.filter(pk=int(k)).exists() and v.isnumeric() and int(v) > 0:
                    food = foods.get(pk=int(k))
                    order_student[food] = v
                    cart_obj = Cart.objects.filter(student= student, food= food)
                    
                    if cart_obj.exists():
                        quantity = int(v)
            
                        for cart in cart_obj:
                            quantity += cart.quantity
                        
                        quantity = min(10, quantity)
                        cart_obj.delete()
                        Cart.objects.create(student= student, food= food, quantity= quantity)
                        order_student[food] = quantity
                    else:
                        Cart.objects.create(student= student, food = foods.get(pk=int(k)), quantity= int(v))
        
        return render(request, "app/student/cart.html", {
            "order" : order_student.items(), "methods" : company.payment_methods.all()
        })

    if company == None:
        return render(request, "app/student/menu.html", {
            "message": "There isn't any company wich offer this service to your school"
        })

    return render(request, "app/student/menu.html", {
        "foods": foods
    })