from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import ScrumyGoals, GoalStatus
from django.contrib.auth.models import User, Group, auth
from django.contrib.auth import get_user_model, login, authenticate
from .forms import *
import random
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages


def index(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name,
                                            last_name=last_name)
            user.save()

            new_user = User.objects.get(username=username)
            group = Group.objects.get(name='Developer')
            group.user_set.add(new_user)

            messages.success(request, f'Your account has been created successfully!')

            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('/ayomidescrumy/home')
            else:
                return redirect('/ayomidescrumy/accounts/login')

    else:
        form = SignupForm()

    context = {'form': form}

    return render(request, 'ayomidescrumy/index.html', context)


# Create your views here.
def move_goal(request, goal_id):
    try:
        goals = ScrumyGoals.objects.get(goal_id=goal_id)
    except ObjectDoesNotExist:
        dictionary = {
            'error': 'A record with that goal id does not exist'
        }
        return render(request, 'ayomidescrumy/exception.html', dictionary)
    else:
        current_user = request.user
        usr_grp = request.user.groups.all()[0]
        if usr_grp == Group.objects.get(name='Developer') and current_user == goals.user:
            if request.method == 'POST':
                form = DeveloperChangeGoalForm(request.POST)
                if form.is_valid():
                    selected_status = form.save(commit=False)
                    selected = form.cleaned_data['goal_status']
                    choice = GoalStatus.objects.get(id=int(selected))
                    goals.goal_status = choice
                    goals.save()
                    return redirect("/ayomidescrumy/home")
                else:
                    return HttpResponse('You are not permitted to move goal to Done Status')
            else:
                form = DeveloperChangeGoalForm()

        elif usr_grp == Group.objects.get(name='Quality Assurance') and current_user == goals.user:
            if request.method == 'POST':
                form = QAChangeGoalForm(request.POST)
                if form.is_valid():
                    selected_status = form.save(commit=False)
                    selected = form.cleaned_data['goal_status']
                    choice = GoalStatus.objects.get(id=int(selected))

                    goals.goal_status = choice

                    goals.save()
                    return redirect("/ayomidescrumy/home")
                else:
                    return HttpResponse('Quality Assurance user can not move goals to weekly goals')

            else:
                form = QAChangeGoalForm()
        elif usr_grp == Group.objects.get(name='Quality Assurance') and current_user != goals.user:
            if goals.goal_status == 'Weekly Goal' or 'Daily Goal':
                return HttpResponse("You are only permitted to move other user's goal status from Verify status to "
                                        "Done Status")
            if request.method == 'POST':
                form = QAChangeGoalForm1(request.POST)
                if form.is_valid():
                    selected_status = form.save(commit=False)
                    selected = form.cleaned_data['goal_status']
                    choice = GoalStatus.objects.get(id=int(selected))
                    goals.goal_status = choice
                    goals.save()
                    return redirect("/ayomidescrumy/home")
                else:
                    return HttpResponse("You are only permitted to move other user's goal status from Verify status to "
                                        "Done Status")
            form = QAChangeGoalForm1()
        elif usr_grp == Group.objects.get(name='Owner') and current_user == goals.user:
            if request.method == 'POST':
                form = OwnerChangeGoalForm(request.POST)
                if form.is_valid():
                    selected_status = form.save(commit=False)
                    selected = form.cleaned_data['goal_status']
                    choice = GoalStatus.objects.get(id=int(selected))
                    goals.goal_status = choice
                    goals.save()
                    return redirect("/ayomidescrumy/home")
            form = OwnerChangeGoalForm()

        elif usr_grp == Group.objects.get(name='Owner') and current_user != goals.user:
            if request.method == 'POST':
                form = OwnerChangeGoalForm(request.POST)
                if form.is_valid():
                    selected_status = form.save(commit=False)
                    selected = form.cleaned_data['goal_status']
                    choice = GoalStatus.objects.get(id=int(selected))
                    goals.goal_status = choice
                    goals.save()
                    return redirect("/ayomidescrumy/home")
            form = OwnerChangeGoalForm()

        elif usr_grp == Group.objects.get(name='Admin'):
            if request.method == 'POST':
                form = AdminChangeGoalForm(request.POST)
                if form.is_valid():
                    selected_status = form.save(commit=False)
                    selected = form.cleaned_data['goal_status']
                    choice = GoalStatus.objects.get(id=int(selected))
                    goals.goal_status = choice
                    goals.save()
                    return redirect("/ayomidescrumy/home")
        else:
            return HttpResponse('You are not authorised to move this goal')
        form = AdminChangeGoalForm()
        return render(request, 'ayomidescrumy/moveGoal.html',
                      {'form': form, 'goals': goals, 'current_user': current_user, 'goal_name': goals.goal_name})


