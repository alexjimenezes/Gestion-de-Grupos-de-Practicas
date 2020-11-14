from django.contrib import admin
from core.models import Student, LabGroup, Teacher, Pair, GroupConstraints, TheoryGroup, OtherConstraints
from django.contrib.auth.admin import UserAdmin


""" class StudentAdmin(admin.ModelAdmin):
    student_display = ['labGroup', 'theoryGroup', 'first_name', 'last_name', 'gradeTheoryLastYear', 'gradeLabLastYear', 'convalidationGranted']
    readonly_fields = ('id',)
 """

class LabGroupAdmin(admin.ModelAdmin):
    labGroup_display = ['teacher', 'groupName', 'language', 'schedule', 'maxNumberStudents', 'counter']
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
    list_display = ['selectGroupStartDate', 'minGradeTheoryConv', 'minGradeLabConv']
    readonly_fields = ('id',)


# Register your models here.
admin.site.register(Student, UserAdmin)
#admin.site.register(Student, StudentAdmin)
admin.site.register(LabGroup, LabGroupAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Pair, PairAdmin)
admin.site.register(GroupConstraints, GroupConstaintAdmin)
admin.site.register(TheoryGroup, TheoryGroupAdmin)
admin.site.register(OtherConstraints, OtherConstraintAdmin)