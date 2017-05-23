# -*- coding: utf-8 -*-

from django.contrib import admin

from paradoxvault.models import *


class SubjectAdmin(admin.ModelAdmin):
    list_display = ('subject_name',)


class DifficultyAdmin(admin.ModelAdmin):
    list_display = ('name', 'difficulty')


class QuestionBankAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'author', 'introduction', 'price', 'score',
                    'question_number', 'create_timestamp', 'update_timestamp')


class SelectionOptionAdmin(admin.ModelAdmin):
    list_display = ('selection_name', 'option')


class SelectionAdmin(admin.ModelAdmin):
    list_display = ('question_type', 'question_bank', 'grade', 'difficulty', 'question', 'answer')


class QuestionCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'question_bank', 'score', 'content', 'timestamp')

admin.site.register(Subject, SubjectAdmin)
admin.site.register(Difficulty, DifficultyAdmin)
admin.site.register(QuestionBank, QuestionBankAdmin)
admin.site.register(QuestionComment, QuestionCommentAdmin)
admin.site.register(Selection, SelectionAdmin)
admin.site.register(SelectionOptions, SelectionOptionAdmin)
