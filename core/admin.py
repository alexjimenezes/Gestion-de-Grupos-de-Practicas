from django.contrib import admin
from core.models import Student, LabGroup, Teacher, Pair, GroupConstraint, TheoryGroup, OtherConstraint


class StudentAdmin(admin.ModelAdmin):
    student_display = ['labGroup', 'theoryGroup', 'first_name', 'last_name', 'gradeTheoryLastYear', 'gradeLabLastYear', 'convalidationGranted']


class LabGroupAdmin(admin.ModelAdmin):
    labGroup_display = ['teacher', 'groupName', 'language', 'schedule', 'maxNumberStudents', 'counter']


class TeacherAdmin(admin.ModelAdmin):
    teacher_display = ['first_name', 'family_name']


class PairAdmin(admin.ModelAdmin):
    pair_display = ['student1_id', 'student2_id', 'validated', 'studentBreakRequest']


class GroupConstaintAdmin(admin.ModelAdmin):
    list_display = ['labGroup', 'theoryGroup']


class TheoryGroupAdmin(admin.ModelAdmin):
    list_display = ['groupName', 'language']


class OtherConstraintAdmin(admin.ModelAdmin):
    list_display = ['selectGroupStartDate', 'minGradeTheoryConv', 'minGradeLabConv']


# Register your models here.
admin.site.register(Student, StudentAdmin)
admin.site.register(LabGroup, LabGroupAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Pair, PairAdmin)
admin.site.register(GroupConstraint, GroupConstaintAdmin)
admin.site.register(TheoryGroup, TheoryGroupAdmin)
admin.site.register(OtherConstraint, OtherConstraintAdmin)