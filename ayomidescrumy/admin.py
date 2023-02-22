from django.contrib import admin

# Register your models here.
from ayomidescrumy.models import ScrumyGoals, ScrumyHistory, GoalStatus


admin.site.register(ScrumyGoals)
admin.site.register(ScrumyHistory)
admin.site.register(GoalStatus)
