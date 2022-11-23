from django.db import models

# Create your models here.
class Institution(models.Model):
    code=models.CharField(max_length=6)
    name=models.CharField(max_length=50)
    address=models.CharField(max_length=150)
    contact=models.CharField(max_length=10)
    email=models.EmailField()
    website=models.URLField()
    cse=models.IntegerField()
    it=models.IntegerField()
    ece=models.IntegerField()
    eee=models.IntegerField()
    civ=models.IntegerField()
    mec=models.IntegerField()
    fee=models.IntegerField()
    def __str__(self):
        return self.code
b=(('CSE','CSE'),('IT','IT'),('ECE','ECE'),('EEE','EEE'),('CIV','CIV'),('MEC','MEC'))
class Students(models.Model):
    username=models.CharField(max_length=40)
    hall_ticket=models.CharField(max_length=10)
    name=models.CharField(max_length=30)
    rank=models.CharField(max_length=8)
    phone=models.CharField(max_length=10)
    def __str__(self):
        return self.name

class Apply(models.Model):
    student=models.ForeignKey(Students,on_delete=models.CASCADE)
    college=models.ForeignKey(Institution,on_delete=models.CASCADE)
    branch=models.CharField(choices=b,max_length=10,null=True)
    def __str__(self):
        return self.student.username
class Allotment(models.Model):
    name=models.CharField(max_length=40)
    hall_ticket=models.CharField(max_length=10)
    rank=models.CharField(max_length=10)
    code=models.CharField(max_length=6)
    college=models.CharField(max_length=50)
    branch=models.CharField(max_length=5)
    fee=models.CharField(max_length=10)
    def __str__(self):
        return self.name