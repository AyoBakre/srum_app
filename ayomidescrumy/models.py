from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class GoalStatus(models.Model):
    status_name = models.CharField(max_length=250)

    def __str__(self):
        return self.status_name


class ScrumyGoals(models.Model):
    goal_name = models.CharField(max_length=250)
    goal_id = models.IntegerField(default=1)
    created_by = models.CharField(max_length=250)
    moved_by = models.CharField(max_length=250)
    owner = models.CharField(max_length=250)
    goal_status = models.ForeignKey(
        GoalStatus, on_delete=models.PROTECT, null=True)
    user = models.ForeignKey(User, related_name='user',
                             on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.goal_name


class ScrumyHistory(models.Model):
    moved_by = models.CharField(max_length=250)
    created_by = models.CharField(max_length=250)
    moved_from = models.CharField(max_length=250)
    moved_to = models.CharField(max_length=250)
    time_of_action = models.DateTimeField(auto_now_add=True, null=True)
    goal = models.ForeignKey(
        ScrumyGoals, on_delete=models.PROTECT)

    def __str__(self):
        return self.created_by
