from django.forms import ModelForm
from django.contrib.auth.models import User, Group
from .models import ScrumyGoals, GoalStatus
from django import forms


class SignupForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']


class CreateGoalForm(ModelForm):
    # goal_status = GoalStatus.objects.all()
    # goal_status = forms.ChoiceField(choices=[(choice.pk, choice) for choice in goal_status.order_by('id')[0:1]])
    class Meta:
        model = ScrumyGoals
        fields = ['goal_name']


class DeveloperChangeGoalForm(forms.ModelForm):
    queryset = GoalStatus.objects.all()
    goal_status = forms.ChoiceField(choices=[(choice.pk, choice) for choice in queryset.order_by('id')[0:3]])

    class Meta():
        model = GoalStatus
        fields = ['goal_status']


class QAChangeGoalForm(forms.ModelForm):
    queryset = GoalStatus.objects.all()
    goal_status = forms.ChoiceField(choices=[(choice.pk, choice) for choice in queryset.order_by('id')[1:4]])

    class Meta:
        model = GoalStatus
        fields = ['goal_status']


class QAChangeGoalForm1(forms.ModelForm):
    queryset = GoalStatus.objects.all()
    goal_status = forms.ChoiceField(choices=[(choice.pk, choice) for choice in queryset.order_by('id')[2:4]])

    class Meta:
        model = GoalStatus
        fields = ['goal_status']


class OwnerChangeGoalForm(forms.ModelForm):
    queryset = GoalStatus.objects.all()
    goal_status = forms.ChoiceField(choices=[(choice.pk, choice) for choice in queryset.order_by('id')[:4]])

    class Meta:
        model = GoalStatus
        fields = ['goal_status']


class AdminChangeGoalForm(forms.ModelForm):
    queryset = GoalStatus.objects.all()
    goal_status = forms.ChoiceField(choices=[(choice.pk, choice) for choice in queryset.order_by('id')[:4]])

    class Meta:
        model = GoalStatus
        fields = ['goal_status']


#create goal form

class DeveloprCreateGoalForm(forms.ModelForm):
    # goal_status = GoalStatus.objects.all()
    # goal_status = forms.ChoiceField(choices=[(choice.pk, choice) for choice in goal_status.order_by('id')[0:1]])
    class Meta:
        model = ScrumyGoals
        fields = ['goal_name']

class QACreateGoalForm(forms.ModelForm):
    # goal_status = GoalStatus.objects.all()
    # goal_status = forms.ChoiceField(choices=[(choice.pk, choice) for choice in goal_status.order_by('id')[0:1]])
    class Meta:
        model = ScrumyGoals
        fields = ['goal_name']

class OwnerCreateGoalForm(forms.ModelForm):
    # goal_status = GoalStatus.objects.all()
    # goal_status = forms.ChoiceField(choices=[(choice.pk, choice) for choice in goal_status.order_by('id')[0:1]])
    class Meta:
        model = ScrumyGoals
        fields = ['goal_name']

class ChangeGoalForm(forms.ModelForm):
    queryset = GoalStatus.objects.all()
    goal_status = forms.ChoiceField(choices=[(choice.pk, choice) for choice in queryset[:3]])

    class Meta:
        model = GoalStatus
        fields = ['goal_status']


class ChangeGroup(forms.ModelForm):
    queryset = Group.objects.all()
    groups = forms.ChoiceField(choices=[(choice.pk, choice) for choice in queryset.order_by('id')[0:4]])

    class Meta():
        model = Group
        fields = ['groups']


