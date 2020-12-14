from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import render, redirect
# flask8 not used: from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.models import Student, Pair, OtherConstraints, LabGroup
from core.forms import RequestPairForm, RequestGroupForm, BreakPairForm


def index(request):
    context_dict = {}
    pairs = []
    # crear una lista de parejas donde el usuario
    if request.user.is_authenticated:
        try:
            pairs += Pair.objects.filter(student1=request.user.id)
        except:
            pass
        try:
            pairs += Pair.objects.filter(student2=request.user.id)
        except:
            pass

    can_request_pair = True
    if Pair.objects.filter(student1=request.user.id) or \
            Pair.objects.filter(student2=request.user.id, validated=True):
        can_request_pair = False

    pairs_accepted = False
    if Pair.objects.filter(student1=request.user.id, validated=True) or\
            Pair.objects.filter(student2=request.user.id, validated=True):
        pairs_accepted = True

    pending_pairs = False
    if Pair.objects.filter(student1=request.user.id, validated=False):
        pending_pairs = True

    pair_to_join = False
    if Pair.objects.filter(student2=request.user.id, validated=False):
        pair_to_join = True

    context_dict['pairs'] = pairs
    context_dict['can_request_pair'] = can_request_pair
    context_dict['pairs_accepted'] = pairs_accepted
    context_dict['pending_pairs'] = pending_pairs
    context_dict['pair_to_join'] = pair_to_join

    return render(request, 'home.html', context=context_dict)


