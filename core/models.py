from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class Student(AbstractUser):
    # identifier = models.IntegerField(primary_key=True)
    labGroup = models.ForeignKey('LabGroup', on_delete=models.CASCADE, null=True)
    theoryGroup = models.ForeignKey('TheoryGroup', on_delete=models.CASCADE, null=True)
    first_name = models.CharField(blank=False, max_length=128)
    last_name = models.CharField(blank=False, max_length=128)
    gradeTheoryLastYear = models.IntegerField(default=0)
    gradeLabLastYear = models.IntegerField(default=0)
    convalidationGranted = models.BooleanField(default=False)
    # password = models.CharField(blank=False, max_length=128)
    # username = models.CharField(blank=False, max_length=128)

    # REQUIRED_FIELDS = ['username', 'password', 'first_name', 'last_name']
    USERNAME_FIELD = 'username'
    # EMAIL_FIELD = 'username'

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return self.first_name + " " + self.last_name + " " + self.theoryGroup.__str__() + " " + self.labGroup.__str__()


class LabGroup(models.Model):
    #identifier = models.IntegerField(primary_key=True)
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    groupName = models.CharField(blank=False, max_length=128)
    language = models.CharField(blank=False, max_length=128)
    schedule = models.CharField(blank=False, max_length=128)
    maxNumberStudents = models.IntegerField(default=0)
    counter = models.IntegerField(default=0)

    class Meta:
        ordering = ['groupName']

    def __str__(self):
        return self.groupName + " " + self.teacher.__str__() + " " + self.language + " " + str(self.counter) + "/" + str(self.maxNumberStudents) 


class Teacher(models.Model):
    #identifier = models.IntegerField(primary_key=True)
    first_name = models.CharField(blank=False, max_length=128)
    last_name = models.CharField(max_length=128)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return self.first_name + " " + self.last_name


class Pair(models.Model):
    #identifier = models.IntegerField(primary_key=True)
    student1 = models.ForeignKey('Student', related_name='par1', on_delete=models.CASCADE)
    student2 = models.ForeignKey('Student', related_name='par2',on_delete=models.CASCADE)
    validated = models.BooleanField(default=False)
    studentBreakRequest = models.ForeignKey('Student', related_name='breakPair', on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['student1', 'student2']

    def __str__(self):
        return self.student1.__str__() + " " + self.student2.__str__() + " " + str(self.validated)


class GroupConstraints(models.Model):
    #identifier = models.IntegerField(primary_key=True)
    labGroup = models.ForeignKey('LabGroup', on_delete=models.CASCADE)
    theoryGroup = models.ForeignKey('TheoryGroup', on_delete=models.CASCADE)

    class Meta:
        ordering = ['labGroup', 'theoryGroup']

    def __str__(self):
        return self.theoryGroup.__str__() + " " + self.labGroup.__str__()


class TheoryGroup(models.Model):
    #identifier = models.IntegerField(primary_key=True)
    groupName = models.CharField(blank=False, max_length=128)
    language = models.CharField(blank=False, max_length=128)

    class Meta:
        ordering = ['groupName']

    def __str__(self):
        return self.groupName + " " + self.language


class OtherConstraints(models.Model):
    #identifier = models.IntegerField(primary_key=True)
    selectGroupStartDate = models.DateTimeField()
    minGradeTheoryConv = models.FloatField(default=0)
    minGradeLabConv = models.FloatField(default=0)

    def __str__(self):
        return str(self.selectGroupStartDate) + " " + str(self.minGradeTheoryConv) + " " + str(self.minGradeLabConv)
