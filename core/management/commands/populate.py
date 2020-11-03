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
from collections import OrderedDict
import pandas as pd
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
        teacher_data, labgroup_data, theorygroup_data, groupconstraints_data, pairs_data = txt_f_aux.split("====")


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
            self.groupconstraints(groupconstraints_data)
        if model == 'otherconstrains' or model == 'all':
            self.otherconstrains()
        if model == 'student' or model == 'all':
            self.student(cvsStudentFile)
        if model == 'studentgrade' or model == 'all':
            self.studentgrade(cvsStudentFileGrades)
        if model == 'pair' or model == 'all':
            self.pair(pairs_data)

    def cleanDataBase(self):
        # delete all models stored (clean table)
        # in database
        # remove pass and ADD CODE HERE
        Teacher.objects.all().delete()
        LabGroup.objects.all().delete()
        TheoryGroup.objects.all().delete()
        OtherConstraints.objects.all().delete()
        Student.objects.all().delete()
        Pair.objects.all().delete()
        GroupConstraints.objects.all().delete()

    def teacher(self, data):
        "create teachers here"
        # remove pass and ADD CODE HERE
        teacherD = {}
        exec(data.replace(" ", ""))

        for t_id, t_data in teacherD.items():
            t = Teacher.objects.get_or_create(id=t_id, first_name=t_data['first_name'], family_name=t_data['last_name'])[0]
            t.save()

    def labgroup(self, data):
        "add labgroups"
        # remove pass and ADD CODE HERE
        labgroupD = {}
        exec(data.replace(" ", ""))
        for l_id, l_data in labgroupD.items():
            teacher = Teacher.objects.get(id=l_data['teacher'])
            lg = LabGroup.objects.get_or_create(id=l_id, teacher=teacher, groupName=l_data['groupName'], language=l_data['language'], schedule=l_data['schedule'], maxNumberStudents=l_data['maxNumberStudents'])[0]
            lg.save()

    def theorygroup(self, data):
        "add theorygroups"
        # remove pass and ADD CODE HERE
        theorygroupD = {}
        exec(data.replace(" ", ""))
        for t_id, t_data in theorygroupD.items():
            t = TheoryGroup.objects.get_or_create(id=t_id, groupName=t_data['groupName'], language=t_data['language'])[0]
            t.save()

    def groupconstraints(self, data):
        "add group constrints"
        """ Follows which laboratory groups (4th column
            may be choosen by which theory groups (2nd column)
        """
        # remove pass and ADD CODE HERE
        groupconstraintsD = {}
        exec(data.replace(" ", ""))
        for t_id, t_data in groupconstraintsD.items():
            labGroup = LabGroup.objects.get(id=t_data['labGroup'])
            theoryGroup = TheoryGroup.objects.get(id=t_data['theoryGroup'])
            t = GroupConstraints.objects.get_or_create(id=t_id, labGroup=labGroup, theoryGroup=theoryGroup)[0]
            t.save()

    def pair(self, data):
        "create a few valid pairs"
        # remove pass and ADD CODE HERE
        pairD = {}
        exec(data.replace(" ", ""))
        for t_id, t_data in pairD.items():
            student1 = Student.objects.get(id=t_id)
            student2 = Student.objects.get(id=t_data['student2'])
            t = Pair.objects.get_or_create(id=t_id, student1_id=student1, student2_id=student2, validated=t_data['validated'])[0]
            t.save()

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
        stdReader = pd.read_csv("./core/management/commands/" + csvStudentFile)
        counter = 1000
        for index, row in stdReader.iterrows():
            grupoToeria = TheoryGroup.objects.get(id=row['grupo-teoria'])
            st = Student.objects.get_or_create(id=counter, first_name=row['Nombre'], last_name=row['Apellidos'], username=row['NIE'], password=row['DNI'], theoryGroup=grupoToeria)[0]
            st.save
            counter += 1

    def studentgrade(self, cvsStudentFileGrades):
        # read csv file
        # structure NIE	DNI	Apellidos	Nombre	group-Teoría	grade-practicas	gradeteoria
        # remove pass and ADD CODE HERE
        stdGradesReader = pd.read_csv("./core/management/commands/" + cvsStudentFileGrades)
        for index, row in stdGradesReader.iterrows():
            Student.objects.filter(username=row['NIE']).update(gradeLabLastYear=row['nota-practicas'], gradeTheoryLastYear=row['nota-teoria'])
