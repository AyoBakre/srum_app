from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import ScrumyGoals, GoalStatus
from django.contrib.auth.models import User, Group
from .forms import SignupForm, CreateGoalForm
import random


def index(request):
    # goal = ScrumyGoals.objects.filter(goal_name='Learn Django')
    # return HttpResponse(goal)

    form = SignupForm()

    if request.method == 'POST':
        form = SignupForm(request.POST)
        form.save()
        user = User.objects.get(username=request.POST['username'])
        my_group = Group.objects.get(name='Developer')
        my_group.user_set.add(user)

        if user.groups.filter(name='Developer').exists():
            return HttpResponse("Your account has been created successfully")

    elif request.method == 'GET':
        form = SignupForm()

    context = {'form': form}

    return render(request, 'ayomidescrumy/index.html', context)

    # return HttpResponse("This is a Scrum Application")


# Create your views here.
def move_goal(request, goal_id):
    try:
        goal = ScrumyGoals.objects.get(goal_id=goal_id)
    except Exception as e:
        dictionary = {
            'error': 'A record with that goal id does not exist'
        }
        return render(request, 'ayomidescrumy/exception.html', dictionary)
    else:
        return HttpResponse(goal.goal_name)


def add_goal(request):
    '''user = User.objects.first()
    random_number = random.randint(1000, 9999)
    weekly_goal = GoalStatus.objects.get(status_name='Weekly Goal')

    new_goal = ScrumyGoals(goal_name='Keep Learning Django', goal_id=random_number,
                           created_by='Louis', moved_by='Louis', owner='Louis', goal_status=weekly_goal, user=user)
    new_goal.save()
    return HttpResponse(new_goal)'''

    form = CreateGoalForm()
    if request.method == 'POST':
        form = CreateGoalForm(request.POST)
        form.save()

    elif request.method == 'GET':
        form = CreateGoalForm()

    context = {'form': form}

    return render(request, 'ayomidescrumy/goal.html', context)


def home(request):
    my_users = User.objects.all()
    my_first_user = my_users[0]
    my_goals = my_first_user.user.all()
    goal_status = GoalStatus.objects.all()
    weekly_goal = goal_status[0]
    daily_goal = goal_status[1]
    verify_goal = goal_status[2]
    done_goal = goal_status[3]

    dictionary = {
        'my_first_user': my_first_user,
        'weekly_goal': weekly_goal,
        'daily_goal': daily_goal,
        'verify_goal': verify_goal,
        'done_goal': done_goal,
        'my_goals': my_goals,
        'my_users': my_users,
    }

    return render(request, 'ayomidescrumy/home.html', dictionary)
