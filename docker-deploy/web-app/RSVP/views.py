from django.shortcuts import render, redirect
from django import forms
from .forms import *
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.core.mail import send_mail

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, email = email, password=raw_password)
            login(request, user)
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def EventHomepage(request):
    curUser = get_object_or_404(User, pk = request.user.id)
    pendingRoleSet = curUser.role_set.filter(status = 'pending')
    pendingNum = pendingRoleSet.count();
    return render(request, 'event-homepage.html', {'curUser': curUser, 'pendingNum':pendingNum})

@login_required
def OwnerEvent(request):
    curUser = get_object_or_404(User, pk = request.user.id)
    return render(request, 'event-owner.html', {'curUser': curUser})

@login_required
def GuestEvent(request):
    curUser = get_object_or_404(User, pk = request.user.id)
    return render(request, 'event-guest.html', {'curUser': curUser})

@login_required
def VendorEvent(request):
    curUser = get_object_or_404(User, pk = request.user.id)
    return render(request, 'event-vendor.html', {'curUser': curUser})

@login_required
def pendingPage(request, role_id):
    form = pendingForm(request.POST)
    curRole = get_object_or_404(Role, pk = role_id)
    if request.method == 'POST' and form.is_valid():
        toRemoveRole = Role.objects.get(roleType = curRole.roleType, event=curRole.event, status='pending')
        toRemoveRole.users.remove(User.objects.get(pk = request.user.id))
        toAddRole = Role.objects.get(roleType = curRole.roleType, event=curRole.event, status=form.cleaned_data['status'])
        toAddRole.users.add(User.objects.get(pk = request.user.id))
        curUser = get_object_or_404(User, pk = request.user.id)
        pendingNum = curUser.role_set.filter(status = 'pending').count();
        return render(request, 'event-homepage.html', {'curUser': curUser, 'pendingNum':pendingNum})
    else :
        return render(request, 'pendingPage.html', {'curRole':curRole, 'form':form})

@login_required
def ownerPage(request, event_id):
    curUser = get_object_or_404(User, pk = request.user.id)
    curEvent = get_object_or_404(Event, pk = event_id)
    role = Role.objects.get(roleType = 'owner', event = curEvent, status = 'accept')
    if curUser.role_set.filter(pk = role.pk).exists():
        return render(request, 'owner-page.html', {'curUser': curUser, 'curEvent':curEvent})
    else:
        return HttpResponseRedirect(reverse('event-hompage'))

@login_required
def vendorPage(request, event_id):
    curUser = get_object_or_404(User, pk = request.user.id)
    curEvent = get_object_or_404(Event, pk = event_id)
    role = Role.objects.get(roleType = 'vendor', event = curEvent, status = 'accept')
    if curUser.role_set.filter(pk = role.pk).exists():
        return render(request, 'vendor-page.html', {'curUser': curUser, 'curEvent':curEvent})
    else:
        return HttpResponseRedirect(reverse('event-hompage'))

@login_required
def guestPage(request, event_id): 
    curUser = get_object_or_404(User, pk = request.user.id)
    curEvent = get_object_or_404(Event, pk = event_id)
    role = Role.objects.get(roleType = 'guest', event = curEvent, status = 'accept')
    if not curUser.role_set.filter(pk = role.pk).exists():
        return HttpResponseRedirect(reverse('event-hompage'))
    else:
        if request.method == 'POST' :
            try:
                selected_choice = get_object_or_404(Choice, pk = request.POST['choice'])
                selected_choice.votes += 1
                selected_choice.save()
                if  Response.objects.filter(user = curUser, question = selected_choice.question).exists() :
                    if Response.objects.filter(user = curUser, question = selected_choice.question).count() == 1:
                        oldResponse = Response.objects.get(user = curUser, question = selected_choice.question)
                        oldResponse.choice.votes -= 1
                        oldResponse.choice.save()
                        oldResponse.choice = selected_choice
                        oldResponse.save()
                    else:
                        selected_choice.votes -= 1
                        selected_choice.save()
                        return render(request, 'guest-page.html', {'curUser': curUser, 'curEvent':curEvent,
                         'error_message':"You have already chosen to take +1, you can only edit in that page!!!"})
                else :
                    newResponse = Response.objects.create(user = curUser, question = selected_choice.question, choice = selected_choice)
                    newResponse.save()
                return render(request, 'guest-page.html', {'curUser': curUser, 'curEvent':curEvent})
            except(KeyError, Choice.DoesNotExist):
                return render(request, 'guest-page.html', {'curUser': curUser, 'curEvent':curEvent, 'error_message':"You did not seleet a valid choice"})
        else :
            return render(request, 'guest-page.html', {'curUser': curUser, 'curEvent':curEvent})
        


