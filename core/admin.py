from django.contrib import admin
<<<<<<< HEAD
from core.models import (Student, LabGroup,
                         Teacher, Pair,
                         GroupConstraints, TheoryGroup,
                         OtherConstraints)
from django.contrib.auth.admin import UserAdmin


""" class StudentAdmin(admin.ModelAdmin):
    student_display = ['labGroup', 'theoryGroup', 'first_name', 'last_name',
    'gradeTheoryLastYear', 'gradeLabLastYear', 'convalidationGranted']
    readonly_fields = ('id',)
 """


class LabGroupAdmin(admin.ModelAdmin):
    labGroup_display = ['teacher',
                        'groupName',
                        'language',
                        'schedule',
                        'maxNumberStudents',
                        'counter']
=======
from core.models import Student, LabGroup, Teacher, Pair, GroupConstraints,\
     TheoryGroup, OtherConstraints
from django.contrib.auth.admin import UserAdmin


class LabGroupAdmin(admin.ModelAdmin):
    labGroup_display = ['teacher', 'groupName', 'language',
                        'schedule', 'maxNumberStudents', 'counter']
>>>>>>> 883b520436e2b991423d05da16486f9f519112e2
    readonly_fields = ('id',)


class TeacherAdmin(admin.ModelAdmin):
    teacher_display = ['first_name', 'last_name']
    readonly_fields = ('id',)


class PairAdmin(admin.ModelAdmin):
    pair_display = ['student1', 'student2', 'validated', 'studentBreakRequest']
    readonly_fields = ('id',)


class GroupConstaintAdmin(admin.ModelAdmin):
    list_display = ['labGroup', 'theoryGroup']
    readonly_fields = ('id',)


class TheoryGroupAdmin(admin.ModelAdmin):
    list_display = ['groupName', 'language']
    readonly_fields = ('id',)


class OtherConstraintAdmin(admin.ModelAdmin):
    list_display = ['selectGroupStartDate',
                    'minGradeTheoryConv', 'minGradeLabConv']
    readonly_fields = ('id',)


admin.site.register(Student, UserAdmin)
<<<<<<< HEAD
# admin.site.register(Student, StudentAdmin)
=======
>>>>>>> 883b520436e2b991423d05da16486f9f519112e2
admin.site.register(LabGroup, LabGroupAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Pair, PairAdmin)
admin.site.register(GroupConstraints, GroupConstaintAdmin)
admin.site.register(TheoryGroup, TheoryGroupAdmin)
admin.site.register(OtherConstraints, OtherConstraintAdmin)
