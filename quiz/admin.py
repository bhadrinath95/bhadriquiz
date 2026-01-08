from django.contrib import admin
from .models import Topic, Question, Option, QuizAttempt, UserAnswer

class OptionInline(admin.TabularInline):
    model = Option
    extra = 4
    min_num = 2

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'topic')
    inlines = [OptionInline]

class TopicAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Topic, TopicAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Option)
admin.site.register(QuizAttempt)
admin.site.register(UserAnswer)