@login_required
def finalizeQuestion(request, question_id): 
    form = FinalizeForm(request.POST)
    curQuestion = get_object_or_404(Question, pk = question_id)
    if request.method == 'POST' and form.is_valid():
        finalizationStatus = form.cleaned_data['finalization']
        curQuestion.finalization = finalizationStatus
        # print(curQuestion.finalization)
        curQuestion.save()
        curUser = get_object_or_404(User, pk = request.user.id)
        return render(request, 'vendor-page.html', {'curUser': curUser, 'curEvent':curQuestion.event})
    else :
        form = FinalizeForm();
        curQuestion = get_object_or_404(Question, pk = question_id)
        return render(request, 'finalize-page.html', {'curQuestion':curQuestion , 'form':form})

@login_required
def viewAnswerPage(request, event_id): #
    curUser = get_object_or_404(User, pk = request.user.id)
    curEvent = get_object_or_404(Event, pk = event_id)
    curQuestionSet = curEvent.question_set.all()
    responseSet = set()
    for curQuestion in curQuestionSet :
        if Response.objects.filter(user = curUser, question = curQuestion).exists() :
            if Response.objects.filter(user = curUser, question = curQuestion).count() == 2 :
                curResponse1 = Response.objects.filter(user = curUser, question = curQuestion)[0]
                curResponse2 = Response.objects.filter(user = curUser, question = curQuestion)[1]
                responseSet.add(curResponse1)
                responseSet.add(curResponse2)
            else :
                curResponse = Response.objects.get(user = curUser, question = curQuestion)
                responseSet.add(curResponse)
    return render(request, 'view-answer.html', {'responseSet':responseSet})



@login_required
def guestPlusOnePage(request, event_id): #
    curUser = get_object_or_404(User, pk = request.user.id)
    curEvent = get_object_or_404(Event, pk = event_id)
    role = Role.objects.get(roleType = 'guest', event = curEvent, status = 'accept')
    if not curUser.role_set.filter(pk = role.pk).exists():
        return HttpResponseRedirect(reverse('event-hompage'))
    else:   
        if request.method == 'POST' :
            try:
                selected_choice1 = get_object_or_404(Choice, pk = request.POST['choice'])
                selected_choice2 = get_object_or_404(Choice, pk = request.POST['choiceplus'])
                if request.POST['choice'] == request.POST['choiceplus']:
                    selected_choice1.votes += 2
                    selected_choice1.save()
                else:
                    selected_choice1.votes += 1
                    selected_choice1.save()
                    selected_choice2.votes += 1
                    selected_choice2.save()
                if  Response.objects.filter(user = curUser, question = selected_choice1.question).exists():
                    if Response.objects.filter(user = curUser, question = selected_choice1.question).count() > 1:
                        oldResponse1 = Response.objects.filter(user = curUser, question = selected_choice1.question)[0]
                        oldResponse1.choice.votes -= 1
                        oldResponse1.choice.save()
                        oldResponse2 = Response.objects.filter(user = curUser, question = selected_choice1.question)[1]
                        oldResponse2.choice.votes -= 1
                        oldResponse2.choice.save()
                        oldResponse1.choice = selected_choice1
                        oldResponse1.save()
                        oldResponse2.choice = selected_choice2
                        oldResponse2.save()
                    else:
                        if request.POST['choice'] == request.POST['choiceplus']:
                            selected_choice1.votes -= 2
                            selected_choice1.save()
                        else:
                            selected_choice1.votes -= 1
                            selected_choice1.save()
                            selected_choice2.votes -= 1
                            selected_choice2.save()
                        return render(request, 'guestPlusOne-page.html', {'curUser': curUser, 'curEvent':curEvent,
                         'error_message':"You have already chosen to not take +1, you can only edit in that page!!!"})
                else :
                    newResponse1 = Response.objects.create(user = curUser, question = selected_choice1.question, choice = selected_choice1)
                    newResponse1.save()
                    newResponse2 = Response.objects.create(user = curUser, question = selected_choice2.question, choice = selected_choice2)
                    newResponse2.save()
                return render(request, 'guestPlusOne-page.html', {'curUser': curUser, 'curEvent':curEvent})
            except:
                return render(request, 'guestPlusOne-page.html', {'curUser': curUser, 'curEvent':curEvent,
                 'error_message':"You did not seleet a valid choice"})
        else :
            return render(request, 'guestPlusOne-page.html', {'curUser': curUser, 'curEvent':curEvent})

