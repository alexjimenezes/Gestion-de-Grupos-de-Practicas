# Populate database
# This file has to be placed within the
# core/management/commands directory in your project.
# If that directory doesn't exist, create it.
# The name of the script is the name of the custom command,
# that is, populate.py.
#
# execute python manage.py  populate


from django.core.management.base import BaseCommand
from core.models import (OtherConstraints, Pair, Student,
                         GroupConstraints, TheoryGroup,
                         LabGroup, Teacher)

import csv
import os


# The name of this class is not optional must be Command
# otherwise manage.py will not process it properly
#
# Teachers, groups and constraints
# will be hardcoded in this file.
# Students will be read from a cvs file
# last year grade will be obtained from another cvs file
class Command(BaseCommand):
    # helps and arguments shown when command python manage.py help populate
    # is executed.
    help = """populate database
           """

    def add_arguments(self, parser):
        parser.add_argument('model', type=str, help="""
        model to  update:
        all -> all models
        teacher
        labgroup
        theorygroup
        groupconstraints
        otherconstrains
        student (require csv file)
        studentgrade (require different csv file,
        update only existing students)
        pair
        """)
        parser.add_argument('studentinfo', type=str, help="""CSV file with student information
        header= NIE, DNI, Apellidos, Nombre, Teoría
        if NIE or DNI == 0 skip this entry and print a warning""")
        parser.add_argument('studentinfolastyear', type=str, help="""CSV file with student information
        header= NIE,DNI,Apellidos,Nombre,Teoría, grade lab, grade the
        if NIE or DNI == 0 skip this entry and print a warning""")
        parser.add_argument('auxiliary_info', type=str, help="""txt file with auxiliary information""")

    # handle is another compulsory name, do not change it"
    def handle(self, *args, **kwargs):
        path = os.getcwd()

        print(path)
        model = kwargs['model']
        cvsStudentFile = kwargs['studentinfo']
        cvsStudentFileGrades = kwargs['studentinfolastyear']
        txtAux = kwargs['auxiliary_info']

        # with open('/tmp/dict.txt', 'r') as dict_file:
        #    dict_text = dict_file.read()
        #   dict_from_file = eval(dict_text)
        f_aux = open("./core/management/commands/" + txtAux, "r")
        txt_f_aux = f_aux.read()
        teacher_data, labgroup_data, theorygroup_data, x, y = txt_f_aux.split("====")


        # clean database
        if model == 'all':
            self.cleanDataBase()
        if model == 'teacher' or model == 'all':
            self.teacher(teacher_data)
        if model == 'labgroup' or model == 'all':
            self.labgroup(labgroup_data)
        if model == 'theorygroup' or model == 'all':
            self.theorygroup(theorygroup_data)
        if model == 'groupconstraints' or model == 'all':
            self.groupconstraints()
        if model == 'otherconstrains' or model == 'all':
            self.otherconstrains()
        if model == 'student' or model == 'all':
            self.student(cvsStudentFile)
        if model == 'studentgrade' or model == 'all':
            self.studentgrade(cvsStudentFileGrades)
        if model == 'pair' or model == 'all':
            self.pair()

    def cleanDataBase(self):
        # delete all models stored (clean table)
        # in database
        # remove pass and ADD CODE HERE
        """ Tag.objects.all().delete()
        Post.objects.all().delete() """
        pass

    def teacher(self, data):
        "create teachers here"
        # remove pass and ADD CODE HERE
        teacherD = {}
        exec(data.replace(" ", ""))

        for t_id, t_data in teacherD.items():
            t = Teacher.objects.get_or_create(first_name=t_data['first_name'], family_name=t_data['last_name'])[0]
            t.save()

    def labgroup(self, data):
        "add labgroups"
        # remove pass and ADD CODE HERE
        labgroupD = {}
        exec(data.replace(" ", ""))

    def theorygroup(self, data):
        "add theorygroups"
        # remove pass and ADD CODE HERE
        theorygroupD = {}
        exec(data.replace(" ", ""))

    def groupconstraints(self):
        "add group constrints"
        """ Follows which laboratory groups (4th column
            may be choosen by which theory groups (2nd column)
theoryGroup: 126, labGroup: 1261
theoryGroup: 126, labGroup: 1262
theoryGroup: 126, labGroup: 1263
theoryGroup: 127, labGroup: 1271
theoryGroup: 127, labGroup: 1272
theoryGroup: 120, labGroup: 1201
theoryGroup: 129, labGroup: 1291
theoryGroup: 125, labGroup: 1292"""
        # remove pass and ADD CODE HERE
        pass

    def pair(self):
        "create a few valid pairs"
        # remove pass and ADD CODE HERE
        pass

    def otherconstrains(self):
        """create a single object here with staarting dates
        and maximum and minimum convalidation grades"""
        """ Use the following values:
        selectGroupStartDate = now + 1 day,
        minGradeTheoryConv = 3,
        minGradeLabConv = 7
        """
        # remove pass and ADD CODE HERE
        pass

    def student(self, csvStudentFile):
        # read csv file
        # structure NIE	DNI	Apellidos	Nombre	group-Teoría
        # remove pass and ADD CODE HERE
        pass

    def studentgrade(self, cvsStudentFileGrades):
        # read csv file
        # structure NIE	DNI	Apellidos	Nombre	group-Teoría	grade-practicas	gradeteoria
        # remove pass and ADD CODE HERE
        pass
