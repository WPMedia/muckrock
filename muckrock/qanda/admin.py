"""
Admin registration for Q&A models
"""

from django.contrib import admin

from qanda.models import Question, Answer

# These inhereit more than the allowed number of public methods
# pylint: disable=R0904

class AnswerInline(admin.TabularInline):
    """Answer Inline Admin"""
    model = Answer
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    """Quesiton Admin"""
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'user', 'date')
    search_fields = ('title', 'question')
    inlines = [AnswerInline]

admin.site.register(Question, QuestionAdmin)
