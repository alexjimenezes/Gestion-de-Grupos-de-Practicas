from django import forms
# from core.models import Pair
from core.models import GroupConstraints, LabGroup, Student, Pair
from django.forms import ModelChoiceField

class RequestPairForm(forms.Form):
    choices = forms.ModelChoiceField(queryset=Student.objects.none(), label='select student')
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user',None)
        super(RequestPairForm, self).__init__(*args, **kwargs)
        students = Pair.objects.filter(validated=True)
        students_id = []
        for o in students:
            students_id.append(o.student1.id)
            students_id.append(o.student2.id)
        qset = Student.objects.all().exclude(id = self.user.id).exclude(id__in = students_id).order_by('first_name')
        self.fields['choices'].queryset = qset
    
    #qset = Student.objects.filter(id != user.id)
    #name = forms.ModelChoiceField(queryset=qset, initial=0)



class RequestGroupForm(forms.Form):
    
    #group = forms.ModelChoiceField(queryset=LabGroup.objects.all(), initial=0)

    choices = forms.ModelChoiceField(queryset=LabGroup.objects.none(), label='select student')
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user',None)
        super(RequestGroupForm, self).__init__(*args, **kwargs)

        all_lab = GroupConstraints.objects.filter(theoryGroup = self.user.theoryGroup)
        labs = LabGroup.objects.filter(groupName = all_lab.labGroup)

        self.fields['choices'].queryset = labs