###############################
@login_required
def freeText(request, question_id): #
    form = TextForm(request.POST) 
    curQuestion = get_object_or_404(Question, pk = question_id)
    curUser = get_object_or_404(User, pk = request.user.id)
    curEvent = curQuestion.event
    if request.method == 'POST' and form.is_valid():
        if  Response.objects.filter(user = curUser, question = curQuestion).exists() :
            oldResponse = Response.objects.get(user = curUser, question = curQuestion)
            oldResponse.choice.choice_text  =  form.cleaned_data['answer']
            oldResponse.choice.save()
            oldResponse.save()
        else :
            answer = form.cleaned_data['answer']
            curChoice = Choice.objects.create(question = curQuestion, choice_text = answer)
            curChoice.save()
            curResponse = Response.objects.create(user = curUser, question = curQuestion, choice = curChoice)
            curResponse.save()
            
        return HttpResponseRedirect(reverse('guest-page', args=(curEvent.id, )))
    else :
        form = TextForm()
        return render(request, 'free-text-question.html', {'curQuestion': curQuestion, 'form':form})

@login_required
def invitePage(request, event_id): 
    curUser = get_object_or_404(User, pk = request.user.id)
    curEvent = get_object_or_404(Event, pk = event_id)
    form = InviteForm(request.POST)
    if request.method == 'POST' and form.is_valid():
        try:
            choice = form.cleaned_data['role']
            userWantToInvite = form.cleaned_data['user_name']
            curRole = Role.objects.get(roleType = choice, event=curEvent, status='pending')
            # if 
            curRole.users.add(User.objects.get(username = userWantToInvite))
            return HttpResponseRedirect(reverse('owner-page', args=(event_id,)))
        except:
            form = InviteForm()
            return render(request, 'invite-page.html', {'curEvent':curEvent, 'form':form, 
                'error_message':"Cannot find the person you want to invite."})
    else :
        form = InviteForm()
        return render(request, 'invite-page.html', {'curEvent':curEvent, 'form':form})

@login_required
def createEvent(request):
    if request.method == 'POST':
        try :
            form = EventForm(request.POST)
            curEvent = form.save()
            ownerAccept = Role.objects.create(roleType = 'owner', event=curEvent, status='accept')
            ownerAccept.users.add(User.objects.get(pk = request.user.id))
            ownerAccept.save()
            ownerPending = Role.objects.create(roleType = 'owner', event=curEvent, status='pending')
            ownerPending.save()
            ownerDeny = Role.objects.create(roleType = 'owner', event=curEvent, status='deny')
            ownerDeny.save()

            vendorAccept = Role.objects.create(roleType = 'vendor', event=curEvent, status='accept')
            vendorAccept.save()
            vendorPending = Role.objects.create(roleType = 'vendor', event=curEvent, status='pending')
            vendorPending.save()
            vendorDeny = Role.objects.create(roleType = 'vendor', event=curEvent, status='deny')
            vendorDeny.save()

            guestAccept = Role.objects.create(roleType = 'guest', event=curEvent, status='accept')
            guestAccept.save()
            guestPending = Role.objects.create(roleType = 'guest', event=curEvent, status='pending')
            guestPending.save()
            guestDeny = Role.objects.create(roleType = 'guest', event=curEvent, status='deny')
            guestDeny.save()
            return HttpResponseRedirect(reverse('event-hompage', args=()))
        except: 
            return render(request, 'create-event.html', {'form':form,
                'error_message':"You did not enter a valid date: yyyy-mm-dd"})

    else :
        form = EventForm()
        return render(request, 'create-event.html', {'form':form})

