from django.contrib import admin
from .models import Topic, Question, Option, QuizAttempt, UserAnswer

class OptionInline(admin.TabularInline):
    model = Option
    extra = 2
    min_num = 2

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'get_correct_answer', 'topic')
    inlines = [OptionInline]

    def get_correct_answer(self, obj):
        correct_option = obj.options.filter(is_correct_ans=True).first()
        return correct_option.option_text if correct_option else "-"
    
    get_correct_answer.short_description = 'Correct Answer'

class TopicAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Topic, TopicAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Option)
admin.site.register(QuizAttempt)
admin.site.register(UserAnswer)
