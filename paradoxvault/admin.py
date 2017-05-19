# -*- coding: utf-8 -*-

from django.contrib import admin

from paradoxvault.models import *


class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)


class DifficultyAdmin(admin.ModelAdmin):
    list_display = ('name', 'difficulty')


class SingleSelectionAdmin(admin.ModelAdmin):
    list_display = ('subject', 'question', 'score', 'selectionA', 'selectionB', 'selectionC', 'selectionD', 'answer', 'difficulty')


class MultiSelectionAdmin(admin.ModelAdmin):
    list_display = ('subject', 'question', 'score', 'selectionA', 'selectionB', 'selectionC', 'selectionD', 'selectionE', 'selectionF', 'answer', 'difficulty')


class JudgementAdmin(admin.ModelAdmin):
    list_display = ('subject', 'question', 'score', 'answer', 'difficulty')


class FillBlanksAdmin(admin.ModelAdmin):
    list_display = ('subject', 'question', 'score', 'answer', 'difficulty')

admin.site.register(Subject, SubjectAdmin)
admin.site.register(Difficulty, DifficultyAdmin)
admin.site.register(SingleSelection, SingleSelectionAdmin)
admin.site.register(MultiSelection, MultiSelectionAdmin)
admin.site.register(Judge, JudgementAdmin)
admin.site.register(FillBlanks, FillBlanksAdmin)
