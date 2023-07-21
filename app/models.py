from django.db import models

# Create your models here.   
# think about a relationship beetween Company and User, and one beetween Student and User

class Category(models.Model):
    name = models.CharField(max_length=64, primary_key=True)

    def __str__(self):
        return self.name


class Food(models.Model):
    name = models.CharField(max_length=64)
    price = models.FloatField()
    category = models.ForeignKey(Category, on_delete= models.CASCADE)

    def __str__(self):
        return f"{self.name}, {self.price}"


class Company(models.Model):
    email = models.EmailField(primary_key=True, max_length=128)
    phone_number = models.CharField(max_length=15, unique=True)
    username = models.CharField(max_length=64)
    foods = models.ManyToManyField(Food, blank=True)

    def __str__(self):
        return f"{self.username}, {self.email}"


class School(models.Model):
    name = models.CharField(max_length=64)
    street = models.CharField(max_length=128)
    street_number = models.PositiveIntegerField()
    zip_code = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    country = models.CharField(max_length=64)
    company = models.ForeignKey(Company, null=True, blank=True, on_delete= models.SET_NULL)

    def __str__(self):
        return f"{self.name}, {self.country}, {self.city}, {self.zip_code}, {self.street}, {self.street_number}"
    
    class Meta:
        unique_together = ("street", "street_number", "zip_code")


class Classroom(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    grade = models.PositiveIntegerField()
    section = models.CharField(max_length=1)
    specialisation = models.CharField(max_length=32)

    def __str__(self):
        return f"ID: {self.id}\nSchool: {str(self.school)}\ngrade: {self.grade}, section: {self.section}, specialisation: {self.specialisation}"
    
    class Meta:
        unique_together = ("school", "grade", "section", "specialisation")


class Student(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(primary_key=True, max_length=128)
    username = models.CharField(max_length=64, default= email)
    classroom = models.ForeignKey(Classroom, blank=True, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.username}"


