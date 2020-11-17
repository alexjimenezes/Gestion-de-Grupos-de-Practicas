from django import forms
# from core.models import Pair
from core.models import GroupConstraints, LabGroup, Student, Pair
from django.forms import ChoiceField

class RequestPairForm(forms.Form):
    secondMemberGroup = forms.ChoiceField(choices=[], label='Select student')
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user',None)
        super(RequestPairForm, self).__init__(*args, **kwargs)
        students = Pair.objects.filter(validated=True)
        students_id = []
        for o in students:
            students_id.append(o.student1.id)
            students_id.append(o.student2.id)
        students_id.append(self.user.id)
        qset = Student.objects.all().exclude(id__in = students_id).order_by('first_name')
        new_choices = []
        for q in qset:
            new_choices.append((q.id, q.last_name + ", " + q.first_name + " - " + str(q.theoryGroup) + " - " + str(q.labGroup)))
        self.fields['secondMemberGroup'].choices = new_choices

class BreakPairForm(forms.Form):
    myPair = forms.ChoiceField(choices=[], widget=forms.RadioSelect, label='Select pair')
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user',None)
        super(BreakPairForm, self).__init__(*args, **kwargs)
        pairs = Pair.objects.filter(student1=self.user) | Pair.objects.filter(student2=self.user)
        pairs = pairs.order_by('validated')
        new_choices = []
        for p in pairs:
            if p.validated:
                new_choices.append((p.id,   p.student1.first_name + " " + p.student1.last_name +
                                            " + " +
                                            p.student2.first_name + " " + p.student2.last_name
                                            ))
            else:
                new_choices.append((p.id,   p.student1.first_name + " " + p.student1.last_name +
                                            " > " +
                                            p.student2.first_name + " " + p.student2.last_name
                                            ))
        self.fields['myPair'].choices = new_choices

class RequestGroupForm(forms.Form):
    
    myLabGroup = forms.ChoiceField(choices=[], label='Select group')
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user',None)
        super(RequestGroupForm, self).__init__(*args, **kwargs)

        all_lab = GroupConstraints.objects.filter(theoryGroup = self.user.theoryGroup)
        labs = []
        for l in all_lab:
            if l.labGroup.counter < l.labGroup.maxNumberStudents:
                labs.append(l.labGroup.id)

        qset = LabGroup.objects.all().filter(id__in = labs)
        new_choices = []
        for q in qset:
            new_choices.append((q.id, q))
        self.fields['myLabGroup'].choices = new_choices