@login_required
def createChoice(request, question_id):
    newChoice = ChoiceForm(request.POST)
    if request.method == 'POST' and newChoice.is_valid():
        curQuestion = get_object_or_404(Question, pk = question_id)
        curChoice = Choice.objects.create(question = curQuestion, choice_text = newChoice.cleaned_data['choice_text'], )
        curChoice.save()
        return HttpResponseRedirect(reverse('choice-create-page', args=(question_id,)))
    else :
        form = ChoiceForm()
        question = get_object_or_404(Question, pk = question_id)
        if question.question_type == 'Multi' :
            choice_set = question.choice_set.all()
            return render(request, 'create-choice.html', {'form':form, 'question':question, 'choice_set':choice_set})
        else :
            curUser = get_object_or_404(User, pk = request.user.id)
            return render(request, 'owner-page.html', {'curUser': curUser, 'curEvent':question.event})

@login_required
def createQuestion(request, event_id):
    newQuestion = QuestionForm(request.POST)
    if request.method == 'POST' and newQuestion.is_valid():
        curEvent = get_object_or_404(Event, pk = event_id)

        curQuestion = Question.objects.create(
            question_text = newQuestion.cleaned_data['question_text'],
            event = curEvent,
            question_type = newQuestion.cleaned_data['question_type'],
            vendor_permission = newQuestion.cleaned_data['vendor_permission'])
        curQuestion.save()
        return HttpResponseRedirect(reverse('choice-create-page', args=(curQuestion.id,)))
    else :
        form = QuestionForm()
        return render(request, 'create-question.html', {'form':form})

@login_required
def editQuestion(request, question_id):
    curQuestion = get_object_or_404(Question, pk = question_id)
    newQuestion = editQuestionForm(request.POST)
    if request.method == 'POST' and newQuestion.is_valid():
        for curResponse in Response.objects.filter(question = curQuestion):
            emailQuestion(curResponse, curQuestion, 'changed')
        curQuestion.question_text = newQuestion.cleaned_data['question_text']
        curQuestion.save()
    form = editQuestionForm()
    return render(request, 'edit-question.html', {'form':form, 'question':curQuestion})
    
@login_required
def editChoice(request, choice_id):
    curChoice = get_object_or_404(Choice, pk = choice_id)
    newChoice = ChoiceForm(request.POST)
    if request.method == 'POST' and newChoice.is_valid():
        for curResponse in Response.objects.filter(choice = curChoice):
            emailChoice(curResponse, curChoice, 'changed')
        curChoice.choice_text = newChoice.cleaned_data['choice_text']
        curChoice.save()
    form = ChoiceForm()
    return render(request, 'edit-choice.html', {'form':form, 'choice':curChoice})

@login_required
def deleteQuestion(request, question_id):
    curQuestion = get_object_or_404(Question, pk = question_id)
    eventId = curQuestion.event.id
    for curResponse in Response.objects.filter(question = curQuestion):
        emailQuestion(curResponse, curQuestion, 'deleted')
    Response.objects.filter(question = curQuestion).delete()
    curQuestion.choice_set.all().delete()
    curQuestion.delete()
    return HttpResponseRedirect(reverse('owner-page', args=(eventId,)))

@login_required
def deleteChoice(request, choice_id):
    curChoice = get_object_or_404(Choice, pk = choice_id)
    questionId = curChoice.question.id
    for curResponse in Response.objects.filter(choice = curChoice):
        emailChoice(curResponse, curChoice, 'deleted')
    Response.objects.filter(choice = curChoice).delete()
    curChoice.delete()
    return HttpResponseRedirect(reverse('question-edit-page', args=(questionId,)))
    

def emailChoice(curResponse, curChoice, changeType):
    send_mail(
        'Dear ' + curResponse.user.__str__(),
        'You are receiving this email because the choice <' + curChoice.choice_text + '> of the question <' 
        + curChoice.question.question_text + '> in event <'+  curChoice.question.event.event_name 
        +'> has been '+ changeType +', please login and check it.',
        'RSVPserver@duke.edu',
        [curResponse.user.email,],
        fail_silently = False,
    )

def emailQuestion(curResponse, curQuestion, changeType):
    send_mail(
        'Dear ' + curResponse.user.__str__(),
        'You are receiving this email because the question <' + curQuestion.question_text + '> in the event <' 
        + curQuestion.event.event_name + '> has been '+ changeType +', please login and check it.',
        'RSVPserver@duke.edu',
        [curResponse.user.email,],
        fail_silently = False,
    )

