from django.shortcuts import render, get_object_or_404, redirect
from .models import Topic, Question, Option, QuizAttempt, UserAnswer
from django.contrib.auth.decorators import login_required
import random

def topic_list(request):
    topics = Topic.objects.all()
    return render(request, 'topic_list.html', {'topics': topics})


def start_quiz(request, topic_slug):
    topic = get_object_or_404(Topic, slug=topic_slug)
    questions = list(Question.objects.filter(topic=topic))
    random.shuffle(questions)
    for q in questions:
        q.options_list = list(q.options.all())
        random.shuffle(q.options_list)
    return render(request, 'start_quiz.html', {'topic': topic, 'questions': questions})


def submit_quiz(request, topic_slug):
    topic = get_object_or_404(Topic, slug=topic_slug)

    question_ids = request.POST.getlist('question_ids')
    questions = Question.objects.filter(id__in=question_ids)

    attempt = QuizAttempt.objects.create(
        user=request.user,
        topic=topic,
        attempted=questions.count(),
        correct_ans=0
    )

    correct_count = 0

    for q in questions:
        selected_id = request.POST.get(str(q.id))
        selected_option = Option.objects.filter(id=selected_id).first()

        is_correct = selected_option.is_correct_ans if selected_option else False
        if is_correct:
            correct_count += 1

        UserAnswer.objects.create(
            attempt=attempt,
            question=q,
            selected_option=selected_option,
            is_correct=is_correct
        )

    attempt.correct_ans = correct_count
    attempt.percent_correct = (correct_count / questions.count()) * 100
    attempt.wrong_questions = list(
        attempt.user_answers.filter(is_correct=False)
        .values_list('question_id', flat=True)
    )
    attempt.save()

    return redirect('quiz_result', attempt_id=attempt.id)


def quiz_result(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt, id=attempt_id)
    answers = []
    wrong_answers = []

    for ua in attempt.user_answers.select_related('question', 'selected_option'):
        correct_option = ua.question.options.filter(is_correct_ans=True).first()
        answer_dict = {
            'question': ua.question,
            'selected_option': ua.selected_option,
            'correct_option': correct_option,
            'is_correct': ua.is_correct
        }
        answers.append(answer_dict)
        if not ua.is_correct:
            wrong_answers.append(answer_dict)

    return render(request, 'result.html', {
        'attempt': attempt,
        'answers': answers,
        'wrong_answers': wrong_answers
    })


def retake_wrong(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt, id=attempt_id)
    wrong_question_ids = attempt.wrong_questions
    questions = Question.objects.filter(id__in=wrong_question_ids)

    for q in questions:
        q.options_list = list(q.options.all())
        random.shuffle(q.options_list)

    return render(request, 'start_quiz.html', {
        'topic': attempt.topic,
        'questions': questions
    })
