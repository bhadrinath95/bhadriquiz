from django.db import models

class Topic(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    question = models.TextField()
    answer_description = models.TextField()

    def __str__(self):
        return self.question[:50]


class Option(models.Model):
    question = models.ForeignKey(
        Question,
        related_name='options',
        on_delete=models.CASCADE
    )
    option_text = models.CharField(max_length=255)
    is_correct_ans = models.BooleanField(default=False)

    def __str__(self):
        return self.option_text


class QuizAttempt(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    attempted = models.PositiveIntegerField(default=0)
    correct_ans = models.PositiveIntegerField(default=0)
    percent_correct = models.FloatField(default=0)
    wrong_questions = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.topic.name


class UserAnswer(models.Model):
    attempt = models.ForeignKey(
        QuizAttempt,
        related_name='user_answers',
        on_delete=models.CASCADE
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(
        Option,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    is_correct = models.BooleanField(default=False)
