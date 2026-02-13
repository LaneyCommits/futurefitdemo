from django.shortcuts import render
from django.views.generic import TemplateView
from .quiz_data import get_questions, score_quiz, get_top_careers, get_career_categories


class QuizHomeView(TemplateView):
    template_name = 'career_quiz/quiz_home.html'


def quiz_view(request):
    questions = get_questions()
    return render(request, 'career_quiz/quiz.html', {'questions': questions})


def quiz_results_view(request):
    if request.method != 'POST':
        return render(request, 'career_quiz/quiz_results.html', {'suggestions': [], 'scores': [], 'error': True})
    # Option keys are submitted as q1, q2, ... q8
    selected = []
    for i in range(1, len(get_questions()) + 1):
        key = request.POST.get(f'q{i}')
        if key:
            selected.append(key)
    if len(selected) < len(get_questions()):
        return render(request, 'career_quiz/quiz_results.html', {
            'suggestions': [],
            'scores': [],
            'error': True,
            'message': 'Please answer all questions.',
        })
    score_tuples = score_quiz(selected)
    category_names = {c[0]: (c[1], c[2]) for c in get_career_categories()}
    scores_with_names = [
        (cat, score, category_names.get(cat, (cat, ''))[0], category_names.get(cat, (cat, ''))[1])
        for cat, score in score_tuples
    ]
    suggestions = get_top_careers(score_tuples, top_n=3)
    return render(request, 'career_quiz/quiz_results.html', {
        'suggestions': suggestions,
        'scores': scores_with_names,
        'error': False,
        'message': None,
    })
