from core.models import (Student, OtherConstraints,
                         Pair, TheoryGroup, GroupConstraints,
                         LabGroup)


def exist_create_st(std):
    try:
        student_1000 = Student.objects.get(pk=std)
    except Student.DoesNotExist:
        st = Student.objects.get_or_create(id=std, first_name="student", last_name=str(std), username=("student" + str(std)), theoryGroup=120)
        st.set_password(str(std) + "student")
        st.save()


def create_pair_1000_1001():
    student1 = Student.objects.get(id=1000)
    student2 = Student.objects.get(id=1001)
    t = Pair.objects.get_or_create(id=t_id, student1=student1, student2=student2, validated=t_data['validated'])
    t.save()

def pair_of_1000_validated():
    student = Student.objects.get(id=1000)
    pairs = Pair.objects.get(student1=student)

    for p in pairs:
        print(Pair.__str__(p)) 
        p.validated = True
        p.save()

def create_other_constraints():
     oc_plus1day = OtherConstraints.objects.get_or_create(selectGroupStartDate=timezone.now()+datetime.timedelta(days=1))
     oc_plus1day.save()

def get_all_other_constraints():
    all_other_constraints = OtherConstraints.objects.all()
    first = all_other_constraints[0]

    if datetime.now() < first.selectGroupStartDate:
        return true
    else:
        return false