def user_login(request):
    # If user already logged in redirect to home page
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in, \
            please logout to log in with another user!')
        return redirect(reverse('index'))
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse('index'))
                else:
                    return HttpResponse("Your account is disabled.")
            else:
                messages.error(request, 'The username or password\
                     are incorrect, please retry.')
                return render(request, 'login.html')

        # The request is not a HTTP POST, so display the login form.
        else:
            return render(request, 'login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('index'))


@login_required
def convalidation(request):
    if request.user.convalidationGranted:
        messages.error(request, 'Convalidation: Your grades\
             have already been convalidated')
        return redirect(reverse('index'))
    # Get the grades needed
    theory = OtherConstraints.objects.all()[0].minGradeTheoryConv
    lab = OtherConstraints.objects.all()[0].minGradeLabConv
    # Check if requirements are met
    if request.user.gradeTheoryLastYear >= theory \
            and request.user.gradeLabLastYear >= lab:
        request.user.convalidationGranted = True
        request.user.save()
        mensaje = "Convalidation: Our team of teachers decided\
                     to convalidate your grades.\
                     You satisfy them.\n This is because your\
                     theory grade was >= " + str(theory) + " and\
                     your lab grade was >= " + str(lab) + ". Congratulations!"
        messages.success(request, mensaje)
    else:
        mensaje = "Convalidation: Our team of teachers\
                     decided to reject your convalidation request.\
                     You do not satify them.\n This is because your\
                     theory grade was < " + str(theory) + " and / or\
                     your lab grade was < " + str(lab) + "."
        messages.error(request, mensaje)
    # Go back to homepage
    return redirect(reverse('index'))


@login_required
def applypair(request):
    pairs = Pair.objects.all()
    for p in pairs:
        # Si la pareja esta validada y
        #  el usuario forma parte de ella volver a index con el respectivo
        # mensaje de error
        if p.validated:
            if p.student1.id == request.user.id or \
                    p.student2.id == request.user.id:
                messages.error(request, "User has already selected a pair error:\
                     You are already in an established pair.\
                     In case you and your partner want to split,\
                    both of you should send a request to disolve the pair.")
                return redirect(reverse('index'))
        # Si la pareja no está validada pero
        #  el usuario ha solicitado crear una pareja volver a index
        # con el respectivo mensaje de error
        elif p.student1.id == request.user.id:
            messages.error(request, "User has already selected a pair error:\
                                     You have already requested\
                                     to be in a pair.\
                                     Please, either wait for your partner to\
                                     or request to disolve your petition. ")
            return redirect(reverse('index'))

    if request.method == 'POST':
        form = RequestPairForm(request.POST, user=request.user)

        if form.is_valid():
            choice = form.cleaned_data['secondMemberGroup']
            student_chosen = Student.objects.get(id=choice)
            # Comprobamos
            #  si nuestro usuario ya forma parte de alguna pareja validada

            pareja_validada = Pair.objects.filter(validated=True) & (
                Pair.objects.filter(
                    student1=request.user) | Pair.objects.filter(
                        student2=request.user))

            # O si ya ha emitido una peticion
            pareja1 = Pair.objects.filter(student1=request.user)
            # O si le han emitido una peticion
            pareja2 = Pair.objects.filter(
                student1=student_chosen, student2=request.user)
            if pareja1 or pareja_validada:
                messages.error(request, "User with a pending\
                     request cannot send a new one.")
            elif pareja2:
                p = pareja2[0]
                p.validated = True
                p.save()
                messages.success(request, "\
                    Your pair has been successully validated!")
                Pair.objects.filter(
                    student2=request.user, validated=False).delete()
                Pair.objects.filter(
                    student2=student_chosen, validated=False).delete()
            else:
                p = Pair.objects.create(
                    student1=request.user, student2=student_chosen)
                p.save()
                messages.success(request, "\
                    Your request has been successfully created!")
            return redirect(reverse('index'))
    else:
        form = RequestPairForm(user=request.user)
    return render(request, 'request_pair.html', {'form': form})


@login_required
def breakpair(request):
    if request.user.labGroup:
        messages.error(request, "\
            Break Pair: You cannot break a pair\
                 if you have already chosen a group.")
        return redirect(reverse('index'))

    if not (
        Pair.objects.filter(
            student1=request.user) | Pair.objects.filter(
                student2=request.user)):
        messages.error(request, "Break Pair:\
             Could not process your request,\
                  currently you do not have any pair to break.")
        return redirect(reverse('index'))

    if request.method == 'POST':
        form = BreakPairForm(request.POST, user=request.user)
        if form.is_valid():
            choice = Pair.objects.get(
                id=form.cleaned_data['myPair'])
            if not choice:
                messages.error("Break Pair:\
                     Could not process your request,\
                         the information provided does not match any pair.")
                return redirect(reverse('index'))
            if choice.student1 == request.user:
                other_student = choice.student2
            else:
                other_student = choice.student1
            if choice.validated:
                if not choice.studentBreakRequest or\
                     choice.studentBreakRequest == request.user:
                    choice.studentBreakRequest = request.user
                    choice.save()
                    messages.success(request,  "Break Pair: The pair selected has been marked as non validated.\
                                                Once your pair mate sybmits a\
                                                 request to break\
                                                 it will be deleted.")
                elif choice.studentBreakRequest \
                        == other_student:
                    choice.delete()
                    messages.success(request,  "\
                        Break Pair: The pair selected\
                         has been successfully removed.")
            else:
                choice.delete()
                messages.success(request,  "Break Pair:\
                     The pair selected has been successfully removed.")
            return redirect(reverse('index'))
    else:
        form = BreakPairForm(user=request.user)
    return render(request, 'break_pair.html', {'form': form})


@login_required
def applygroup(request):
    if request.user.labGroup:
        messages.error(request, "You already have been assigned to a group!")
        return redirect(reverse('index'))
    if request.method == 'POST':
        form = RequestGroupForm(request.POST, user=request.user)

        if form.is_valid():
            group_choice = LabGroup.objects.get(
                id=form.cleaned_data['myLabGroup'])
            if request.user.labGroup:
                messages.error(request, "\
                    You have been assigned to a group already!")
            else:
                lg = LabGroup.objects.get(pk=group_choice.id)

                qset = Pair.objects.filter(validated=True) & (
                    Pair.objects.filter(
                        student1=request.user) | Pair.objects.filter(
                            student2=request.user))
                if qset:
                    if lg.counter + 2 <= lg.maxNumberStudents:
                        st1 = qset.first().student1
                        st1.labGroup = lg
                        st1.save()
                        st2 = qset.first().student2
                        st2.labGroup = lg
                        st2.save()
                        lg.counter += 2
                        lg.save()
                        messages.success(request, "\
                            You and your partner have been assigned\
                             to the selected group.")
                    else:
                        messages.error(request, "\
                            There is not enouhg space for a pair\
                             in this group! Try a different one.")
                else:
                    lg.counter += 1
                    lg.save()
                    request.user.labGroup = lg
                    request.user.save()
                    messages.success(request, "\
                        You and your partner have been assigned\
                         to the selected group.")

            return redirect(reverse('index'))
    else:
        form = RequestGroupForm(user=request.user)
    return render(request, 'request_group.html', {'form': form})
