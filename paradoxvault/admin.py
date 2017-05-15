# -*- coding: utf-8 -*-

from django.contrib import admin

from paradoxvault.models import *


class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)


class DifficultyAdmin(admin.ModelAdmin):
    list_display = ('name', 'difficulty')


class SingleSelectionAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer', 'score', 'selectionA', 'selectionB', 'selectionC', 'selectionD', 'difficulty')


admin.site.register(Subject, SubjectAdmin)
admin.site.register(Difficulty, DifficultyAdmin)
admin.site.register(SingleSelection, SingleSelectionAdmin)
