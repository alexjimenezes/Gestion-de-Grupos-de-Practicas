import pytz
from datetime import timedelta, datetime, date

from django.test import TestCase

from core.models import (TheoryGroup,
                         Student, Pair,
                         OtherConstraints)


class QueryTest(TestCase):
    def setUp(self):
        self.thG = TheoryGroup()
        self.thG.groupName = "120"
        self.thG.language = "En"
        self.thG.save()
        self.s = Student.objects.create(
            id=1000, first_name="student",
            last_name=str(1000),
            username=("student" + str(1000)), theoryGroup=self.thG)
        self.s.save()
        self.s1 = Student.objects.create(
            id=1001, first_name="student",
            last_name=str(1001), username=("student" + str(1001)),
            theoryGroup=self.thG)
        self.s1.save()

    def test_exist_create_st(self):
        print("\nTest01")
        try:
            self.s = Student.objects.create(
                id=1000, first_name="student",
                last_name=str(1000), username=("student" + str(1000)),
                theoryGroup=self.thG)
            self.s.save()
        except:
            pass
        try:
            self.s1 = Student.objects.create(
                id=1001, first_name="student",
                last_name=str(1001), username=("student" + str(1001)),
                theoryGroup=self.thG)
            self.s1.save()
        except:
            pass

    def test_pair_1000_1001(self):
        print("\nTest02")
        student1 = Student.objects.get(pk=1000)
        student2 = Student.objects.get(id=1001)
        t = Pair.objects.create(
            id=123, student1=student1,
            student2=student2, validated=False)
        t.save()
        print("\nPair created!\n")

        pairs = Pair.objects.all().filter(student1=student1)

        for p in pairs:
            print(Pair.__str__(p))
            p.validated = True
            p.save()

    def test_other_constraints(self):
        print("\nTest03")
        date1 = date.today() + timedelta(days=1)
        oc_plus1day = OtherConstraints.objects.create(
            selectGroupStartDate=date1)
        oc_plus1day.save()

        all_other_constraints = OtherConstraints.objects.all()
        first = all_other_constraints[0]

        date1 = datetime.today()
        date2 = first.selectGroupStartDate

        date1 = date1.replace(tzinfo=pytz.UTC)
        date2 = date2.replace(tzinfo=pytz.UTC)

        if date1 < date2:
            aux = True
        else:
            aux = False

        self.assertEqual(aux, True)