def add_goal(request):
    dev = User.objects.filter(groups__name__in=['Developer'])
    qa = User.objects.filter(groups__name__in=['Quality Assurance'])
    admin = User.objects.filter(groups__name__in=['Admin'])
    own = User.objects.filter(groups__name__in=['Owner'])
    if request.user in dev:
        form = DeveloprCreateGoalForm()
        dictionary = {'form': form, 'goal_status': GoalStatus.objects.get(status_name="Weekly Goal")}
        if request.method == 'POST':
            form = DeveloprCreateGoalForm(request.POST)
            if form.is_valid():
                user = User.objects.get(username=request.user.username)
                add_goal = ScrumyGoals()
                add_goal = form.save(commit=False)
                add_goal.goal_id = random.randint(1000, 9999)
                add_goal.created_by = user
                add_goal.moved_by = user
                add_goal.owner = user
                add_goal.user = user
                add_goal.goal_status = GoalStatus.objects.get(status_name="Weekly Goal")
                add_goal.save()
                return redirect("/ayomidescrumy/home")
            return HttpResponse("Invalid credentials provided, please fill out all fields")
        else:
            form = DeveloprCreateGoalForm()
            return render(request, 'ayomidescrumy/goal.html', dictionary)

    elif request.user in qa:
        form = QACreateGoalForm()
        dictionary = {'form': form, 'goal_status': GoalStatus.objects.get(status_name="Weekly Goal")}
        if request.method == 'POST':
            form = QACreateGoalForm(request.POST)
            if form.is_valid():
                user = User.objects.get(username=request.user.username)
                add_goal = ScrumyGoals()
                add_goal = form.save(commit=False)
                add_goal.goal_id = random.randint(1000, 9999)
                add_goal.created_by = user
                add_goal.moved_by = user
                add_goal.owner = user
                add_goal.user = user
                add_goal.goal_status = GoalStatus.objects.get(status_name="Weekly Goal")
                add_goal.save()
                return redirect("/ayomidescrumy/home")
            return HttpResponse("Invalid credentials provided, please fill out all fields")
        else:
            form = QACreateGoalForm()

        return render(request, 'ayomidescrumy/goal.html', dictionary)
    elif request.user in admin:
        form = CreateGoalForm()
        dictionary = {'form': form, 'goal_status': GoalStatus.objects.get(status_name="Weekly Goal")}

        if request.method == 'POST':
            form = CreateGoalForm(request.POST)
            if form.is_valid():
                user = User.objects.get(username=request.user.username)
                add_goal = ScrumyGoals()
                add_goal = form.save(commit=False)
                add_goal.goal_id = random.randint(1000, 9999)
                add_goal.created_by = user
                add_goal.moved_by = user
                add_goal.owner = user
                add_goal.user = user
                add_goal.goal_status = GoalStatus.objects.get(status_name="Weekly Goal")
                add_goal.save()
                return redirect("/ayomidescrumy/home")
            return HttpResponse("Invalid credentials provided, please fill out all fields")
        else:
            form = CreateGoalForm()

        return render(request, 'ayomidescrumy/goal.html', dictionary)
    elif request.user in own:
        form = OwnerCreateGoalForm()
        dictionary = {'form': form, 'goal_status': GoalStatus.objects.get(status_name="Weekly Goal")}

        if request.method == 'POST':
            form = OwnerCreateGoalForm(request.POST)
            if form.is_valid():
                user = User.objects.get(username=request.user.username)
                add_goal = ScrumyGoals()
                add_goal = form.save(commit=False)
                add_goal.goal_id = random.randint(1000, 9999)
                add_goal.created_by = user
                add_goal.moved_by = user
                add_goal.owner = user
                add_goal.user = user
                add_goal.goal_status = GoalStatus.objects.get(status_name="Weekly Goal")
                add_goal.save()
                return redirect("/ayomidescrumy/home")
            return HttpResponse("Invalid credentials provided, please fill out all fields")
        else:
            form = OwnerCreateGoalForm()

        return render(request, 'ayomidescrumy/goal.html', dictionary)


def home(request):
    goal = ScrumyGoals.objects.get(goal_name="Keep Learning Django")

    all_users = User.objects.all()
    weekly_goals = GoalStatus.objects.get(status_name="Weekly Goal")
    goals_weekly = weekly_goals.scrumygoals_set.all()

    daily_goals = GoalStatus.objects.get(status_name="Daily Goal")
    goals_daily = daily_goals.scrumygoals_set.all()

    verify_goals = GoalStatus.objects.get(status_name="Verify Goal")
    goals_verify = verify_goals.scrumygoals_set.all()

    done_goals = GoalStatus.objects.get(status_name="Done Goal")
    goals_done = done_goals.scrumygoals_set.all()

    dictionary = {'users': all_users, 'weekly': goals_weekly, 'daily': goals_daily, 'verify': goals_verify,
                  'done': goals_done, 'developer': Group.objects.first() }
    return render(request, "ayomidescrumy/home.html", dictionary)


def change_goal(request):
    if request.method == 'POST':
        form = ChangeGroup(request.POST)
        if form.is_valid():
            user = request.user
            g = Group.objects.all()
            for i in g:
                i.user_set.remove(user)
            group = form.cleaned_data['groups']
            group = Group.objects.get(id=group)

            group.user_set.add(user)
            messages.success(request, f'You successfully changed group to {group.name}')
            return redirect("/ayomidescrumy/home")
    else:
        form = ChangeGroup()
    context = {'form': form}

    return render(request, 'ayomidescrumy/changeGroup.html', context)
